import random

import pygame

from .settings import WINDOW_SIZE, HOVER_BY_CLASS_WEIGHT_ENUM
from .settings import GROUND_BLOCK_SIZE, GROUND_BLOCK_TYPE_ENUM, GROUND_POSITION_TO_TYPE, GROUND_TYPE_TO_IMAGE_PATH


class Ground:
    class Food:
        def __init__(self, homeGroundBlock):
            self.scentValue = random.randint(1, 6)
            self.nutritiousValue = random.randint(1, 6)
    
    class GroundBlock:
        def __init__(self, id, type, rect):
            self.id = id
            self.type = type
            self.rect = rect
            self.image = pygame.image.load(GROUND_TYPE_TO_IMAGE_PATH[self.type]).convert_alpha()
            
            self.inhabitet = False
            self.inhabitable = self.type != GROUND_BLOCK_TYPE_ENUM.MIDDLE_BLOCK
            
            self.fertility = 0 if self.inhabitable == True else random.random()
            self.food = None
        
        def __int__(self):
            return HOVER_BY_CLASS_WEIGHT_ENUM.GROUND_BLOCK

        def collidepoint(self, point):
            if self.rect[0] > point[0]:
                return False
            if self.rect[1] > point[1]:
                return False
            if self.rect[0] + GROUND_BLOCK_SIZE > point[0] and self.rect[1] + GROUND_BLOCK_SIZE > point[1]:
                return True
            return False

        def render(self, renderScreen):
            if self.inhabitet:
                pygame.draw.rect(renderScreen, (255, 0, 0), (self.rect, (GROUND_BLOCK_SIZE, GROUND_BLOCK_SIZE)))
            else:
                renderScreen.blit(self.image, self.rect)
                    
        def getDebugInfo(self):
            return [
                'GROUND ID: ' + str(self.id),
                'INHABITABLE: ' + str(self.inhabitable) + ' INHABITET: ' + str(self.inhabitet),
                'RECT: ' + str(self.rect) + ' MOUSE: ' + str(pygame.mouse.get_pos()),
                'FERTILITY: ' + str(self.fertility),
            ]
            
    def __init__(self, EVENT_LOOP):
        self.EVENT_LOOP = EVENT_LOOP
        
        renderMargin = ((WINDOW_SIZE[0] % GROUND_BLOCK_SIZE) / 2,
                        (WINDOW_SIZE[1] % GROUND_BLOCK_SIZE) / 2)
        groundBlockCount = (
            WINDOW_SIZE[0] // GROUND_BLOCK_SIZE, WINDOW_SIZE[1] // GROUND_BLOCK_SIZE)

        self.groundBlocksList = []
        for x in range(groundBlockCount[0]):
            for y in range(groundBlockCount[1]):
                currentBlockPos = (
                    renderMargin[0] + (x * GROUND_BLOCK_SIZE), renderMargin[1] + (y * GROUND_BLOCK_SIZE))
                currentBlockPos2Type = (0 if x == 0 else -1 if x == (
                    groundBlockCount[0] - 1) else 1, 0 if y == 0 else -1 if y == (groundBlockCount[1] - 1) else 1)
                self.groundBlocksList.append(self.GroundBlock(len(
                    self.groundBlocksList), GROUND_POSITION_TO_TYPE[currentBlockPos2Type], currentBlockPos))
        
        self.findInhabitableGroundBlocks()
        
    def findInhabitableGroundBlocks(self):
        self.inhabitableGroundBlocks = []
        for groundBlock in self.groundBlocksList:
            if groundBlock.inhabitable == True and groundBlock.inhabitet == False:
                self.inhabitableGroundBlocks.append(groundBlock.id)
    
    def update(self):
        self.findInhabitableGroundBlocks()
        
    def render(self, renderScreen):
        for groundBlock in self.groundBlocksList:
            groundBlock.render(renderScreen)
            
    def getRandomGroundBlock(self):
        return random.choice(self.groundBlocksList)
    
    def getGroundBlockByID(self, id):
        return self.groundBlocksList[id]
    
    def getRandomHome(self):
        if self.inhabitableGroundBlocks != []:
            return self.groundBlocksList[random.choice(self.inhabitableGroundBlocks)]
        return None
