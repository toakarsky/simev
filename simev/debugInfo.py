import enum

import pygame

from .settings import WINDOW_SIZE, FONT_PATH, DEBUG_INFO_FONT_SIZE


class DEBUG_INFO_POS_ENUM(enum.Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

class HoveredObjectsList:
    def __init__(self):
        self.hoveredObjects = []
    
    def append(self, object):
        self.hoveredObjects.append(object)
        self.hoveredObjects = sorted(self.hoveredObjects, key=lambda x : int(x))
        
    def clear(self):
        self.hoveredObjects = []
    
    def getHoveredObjectInfo(self, renderScreen):
        if self.hoveredObjects:
            d = DebugInfo(renderScreen, self.hoveredObjects[-1].getDebugInfo(), DEBUG_INFO_POS_ENUM.BOTTOM_RIGHT)
            

class DebugInfo:
    def __init__(self, renderScreen, debugInfoTextStrs, position):
        if debugInfoTextStrs == []:
            return
        
        debugFont = pygame.font.Font(FONT_PATH, DEBUG_INFO_FONT_SIZE)
        debugInfoTexts = []
        
        height = len(debugInfoTextStrs) * DEBUG_INFO_FONT_SIZE + 30
        width = 0
        for debugInfoTextStr in debugInfoTextStrs:
            debugInfoTexts.append(debugFont.render(debugInfoTextStr, True, (255, 255, 255)))
            width = max(width, debugInfoTexts[-1].get_width())
        width += 40
        
        debugSurface = pygame.Surface((width, height))
        debugSurface.set_alpha(128)
        debugSurface.fill((0, 0, 0))
        
        if position == DEBUG_INFO_POS_ENUM.TOP_LEFT:
            coords = (0, 0)
        elif position == DEBUG_INFO_POS_ENUM.TOP_RIGHT:
            coords = (WINDOW_SIZE[0] - width, 0)
        elif position == DEBUG_INFO_POS_ENUM.BOTTOM_LEFT:
            coords = (0, WINDOW_SIZE[1] - height)
        else:
            coords = (WINDOW_SIZE[0] - width, WINDOW_SIZE[1] - height)
        
        for i in range(len(debugInfoTextStrs)):
            debugSurface.blit(debugInfoTexts[i], (20, (i * DEBUG_INFO_FONT_SIZE) + 15))
            
        renderScreen.blit(debugSurface, coords)
        