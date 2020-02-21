import pygame

from .settings import WINDOW_SIZE, BLOCK_SIZE, FONT_PATH
from .settings import TICKS_PER_DAY, FRAMES_PER_TICK


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
            self.isNight = True
        
        def updateDay(self):
            self.isNight = False
            self.currentFrame = 0
            self.currentTick = 0
        
        def renderTime(self, renderScreen):
            timeText = self.timeFont.render(str(self.currentTick) + '_' + str(self.currentFrame) + ':' + str(self.isNight), True, (255, 255, 255))
            renderScreen.blit(timeText, (20, 20))
        
        # def updateNight(self):
            
        # def updateDay(self):
        #     self.currentTick = 0
        #     self.framesPassed = 0
            
    
    class Block(pygame.sprite.Sprite):      
        def __init__(self, blockCoords, spritePath):
            pygame.sprite.Sprite.__init__(self)
            self.coords = blockCoords
            self.image = pygame.image.load('assets/sprites/grass/' + spritePath)
            self.rect = self.image.get_rect()
            self.rect.center = self.coords
    
    def __init__(self):
        self.margins = (WINDOW_SIZE[0] % BLOCK_SIZE / 2, WINDOW_SIZE[1] % BLOCK_SIZE / 2)
        self.blockCount = (WINDOW_SIZE[0] // BLOCK_SIZE, WINDOW_SIZE[1] // BLOCK_SIZE)
        print(f'#INITIALIZING ADHARAS__ BLOCKS={self.blockCount} MARGINS={self.margins}')
        
        self.blocksMatrix = []
        for y in range(self.blockCount[1]):
            self.blocksMatrix.append([])
            for x in range(self.blockCount[0]):
                blockCoords = (self.margins[0] + ((x * BLOCK_SIZE) + BLOCK_SIZE / 2), self.margins[1] + ((y * BLOCK_SIZE) + BLOCK_SIZE / 2))
                if y == 0 and x == 0:
                    b = self.Block(blockCoords, 'topLeft.png')
                elif y == 0 and x == (self.blockCount[0] - 1):
                    b = self.Block(blockCoords, 'topRight.png')
                elif y == 0:
                    b = self.Block(blockCoords, 'top.png')
                elif x == 0 and y == (self.blockCount[1] - 1):
                    b = self.Block(blockCoords, 'bottomLeft.png')
                elif x == (self.blockCount[0] - 1) and y == (self.blockCount[1] - 1):
                    b = self.Block(blockCoords, 'bottomRight.png')
                elif x == 0:
                    b = self.Block(blockCoords, 'left.png')
                elif x == (self.blockCount[0] - 1):
                    b = self.Block(blockCoords, 'right.png')
                elif y == (self.blockCount[1] - 1):
                    b = self.Block(blockCoords, 'bottom.png')
                else:
                    b = self.Block(blockCoords, 'middle.png')
                    
                self.blocksMatrix[-1].append(b)
        
        # add to rendering
        self.blockSpriteGroup = pygame.sprite.Group()
        for blockRow in self.blocksMatrix:
            for block in blockRow:
                self.blockSpriteGroup.add(block)
        
        # timing
        self.naturalClock = None
                
    def startSimulation(self):
        self.naturalClock = self.NaturalClock()
    
    def updateWorld(self):
        self.blockSpriteGroup.update() 
        
        if self.naturalClock != None:
            self.naturalClock.updateFrame()       
        
    def renderWorld(self, renderScreen):
        self.blockSpriteGroup.draw(renderScreen)
        if self.naturalClock != None:
            self.naturalClock.renderTime(renderScreen)  
        
        
        