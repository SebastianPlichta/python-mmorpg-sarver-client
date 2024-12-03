import pygame
import threading
import time

class AnimationHandler:
    def __init__(self,sprite,columns,row,frameWidth,frameHeight):
        self.frameList = []
        self.maxFrame = columns * row
        for i in range(row):
            for i2 in range(columns):
                fragment_rect = pygame.Rect(i2*frameWidth, i*frameHeight, frameWidth, frameHeight)
                fragment = sprite.subsurface(fragment_rect)
                scaled_fragment = pygame.transform.scale(fragment, (frameWidth*3, frameHeight*3))
                self.frameList.append(scaled_fragment)