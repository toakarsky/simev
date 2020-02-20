import pygame

from .settings import WINDOW_SIZE, WINDOW_TITLE, WINDOW_ICON_PATH, FONT_PATH
from .adharas import Adharas


class Simulation:
    def __init__(self):
        pygame.init()
        self.shutdown = False
        self.simulate = False

        print(
            f'#INITIALIZING WINDOW__ SIZE={WINDOW_SIZE} TITLE={WINDOW_TITLE} ICON_PATH={WINDOW_ICON_PATH}')
        self.renderScreen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)
        self.icon = pygame.image.load(WINDOW_ICON_PATH)
        pygame.display.set_icon(self.icon)
        
        self.clock = pygame.time.Clock()
        
        # initialize Adharas
        self.adharas = Adharas()

        self.runMenuScreen()
        if self.simulate:
            self.runMainLoop()

    def runMenuScreen(self):
        # Title
        titleFont = pygame.font.Font(FONT_PATH, 82)
        titleText = titleFont.render('SimEv', True, (255, 255, 255))
        titleTextShadow = titleFont.render('SimEv', True, (128, 128, 128))
        titleTextPos = (WINDOW_SIZE[0] / 2 - titleText.get_width() / 2, 25)
        titleTextShadowPos = (titleTextPos[0] + 4, titleTextPos[1] + 4)

        # Run simulation button
        runSimButtonColor = (255, 255, 255)
        runSimButtonSize = (300, 100)
        runSimButtonCoords = (WINDOW_SIZE[0] / 2 - runSimButtonSize[0] / 2, WINDOW_SIZE[1] -
                              runSimButtonSize[1] - 25, runSimButtonSize[0], runSimButtonSize[1])

        def runSimButtonHovered():
            return (mouseCoords[0] - runSimButtonCoords[0] > 0) and (mouseCoords[0] - runSimButtonCoords[0] < runSimButtonSize[0]) and (mouseCoords[1] - runSimButtonCoords[1] > 0) and (mouseCoords[1] - runSimButtonCoords[1] < runSimButtonSize[1])

        print('*MENU SCREEN LOADED')
        while self.shutdown == False:
            # looping over every input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('_EVENT_GOT__ QUIT')
                    self.shutdown = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    print('_EVENT_GOT__ MOUSEBUTTONUP')
                    if runSimButtonHovered():
                        self.simulate = True
                        return

            # calculate everything
            mouseCoords = pygame.mouse.get_pos()
            if runSimButtonHovered():
                runSimButtonColor = (180, 180, 180)
            else:
                runSimButtonColor = (255, 255, 255)

            self.renderScreen.fill((0, 0, 0))
            # render everything
            self.adharas.render(self.renderScreen)
            self.renderScreen.blit(titleTextShadow, titleTextShadowPos)
            self.renderScreen.blit(titleText, titleTextPos)

            pygame.draw.rect(self.renderScreen,
                             runSimButtonColor, runSimButtonCoords)

            # flip everything
            pygame.display.update()
            self.clock.tick(60)

    def runMainLoop(self):
        print('*SIMULATION STARTED')
        while self.shutdown == False:
            # looping over every input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('_EVENT_GOT__ QUIT')
                    self.shutdown = True

            # calculate everything

            # render everything
            self.renderScreen.fill((0, 0, 0))

            # flip everything
            pygame.display.update()
            self.clock.tick(60)

    def __del__(self):
        print(f'#CLOSING WINDOW__')
