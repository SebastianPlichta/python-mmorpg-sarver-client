import pygame
import animationHandler

class Player:
    def __init__(self,sprite,swidth,sheight,fps, cAmaxFrame,name,last_update_time = 0):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.width = swidth
        self.name = name
        self.height = sheight
        self.swidth, self.sheight = self.sprite.get_size()
        self.rows = int(self.sheight / self.height)
        self.columns = int(self.swidth / self.width)
        self.currentFrameID = 0
        self.currentFrame:pygame.image = self.sprite
        self.fps = fps
        self.last_update_time = last_update_time
        self.animationHandler = animationHandler.AnimationHandler(self.sprite,self.columns,self.rows,self.width,self.height)
        self.currentAnimation = 0
        self.cAmaxFrame = cAmaxFrame

    def nextFrame(self):
        if self.currentFrameID < self.cAmaxFrame - 1:
            self.currentFrameID += 1
        else:
            self.currentFrameID = 0
        valuetoreturn = self.currentAnimation*self.cAmaxFrame +self.currentFrameID
        self.animationHandler.frameList[valuetoreturn]
        return valuetoreturn

    def changeAnimation(self,index,max):
        self.currentAnimation = index
        self.cAmaxFrame = max