import pygame

from .settings import WINDOW_SIZE, FONT_PATH
from .settings import TICKS_PER_DAY, FRAMES_PER_TICK

from .ground import Ground
from .dian import Dian, DIAN_EVENTS_ENUM


class Adharas:
    class NaturalClock():
        def __init__(self):
            self.currentTick = 0
            self.currentFrame = 0
            self.timeFont = pygame.font.Font(FONT_PATH, 32)
            self.isNight = False

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
            print('_WORLD_EVENT_PUSHED NIGHT_BEGAN')
            self.isNight = True

        def updateDay(self):
            print('_WORLD_EVENT_PUSHED DAY_BEGAN')
            self.isNight = False
            self.currentFrame = 0
            self.currentTick = 0

        def renderTime(self, renderScreen):
            timeText = self.timeFont.render(str(self.currentTick) + '_' + str(
                self.currentFrame) + ':' + str("NIGHT" if self.isNight else "DAY"), True, (255, 255, 255))
            if self.isNight:
                # TODO:
                # Make this not retarded
                nightSky = pygame.Surface(WINDOW_SIZE)
                nightSky.set_alpha(64)
                nightSky.fill((36, 50, 64))
                renderScreen.blit(nightSky, (0, 0))
            renderScreen.blit(timeText, (20, 20))

    class EVENT_LOOP:
        def __init__(self):
            self.loop = []

    def __init__(self):
        self.naturalClock = None
        self.ground = Ground()
        
        self.singleDian = None
        self.DIAN_EVENT_LOOP = self.EVENT_LOOP()

    def startSimulation(self):
        self.naturalClock = self.NaturalClock()
        self.naturalClock.updateDay()
        
        self.singleDian = Dian(self.ground.getRandomGroundBlock(), self.DIAN_EVENT_LOOP)

    def updateWorld(self):
        if self.naturalClock == None:
            return
        
        self.naturalClock.updateFrame()
        
        # TODO:
        # Change this into an event
        if self.naturalClock.isNight:
            self.singleDian.sleep()
        elif self.naturalClock.currentFrame == 0 and self.naturalClock.currentTick == 0: 
            self.singleDian.awake()
        
        for devent in self.DIAN_EVENT_LOOP.loop:
            if devent == DIAN_EVENTS_ENUM.NEEDS_DESTINATION:
                print('_DIAN_EVENT NEEDS_DESTINATION')
                self.singleDian.setDestination(self.ground.getRandomGroundBlock())
        self.DIAN_EVENT_LOOP.loop = []
        self.singleDian.update()

    def renderWorld(self, renderScreen):
        self.ground.render(renderScreen)
        if self.naturalClock != None:
            self.naturalClock.renderTime(renderScreen)
        
        if self.singleDian != None:
            self.singleDian.render(renderScreen)
