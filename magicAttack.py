import math

class MagicAttack():
    def __init__(self,time,x,y,dxy):
        self.time = time #existing time in ms
        self.color = (0,0,0)
        self.velocity = 20
        self.firstCast = True
        self.x = x
        self.y = y
        self.dx = dxy[0]
        self.dy = dxy[1]


    def cast(self,currentTime):
        self.x += self.dx * self.velocity
        self.y += self.dy * self.velocity
        if self.firstCast:
            self.firstCastTime = currentTime
            self.firstCast = False
            return True
        else:
            if currentTime - self.firstCastTime >= self.time:
                return False
            else:
                return True 