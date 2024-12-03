import pygame
import sys


class Window:
    def __init__(self, width:int,height:int,fullScreen:bool,capction:str):
        pygame.init()
        self.width = width
        self.height = height
        self.fullScreen = fullScreen
        self.capction = capction
        self.running = True
        pygame.display.set_caption(self.capction)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.robotoBold = pygame.font.Font("assets/fonts/Roboto-Bold.ttf", 30)

    def Quit(self):
        self.running = False
        pygame.quit()
        sys.exit()