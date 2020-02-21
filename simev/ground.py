import pygame

from .settings import WINDOW_SIZE, GROUND_BLOCK_SIZE, GROUND_POSITION_TO_TYPE, GROUND_TYPE_TO_IMAGE


class Ground:
    class GroundBlock:
        def __init__(self, id, type, rect):
            self.id = id
            self.type = type
            self.rect = rect
            self.image = pygame.image.load(GROUND_TYPE_TO_IMAGE[self.type])

        def render(self, renderScreen):
            renderScreen.blit(self.image, self.rect)

    def __init__(self):
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

    def render(self, renderScreen):
        for groundBlock in self.groundBlocksList:
            groundBlock.render(renderScreen)
