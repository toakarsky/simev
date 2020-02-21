import enum

import pygame

from .settings import GROUND_BLOCK_SIZE
from .settings import DIAN_IDLE_IMAGE_PATH, DIAN_SLEEP_IMAGE_PATH, DIAN_MOVE_SPEED


class DIAN_EVENTS_ENUM(enum.Enum):
    NEEDS_DESTINATION = 0


# TODO
# ADD ID TO THIS
DIAN_EVENT_LOOP = []

class Dian:
    class DIAN_STATES(enum.Enum):
        SLEEP = 0
        IDLE = 1

    def __init__(self, homeGroundBlock, EVENT_LOOP):
        self.IDLE_SPRITE = pygame.image.load(
            DIAN_IDLE_IMAGE_PATH).convert_alpha()
        self.SLEEP_SPRITE = pygame.image.load(
            DIAN_SLEEP_IMAGE_PATH).convert_alpha()
        self.EVENT_LOOP = EVENT_LOOP

        self.state = self.DIAN_STATES.IDLE
        self.homeGroundBlock = homeGroundBlock

        self.coords = (self.homeGroundBlock.rect[1] + GROUND_BLOCK_SIZE / 2 + self.IDLE_SPRITE.get_width(
        ) / 2, self.homeGroundBlock.rect[1] + GROUND_BLOCK_SIZE / 2 + self.IDLE_SPRITE.get_height() / 2)
        print(
            f'*DIAN_CREATED HOME_ID={self.homeGroundBlock.id} COORDS={self.coords}')

        self.destination = None
        self.destCoords = None
        self.searchingForDestination = False

    def sleep(self):
        self.coords = (self.homeGroundBlock.rect[1] + GROUND_BLOCK_SIZE / 2 + self.IDLE_SPRITE.get_width(
        ) / 2, self.homeGroundBlock.rect[1] + GROUND_BLOCK_SIZE / 2 + self.IDLE_SPRITE.get_height() / 2)
        self.state = self.DIAN_STATES.SLEEP
        self.destination = None
        self.destCoords = None
        self.searchingForDestination = False

    def awake(self):
        self.state = self.DIAN_STATES.IDLE
        self.searchingForDestination = False

    def findDestination(self):
        self.EVENT_LOOP.loop.append(DIAN_EVENTS_ENUM.NEEDS_DESTINATION)
        self.searchingForDestination = True

    def setDestination(self, destinationGroundBlock):
        self.destination = destinationGroundBlock
        
        self.destCoords = (self.destination.rect[1] + GROUND_BLOCK_SIZE / 2 + self.IDLE_SPRITE.get_width(
        ) / 2, self.destination.rect[1] + GROUND_BLOCK_SIZE / 2 + self.IDLE_SPRITE.get_height() / 2)

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

    def update(self):
        if self.state == self.DIAN_STATES.SLEEP:
            return

        # print(f'DIAN UPDATE {self.destination} {self.coords} {self.searchingForDestination}')
        if self.searchingForDestination == False and self.destination == None:
            self.findDestination()
        elif self.destination != None:
            self.moveTowardsDestination()
            
            if self.coords == self.destCoords:
                self.destination = None
                self.destCoords = None
                self.searchingForDestination = False

    def render(self, renderScreen):
        if self.state == self.DIAN_STATES.IDLE:
            renderScreen.blit(self.IDLE_SPRITE, self.coords)
        elif self.state == self.DIAN_STATES.SLEEP:
            renderScreen.blit(self.SLEEP_SPRITE, self.coords)