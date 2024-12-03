import pygame
import animationHandler

class Goblin():
    def __init__(self,x,y,hp,sprite):
        self.x = x
        self.y = y
        self.hp = hp
        self.sprite = sprite
        self.currentFrameID = 0
        self.animationHandler = animationHandler.AnimationHandler(sprite,8,1,16,32)
        self.cAmaxFrame = 8
        self.lastUpdateTime = 0
    
    def nextFrame(self):
        if self.currentFrameID < self.cAmaxFrame - 1:
            self.currentFrameID += 1
        else:
            self.currentFrameID = 0
        valuetoreturn = self.cAmaxFrame +self.currentFrameID
        return valuetoreturn
