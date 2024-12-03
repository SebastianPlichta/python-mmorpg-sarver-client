import pygame
from pygame.locals import *
import client
import windowHandler
import player
import mapLoader
import enemies
import math

def checkPlayer():
    global cplayers, camera, name, windowSize
    detected:bool = False
    missing = []
    client.PlayerData()
    for i in client.globalPlayerList:
        for cplayer in cplayers:
            if cplayer.name == i['name']:
                detected = True
                if cplayer.name == name:
                    camera = [i['x']-windowSize[0]/2, i['y']-windowSize[1]/2]
                    currentPosition.clear()
                    currentPosition.append(i['x'])
                    currentPosition.append(i['y'])
        if not detected:
            missing.append(i)
        detected = False
    
    for newPlayer in missing:
        cplayers.append(player.Player('assets/characters/mike.png',16,32, 100,8,newPlayer['name']))

if __name__ == '__main__':
    running:bool = True
    name:str
    cplayers = []

    currentPosition = []

    clock = pygame.time.Clock()
    animation = 0
    betterAnimation = 0

    flip = False
    direction = 0
    camera = [0,0]
    name = ''

    windowSize = [1280,720]
    tilemapDrawed = False

    name = input()
    client.CtS(name)
    mainWindow = windowHandler.Window(windowSize[0],windowSize[1],False,'Project PMR')
    tilemaploader = mapLoader.TileLoader('testMap.json', 'assets/tileset.png')

    goblin = enemies.Goblin(50,50,100, pygame.image.load('assets/enemies/goblin1.png'))
    client.globalEnemiesList.append(goblin)

    while mainWindow.running: 

        tilemapDrawed = False

        mainWindow.screen.fill((0,0,0))

        if betterAnimation == 0: flip = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            client.move_player('W')
            animation = 3
            direction = 0
        elif keys[pygame.K_s]:
            client.move_player('S')
            direction = 1
            animation = 1
        elif keys[pygame.K_a]:
            client.move_player('A')
            direction = 2
            if betterAnimation == 0: flip = True
            animation = 5
        elif keys[pygame.K_d]:
            client.move_player('D')
            direction = 2
            animation = 5
        else:
            if direction == 2: animation = 4
            elif direction == 1: animation = 0 
            else: animation = 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainWindow.Quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    dx = mousePos[0] + camera[0] - currentPosition[0]
                    dy = mousePos[1] + camera[1] - currentPosition[1]
                    distance = math.sqrt(dx**2 + dy**2)
                    dx /= distance
                    dy /= distance
                    if dx > 0.5:
                        animation = 4
                        betterAnimation = 1
                        flip = False
                    elif dx < -0.5:
                        animation = 4
                        betterAnimation = 1
                        flip = True
                    elif dy > 0.5:
                        animation = 1
                        betterAnimation = 1
                    elif dy < -0.5:
                        animation = 3
                        betterAnimation = 1
                    client.addObject([1,1000, currentPosition, [dx,dy]]) #addObject Type,LifeTime in ms, position


        currentTime = pygame.time.get_ticks()

        checkPlayer()

        for cplayer in cplayers:

            if cplayer.name == client.globalName:
                if animation != None: #change player animation
                    if betterAnimation == 0:
                        cplayer.changeAnimation(animation,8)
                        animation = None
                    elif betterAnimation == 1:
                        cplayer.changeAnimation(animation,8)
                        animation = None
                        betterAnimation = 2

                if currentTime - cplayer.last_update_time >= cplayer.fps: #updating player animation
                    betterAnimation = 0
                    cplayer.last_update_time = currentTime
                    client.changeFrame([cplayer.nextFrame(),flip])

            for i in client.globalPlayerList:
                if cplayer.name == i['name']:
                    cameraPosX = i['x'] - cplayer.width*3 /2 - camera[0]
                    cameraPosY = i['y'] - cplayer.height*3 / 2- camera[1]
                    
                    #draw tileMap
                    if tilemapDrawed == False:
                        for x in tilemaploader.loadMap():
                            if (x.x + 64> camera[0] and x.x - 64 < camera[0] + windowSize[0] and 
                                x.y + 64> camera[1] and x.y - 64 < camera[1] + windowSize[1]):
                                mainWindow.screen.blit(x.img, (x.x - camera[0], x.y - camera[1]))
                                tilemapDrawed = True

                    #draw player with player name
                    text_surface = mainWindow.robotoBold.render(i['name'], False, (0, 0, 0))
                    mainWindow.screen.blit(pygame.transform.flip(cplayer.animationHandler.frameList[i['animationFrame']],i['flip'],False),(cameraPosX ,cameraPosY))
                    mainWindow.screen.blit(text_surface, (i['x'] - camera[0] - text_surface.get_width() / 2, cameraPosY - 60))

                    #draw enemies

                    for x in client.globalEnemiesList:
                        x.nextFrame()
                        mainWindow.screen.blit(x.animationHandler.frameList[0], (x.x - camera[0], x.y - camera[1]) )

                    #draw player projectiles

                    for x in client.globalObjectList:
                        if x.cast(currentTime):
                            pygame.draw.circle(mainWindow.screen, (255,255,255),(x.x - camera[0], x.y - camera[1]), 20,20)
                        else:
                            client.removeFromList(x)

        clock.tick(60)
        pygame.display.update()