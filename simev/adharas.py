import enum
import random

import pygame

from .settings import WINDOW_SIZE, FONT_PATH
from .settings import TICKS_PER_DAY, FRAMES_PER_TICK, STARTING_POPULATATION_SIZE

from .debugInfo import DebugInfo, DEBUG_INFO_POS_ENUM
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
            d = DebugInfo(renderScreen, timeTexts, DEBUG_INFO_POS_ENUM.TOP_LEFT)
            
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
        populationSize = min(len(self.ground.inhabitableGroundBlocks), populationSize)
        self.ground.update()
        for dianID in range(populationSize):
            self.dianPopulation.append(Dian(dianID, self.ground.getGroundBlockByID(self.ground.inhabitableGroundBlocks.pop(random.randrange(len(self.ground.inhabitableGroundBlocks)))), self.DIAN_EVENT_LOOP))            

    def updateWorld(self):
        if self.naturalClock == None:
            return
        
        self.naturalClock.updateFrame()
        
        for ncevent in self.NATURAL_CLOCK_EVENT_LOOP.get():
            if ncevent == self.NaturalClock.NATURAL_CLOCK_EVENTS_ENUM.NIGHT:
                print('_NATURAL_CLOCK_EVENT NIGTH_BEGAN')
                for dian in self.dianPopulation:
                    dian.sleep()
            if ncevent == self.NaturalClock.NATURAL_CLOCK_EVENTS_ENUM.DAY:
                print('_NATURAL_CLOCK_EVENT DAY_BEGAN')
                self.dayCount += 1
                for dian in self.dianPopulation:
                    dian.awake()
        self.NATURAL_CLOCK_EVENT_LOOP.clear()
        
        if self.naturalClock.isNight == False:
            self.ground.update()
        
        for devent in self.DIAN_EVENT_LOOP.get():
            if devent[0] == DIAN_EVENTS_ENUM.NEEDS_DESTINATION:
                print(f'_DIAN_EVENT NEEDS_DESTINATION DIAN_ID={devent[1]}')
                self.dianPopulation[devent[1]].setDestination(self.ground.getRandomGroundBlock())
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
        
