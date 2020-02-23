import enum
import random

import pygame

from .settings import WINDOW_SIZE, FONT_PATH
from .settings import TICKS_PER_DAY, FRAMES_PER_TICK, STARTING_POPULATATION_SIZE

from .debugInfo import DebugInfo, HoveredObjectsList, DEBUG_INFO_POS_ENUM
from .ground import Ground
from .dian import Dian, DIAN_EVENTS_ENUM


class Adharas:
    class NaturalClock():
        class NATURAL_CLOCK_EVENTS_ENUM(enum.Enum):
            NIGHT = 0
            DAY = 1

        def __init__(self, EVENT_LOOP):
            self.currentTick = 0
            self.currentFrame = 0
            self.timeFont = pygame.font.Font(FONT_PATH, 32)
            self.isNight = False
            self.EVENT_LOOP = EVENT_LOOP

        def updateFrame(self):
            self.currentFrame += 1
            # if self.framesPassed
            if self.currentFrame == FRAMES_PER_TICK:
                self.updateTick()

        def updateTick(self):
            self.currentTick += 1
            self.currentFrame = 0

            if self.currentTick == TICKS_PER_DAY - 1:
                self.updateNight()
            if self.currentTick == TICKS_PER_DAY:
                self.updateDay()

        def updateNight(self):
            self.EVENT_LOOP.append(self.NATURAL_CLOCK_EVENTS_ENUM.NIGHT)
            self.isNight = True

        def updateDay(self):
            self.EVENT_LOOP.append(self.NATURAL_CLOCK_EVENTS_ENUM.DAY)
            self.isNight = False
            self.currentFrame = 0
            self.currentTick = 0

        def renderTime(self, renderScreen):
            timeTexts = [
                str(self.currentTick) + '_' + str(self.currentFrame),
                str("NIGHT" if self.isNight else "DAY"),
            ]
            d = DebugInfo(renderScreen, timeTexts,
                          DEBUG_INFO_POS_ENUM.TOP_LEFT)

            if self.isNight:
                # TODO:
                # Make this not retarded
                nightSky = pygame.Surface(WINDOW_SIZE)
                nightSky.set_alpha(64)
                nightSky.fill((36, 50, 64))
                renderScreen.blit(nightSky, (0, 0))

    class EVENT_LOOP:
        def __init__(self):
            self.loop = []

        def append(self, val):
            self.loop.append(val)

        def clear(self):
            self.loop = []

        def get(self):
            return self.loop

    def __init__(self):
        self.hoverObjectsList = HoveredObjectsList()
        self.statisticsList = []

        self.NATURAL_CLOCK_EVENT_LOOP = self.EVENT_LOOP()
        self.naturalClock = None

        self.GROUND_EVENT_LOOP = self.EVENT_LOOP()
        self.ground = Ground(self.GROUND_EVENT_LOOP)

        self.dianPopulation = []
        self.DIAN_EVENT_LOOP = self.EVENT_LOOP()

        self.dayCount = -1

    def startSimulation(self):
        self.naturalClock = self.NaturalClock(self.NATURAL_CLOCK_EVENT_LOOP)
        self.naturalClock.updateDay()

        self.generateStartingPopulation(STARTING_POPULATATION_SIZE)

    def generateStartingPopulation(self, populationSize):
        populationSize = min(
            len(self.ground.inhabitableGroundBlocks), populationSize)
        self.ground.update()
        for dianID in range(populationSize):
            self.dianPopulation.append(Dian(dianID, self.ground.getGroundBlockByID(self.ground.inhabitableGroundBlocks.pop(
                random.randrange(len(self.ground.inhabitableGroundBlocks)))), self.DIAN_EVENT_LOOP))

    def generateNextGeneration(self):
        offsprings = []
        for dian in self.dianPopulation:
            offspring = dian.generateOffsprings()
            offsprings.extend(offspring)

        # newPeople = []
        # for free_home in self.ground.inhabitableGroundBlocks:
        #     if random.uniform(0, 1) > 0.99:
        #         newPeople.append(Dian(32, self.ground.getGroundBlockByID(free_home), self.DIAN_EVENT_LOOP))

        self.dianPopulation = offsprings
        for i in range(len(self.dianPopulation)):
            self.dianPopulation[i].id = i

        # TODO:
        # WHEN EVERYTHING DIES

    def renderHoverInformation(self, renderScreen):
        self.hoverObjectsList.getHoveredObjectInfo(renderScreen)

    def getHoverInformation(self):
        self.hoverObjectsList.clear()
        for groundBlock in self.ground.groundBlocksList:
            if groundBlock.collidepoint(pygame.mouse.get_pos()):
                self.hoverObjectsList.append(groundBlock)
        for dian in self.dianPopulation:
            if dian.collidepoint(pygame.mouse.get_pos()):
                self.hoverObjectsList.append(dian)

    def printStatisticsConsole(self):
        # DIAN STATISTICS
        statsData = []
        for dian in self.dianPopulation:
            print(f'DIAN ID={dian.id}')
            statsData.append(dian.getStatisticData())
            print(statsData[-1])

        if len(self.dianPopulation) == 0:
            self.generateStartingPopulation(STARTING_POPULATATION_SIZE)
            return

        statistics = {}
        statsList = {}
        for k in statsData[0].keys():
            statistics[k] = [0, 0, 0, 0]
            statsList[k] = []

        for stats in statsData:
            for k in stats.keys():
                statsList[k].append(stats[k])
        for k in statsList.keys():
            statsList[k] = sorted(statsList[k])
            statistics[k][0] = statsList[k][0]
            statistics[k][1] = statsList[k][-1]
            statistics[k][2] = statsList[k][len(statsList[k]) // 2]
            statistics[k][3] = sum(statsList[k]) / len(statsList[k])

        self.statisticsList = [
            'DIAN POPULATION STATISTICS'
        ]
        for k in statsList.keys():
            self.statisticsList.append(k)
            text = '-- MIN: ' + str(statistics[k][0]) + ';MAX: ' + str(
                statistics[k][1]) + ';MEAN: ' + str(statistics[k][2]) + ';AVG: ' + str(statistics[k][3])
            self.statisticsList.append(text)

        print('----------- STATISTICS ------------')
        for s in self.statisticsList:
            print(s)
        print('--------- STATISTICS END ----------')

    def updateDianDestination(self, dian):
        getFoodWithScent = self.ground.searchForFoodScent(dian)
        if getFoodWithScent == None:
            dian.setDestination(self.ground.getRandomGroundBlock())
        else:
            dian.setDestination(getFoodWithScent.homeGroundBlock)

    def updateWorld(self):
        if self.naturalClock == None:
            return

        self.naturalClock.updateFrame()

        for ncevent in self.NATURAL_CLOCK_EVENT_LOOP.get():
            if ncevent == self.NaturalClock.NATURAL_CLOCK_EVENTS_ENUM.NIGHT:
                print('_NATURAL_CLOCK_EVENT NIGTH_BEGAN')
                self.DIAN_EVENT_LOOP.clear()
                self.ground.removeFood()
                for dian in self.dianPopulation:
                    dian.sleep()
            if ncevent == self.NaturalClock.NATURAL_CLOCK_EVENTS_ENUM.DAY:
                if self.dayCount > 0:
                    self.generateNextGeneration()
                for dian in self.dianPopulation:
                    dian.sleep()
                print('_NATURAL_CLOCK_EVENT DAY_BEGAN')
                self.ground.growFood()
                self.dayCount += 1
                for dian in self.dianPopulation:
                    dian.awake()
                self.printStatisticsConsole()
        self.NATURAL_CLOCK_EVENT_LOOP.clear()

        if self.naturalClock.isNight == False:
            self.ground.update()

        self.ground.updateFoodList()
        for devent in self.DIAN_EVENT_LOOP.get():
            if devent[0] == DIAN_EVENTS_ENUM.NEEDS_DESTINATION:
                # print(f'_DIAN_EVENT NEEDS_DESTINATION DIAN_ID={devent[1]}')
                self.updateDianDestination(self.dianPopulation[devent[1]])
            if devent[0] == DIAN_EVENTS_ENUM.SMELLING:
                # print(f'_DIAN_EVENT SMELLING_FOR_FOOD DIAN_ID={devent[1]}')
                smelledFood = self.ground.searchForFoodScent(
                    self.dianPopulation[devent[1]])
                if smelledFood != None:
                    self.dianPopulation[devent[1]].setDestination(
                        smelledFood.homeGroundBlock)

        self.DIAN_EVENT_LOOP.clear()
        for dian in self.dianPopulation:
            dian.update()

    def renderInfo(self, renderScreen):
        infoStrs = [
            'POP: ' + str(len(self.dianPopulation)),
            'DAYN: ' + str(self.dayCount),
        ]
        d = DebugInfo(renderScreen, infoStrs, DEBUG_INFO_POS_ENUM.TOP_RIGHT)

    def renderWorld(self, renderScreen):
        self.ground.render(renderScreen)
        if self.naturalClock == None:
            return

        for dian in self.dianPopulation:
            dian.render(renderScreen)
        self.naturalClock.renderTime(renderScreen)
        self.renderInfo(renderScreen)
