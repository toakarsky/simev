import pygame

from .settings import WINDOW_SIZE, BLOCK_SIZE


class Adharas:
    class Block(pygame.sprite.Sprite):      
        def __init__(self, blockCoords, spritePath):
            pygame.sprite.Sprite.__init__(self)
            self.coords = blockCoords
            self.image = pygame.image.load('assets/sprites/grass/' + spritePath)
            self.rect = self.image.get_rect()
            self.rect.center = self.coords
            
    def __init__(self, spritesGroup):
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
        for blockRow in self.blocksMatrix:
            for block in blockRow:
                spritesGroup.add(block)
        