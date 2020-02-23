import random

import pygame

from .settings import WINDOW_SIZE, HOVER_BY_CLASS_WEIGHT_ENUM
from .settings import GROUND_BLOCK_SIZE, GROUND_BLOCK_TYPE_ENUM, GROUND_POSITION_TO_TYPE, GROUND_TYPE_TO_IMAGE_PATH, FOOD_SIZE


class Ground:
    class Food:
        def __init__(self, id, homeGroundBlock):
            self.id = id
            self.homeGroundBlock = homeGroundBlock
            self.homeGroundBlock.food = self

            self.scentValue = 1
            self.nutritiousValue = 1

            MARGIN = (GROUND_BLOCK_SIZE - FOOD_SIZE) / 2
            self.rect = (
                self.homeGroundBlock.rect[0] + MARGIN, self.homeGroundBlock.rect[1] + MARGIN)

        def __del__(self):
            self.homeGroundBlock.food = None

        def getDebugInfo(self):
            return [
                'SCENT_VALUE: ' + str(self.scentValue),
                'NUTRITIOUS_VALUE: ' + str(self.nutritiousValue),
            ]

        def render(self, renderScreen):
            pygame.draw.rect(renderScreen, (0, 255, 0),
                             (self.rect, (FOOD_SIZE, FOOD_SIZE)))

    class GroundBlock:
        def __init__(self, id, type, rect):
            self.id = id
            self.type = type
            self.rect = rect
            self.image = pygame.image.load(
                GROUND_TYPE_TO_IMAGE_PATH[self.type]).convert_alpha()

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
            renderScreen.blit(self.image, self.rect)

        def getDebugInfo(self, renderScreen):
            info = [
                'GROUND ID: ' + str(self.id),
                'INHABITABLE: ' + str(self.inhabitable) +
                ' INHABITET: ' + str(self.inhabitet),
                'RECT: ' + str(self.rect) + ' MOUSE: ' +
                str(pygame.mouse.get_pos()),
                'FERTILITY: ' + str(self.fertility),

                'FOOD:',
            ]

            if self.food == None:
                info.append('None')
            else:
                info.extend(self.food.getDebugInfo())

            return info

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

        self.foodList = []

    def findInhabitableGroundBlocks(self):
        self.inhabitableGroundBlocks = []
        for groundBlock in self.groundBlocksList:
            if groundBlock.inhabitable == True and groundBlock.inhabitet == False:
                self.inhabitableGroundBlocks.append(groundBlock.id)

    def update(self):
        self.findInhabitableGroundBlocks()
        for groundBlock in self.groundBlocksList:
            if groundBlock.food != None and groundBlock.food.nutritiousValue == 0:
                groundBlock.food = None
        self.updateFoodList()

    def removeFood(self):
        self.foodList = []

    def updateFoodList(self):
        updatedFoodList = []
        for i in range(len(self.foodList)):
            if self.foodList[i].nutritiousValue > 0:
                updatedFoodList.append(self.foodList[i])
        for i in range(len(updatedFoodList)):
            updatedFoodList[i].id = i
        self.foodList = updatedFoodList

    def growFood(self):
        # OLD METHOD
        # fertilityRequired = random.uniform(0.5, 1)
        # print(f'*GROWING FOOD FERTILITY_REQUIRED={fertilityRequired}')
        # for groundBlock in self.groundBlocksList:
        #     if groundBlock.fertility > 0 and random.random() > fertilityRequired:
        #         self.foodList.append(
        #             self.Food(len(self.foodList), groundBlock))
        fertileGroundBlocks = []
        for groundBlock in self.groundBlocksList:
            if groundBlock.fertility > 0:
                fertileGroundBlocks.append(groundBlock.id)

        for i in range(50):
            choosenBlock = fertileGroundBlocks.pop(
                random.randrange(len(fertileGroundBlocks)))
            self.foodList.append(
                self.Food(len(self.foodList),
                          self.groundBlocksList[choosenBlock])
            )

    def searchForFoodScent(self, dian):
        scents = []
        for food in self.foodList:
            dist = (abs(dian.coords[0] - food.rect[0]) / GROUND_BLOCK_SIZE) + \
                (abs(dian.coords[1] - food.rect[1]) / GROUND_BLOCK_SIZE)
            if dist <= food.scentValue + dian.smellStrength and food.nutritiousValue > 0:
                scents.append(
                    ((food.scentValue + dian.smellStrength) - dist, food.id))
        scents = sorted(scents)
        if scents != []:
            return self.foodList[scents[-1][1]]
        return None

    def render(self, renderScreen):
        for groundBlock in self.groundBlocksList:
            groundBlock.render(renderScreen)

        for food in self.foodList:
            food.render(renderScreen)

    def getRandomGroundBlock(self):
        return random.choice(self.groundBlocksList)

    def getGroundBlockByID(self, id):
        return self.groundBlocksList[id]

    def getRandomHome(self):
        if self.inhabitableGroundBlocks != []:
            return self.groundBlocksList[random.choice(self.inhabitableGroundBlocks)]
        return None
