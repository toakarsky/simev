import pygame

from .settings import WINDOW_SIZE, BLOCK_SIZE


class Adharas:
    class Block:      
        def __init__(self, blockCoords):
            self.coords = blockCoords
            
        def render(self, renderScreen):
            # TODO:
            #   Render actual sprite
            pygame.draw.rect(renderScreen, (67, 176, 72), self.coords)          
    
    def __init__(self):
        self.margins = (WINDOW_SIZE[0] % BLOCK_SIZE / 2, WINDOW_SIZE[1] % BLOCK_SIZE / 2)
        self.blockCount = (WINDOW_SIZE[0] // BLOCK_SIZE, WINDOW_SIZE[1] // BLOCK_SIZE)
        print(f'#INITIALIZING ADHARAS__ BLOCKS={self.blockCount} MARGINS={self.margins}')
        
        self.blocksMatrix = []
        for y in range(self.blockCount[1]):
            self.blocksMatrix.append([])
            for x in range(self.blockCount[0]):
                blockCoords = (self.margins[0] + (x * BLOCK_SIZE), self.margins[1] + (y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
                self.blocksMatrix[-1].append(self.Block(blockCoords))
    
    def render(self, renderScreen):
        for blockRow in self.blocksMatrix:
            for block in blockRow:
                block.render(renderScreen)
        