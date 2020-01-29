import pygame
import sys
from pygame.locals import *
pygame.init()

myfont = pygame.font.Font(None,30)
screen = pygame.display.set_mode((400,300))
pygame.display.set_caption('Stem Cell')

t = pygame.time.Clock()

def SomeFunction(screen):
    p = myfont.render('STEM CELL',1,(255,255,255))
    screen.blit(p,(10,10))
    p = myfont.render('FOR ANY PURPOSE ONLY',1,(200,200,255))
    screen.blit(p,(10,60))
while True:
    x,y = pygame.mouse.get_pos()
    screen.fill((0,0,0))
    SomeFunction(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            print 'END'
            pygame.quit()
            sys.exit()
    pygame.display.update()
    t.tick(30)