import enum
import random

import pygame

from .settings import GROUND_BLOCK_SIZE, HOVER_BY_CLASS_WEIGHT_ENUM
from .settings import DIAN_IDLE_IMAGE_PATH, DIAN_SLEEP_IMAGE_PATH, DIAN_MOVE_SPEED


class DIAN_EVENTS_ENUM(enum.Enum):
    NEEDS_DESTINATION = 0
    SMELLING = 1


# TODO
# ADD ID TO THIS
DIAN_EVENT_LOOP = []


class Dian:
    class DIAN_STATES(enum.Enum):
        SLEEP = 0
        IDLE = 1
        FOLLOWING_FOOD = 2
        EATING_FOOD = 3

    def __int__(self):
        return int(HOVER_BY_CLASS_WEIGHT_ENUM.DIAN)

    def __init__(self, id, homeGroundBlock, EVENT_LOOP, generation=1):
        self.id = id
        self.IDLE_SPRITE = pygame.image.load(
            DIAN_IDLE_IMAGE_PATH).convert_alpha()
        self.SLEEP_SPRITE = pygame.image.load(
            DIAN_SLEEP_IMAGE_PATH).convert_alpha()
        self.EVENT_LOOP = EVENT_LOOP

        self.state = self.DIAN_STATES.IDLE
        self.homeGroundBlock = homeGroundBlock
        self.homeGroundBlock.inhabitet = True

        self.coords = (self.homeGroundBlock.rect[0] + (GROUND_BLOCK_SIZE - self.IDLE_SPRITE.get_width(
        )) / 2, self.homeGroundBlock.rect[1] + (GROUND_BLOCK_SIZE - self.IDLE_SPRITE.get_height()) / 2)
        print(
            f'*DIAN_CREATED HOME_ID={self.homeGroundBlock.id} COORDS={self.coords} TYPE={self.homeGroundBlock.type}')

        self.destination = None
        self.destCoords = None
        self.searchingForDestination = False

        self.generation = generation
        self.smellStrength = random.randint(1, 10)
        self.foodCollected = 0

    def __del__(self):
        self.homeGroundBlock.inhabitet = False

    def collidepoint(self, point):
        if self.coords[0] > point[0]:
            return False
        if self.coords[1] > point[1]:
            return False
        if self.coords[0] + self.IDLE_SPRITE.get_width() > point[0] and self.coords[1] + self.IDLE_SPRITE.get_height() > point[1]:
            return True
        return False

    def drawDebugLine(self, renderScreen, object, color):
        LINE_WEIGHT = 5
        ourX = self.coords[0] + \
            self.IDLE_SPRITE.get_width() / 2 - LINE_WEIGHT / 2
        ourY = self.coords[1] + \
            self.IDLE_SPRITE.get_height() / 2 - LINE_WEIGHT / 2
        theirX = object.rect[0] + GROUND_BLOCK_SIZE / 2 - LINE_WEIGHT / 2
        theirY = object.rect[1] + GROUND_BLOCK_SIZE / 2 - LINE_WEIGHT / 2

        dist = ((abs(ourX - theirX)), (abs(ourY - theirY)))
        linePoints = (min(ourX, theirX), min(ourY, theirY))
        pygame.draw.rect(renderScreen, color,
                         ((linePoints[0], ourY), (dist[0], LINE_WEIGHT)))
        pygame.draw.rect(renderScreen, color,
                         ((theirX - 1, linePoints[1]), (LINE_WEIGHT, dist[1])))

    def getDebugInfo(self, renderScreen):
        if self.destination != None:
            self.drawDebugLine(renderScreen, self.destination, (68, 244, 23))
            pygame.draw.rect(renderScreen, (0, 255, 255),
                             (self.destination.rect, (GROUND_BLOCK_SIZE, GROUND_BLOCK_SIZE)))
        self.drawDebugLine(renderScreen, self.homeGroundBlock, (244, 23, 58))
        pygame.draw.rect(renderScreen, (255, 0, 255),
                         (self.homeGroundBlock.rect, (GROUND_BLOCK_SIZE, GROUND_BLOCK_SIZE)))

        return [
            'DIAN ID: ' + str(self.id),
            'GENERATION #: ' + str(self.generation),
            'COORDS: ' + str((int(self.coords[0]), int(self.coords[1]))
                             ) + ' MOUSE: ' + str(pygame.mouse.get_pos()),
            'STATE: ' + str(self.state),
            'SMELL_STRENTGH: ' + str(self.smellStrength),
        ]

    def sleep(self):
        self.coords = (self.homeGroundBlock.rect[0] + (GROUND_BLOCK_SIZE - self.IDLE_SPRITE.get_width(
        )) / 2, self.homeGroundBlock.rect[1] + (GROUND_BLOCK_SIZE - self.IDLE_SPRITE.get_height()) / 2)
        self.state = self.DIAN_STATES.SLEEP
        self.destination = None
        self.destCoords = None
        self.searchingForDestination = False

    def awake(self):
        self.state = self.DIAN_STATES.IDLE
        self.searchingForDestination = False

        self.foodCollected = 0

    def findDestination(self):
        self.EVENT_LOOP.append((DIAN_EVENTS_ENUM.NEEDS_DESTINATION, self.id))
        self.searchingForDestination = True

    def setDestination(self, destinationGroundBlock):
        self.destination = destinationGroundBlock
        if self.destination.food != None:
            self.state = self.DIAN_STATES.FOLLOWING_FOOD

        self.destCoords = (self.destination.rect[0] + (GROUND_BLOCK_SIZE - self.IDLE_SPRITE.get_width(
        )) / 2, self.destination.rect[1] + (GROUND_BLOCK_SIZE - self.IDLE_SPRITE.get_height()) / 2)

        self.searchingForDestination = False

    def moveTowardsDestination(self):
        newCoordsX = self.coords[0]
        newCoordsY = self.coords[1]
        if newCoordsX != self.destCoords[0]:
            if abs(self.coords[0] - self.destCoords[0]) <= DIAN_MOVE_SPEED:
                newCoordsX = self.destCoords[0]
            else:
                if newCoordsX > self.destCoords[0]:
                    newCoordsX -= DIAN_MOVE_SPEED
                else:
                    newCoordsX += DIAN_MOVE_SPEED
        else:
            if abs(self.coords[1] - self.destCoords[1]) <= DIAN_MOVE_SPEED:
                newCoordsY = self.destCoords[1]
            else:
                if newCoordsY > self.destCoords[1]:
                    newCoordsY -= DIAN_MOVE_SPEED
                else:
                    newCoordsY += DIAN_MOVE_SPEED
        self.coords = (newCoordsX, newCoordsY)

    def smellForFood(self):
        self.EVENT_LOOP.append((DIAN_EVENTS_ENUM.SMELLING, self.id))

    def eatFood(self):
        if self.destination.food == None or self.destination.food.nutritiousValue == 0:
            self.state = self.DIAN_STATES.IDLE
            self.destination = None
        else:
            self.destination.food.nutritiousValue -= 1
            self.foodCollected += 1

    def update(self):
        if self.state == self.DIAN_STATES.SLEEP:
            return

        if self.state == self.DIAN_STATES.IDLE:
            if self.searchingForDestination == False and self.destination == None:
                self.findDestination()
            else:
                self.smellForFood()
        if self.state == self.DIAN_STATES.IDLE or self.state == self.DIAN_STATES.FOLLOWING_FOOD:
            if self.destination != None:
                self.moveTowardsDestination()

                if self.coords == self.destCoords:
                    if self.destination.food != None:
                        self.state = self.DIAN_STATES.EATING_FOOD
                    else:
                        self.destination = None
                        self.destCoords = None
                        self.searchingForDestination = False
        elif self.state == self.DIAN_STATES.EATING_FOOD:
            self.eatFood()

    def render(self, renderScreen):
        if self.state == self.DIAN_STATES.SLEEP:
            renderScreen.blit(self.SLEEP_SPRITE, self.coords)
        renderScreen.blit(self.IDLE_SPRITE, self.coords)
