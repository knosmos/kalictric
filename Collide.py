import Adafruit_MPR121.MPR121 as sensor
cap = sensor.MPR121()
if not cap.begin:
    print '???'
import kmodule
import pygame
import random
import time
from pygame.locals import *
pygame.init()
def main():
    screen = pygame.display.set_mode((400,300))
    pygame.display.set_caption('Collide')

    '''VARIABLES'''
    playery = 130

    ticktock = pygame.time.Clock()
    speed = 20
    direction = 1
    enemies = []
    blues = []
    lost = False
    #last_touched = cap.touched()
    for x in range(0,10):
        enemies.append([random.randint(-1000,0),random.randint(0,300)])
        blues.append([random.randint(-1000,0),random.randint(0,300)])
    while True:
        '''if kmodule.detect() == 5:
            speed = 0
            print 'slowdown!'
        else:
            speed = 20'''
        '''while lost:
            screen.fill((255,255,255))
            pygame.display.update()
            ticktock.tick(20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == MOUSEBUTTONUP:
                    lost = False
                    enemies = []
                    for x in range(0,10):
                        enemies.append([random.randint(-1000,0),random.randint(0,300)])'''
        player = pygame.rect.Rect(180,playery,40,40)
        screen.fill((0,0,0))
        '''DRAW PLAYER'''
        pygame.draw.rect(screen, (200,100,100), (player))
        '''MOVE PLAYER'''
        playery+=speed*direction
        if playery > 300 or playery < 0:
            direction = direction*-1
        '''RENDER ENEMIES'''
        for object in enemies:
            pygame.draw.rect(screen, (200,200,0), (object[0],object[1],20,20))
            object[0]+=10
            if object[0] > 420:
                object[0] = random.randint(-1000,0)
            '''DETECT HIT'''
            obrect = pygame.rect.Rect(object[0],object[1],20,20)
            if obrect.colliderect(player):
                screen.fill((255,255,255))
                pygame.display.update()
                time.sleep(0.5)
                enemies = []
                for x in range(0,10):
                    enemies.append([random.randint(-1000,0),random.randint(0,300)])
        '''RENDER BLUES'''
        for object in blues:
            pygame.draw.rect(screen, (100,120,200), (object[0],object[1],20,20))
            object[0]+=10
            if object[0] > 420:
                object[0] = random.randint(-1000,0)
        '''if cap.is_touched(0):
            speed = 5
        else:
            speed = 10'''
        if kmodule.constdetect() == 5:
            speed = 5
            print 'slowdown!'
        else:
            speed = 20

        '''EVENTS'''
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                speed = 5
            if event.type == MOUSEBUTTONUP:
                speed = 20
        pygame.display.update()
        ticktock.tick(20)           
            
if __name__ == '__main__':            
    main()   
