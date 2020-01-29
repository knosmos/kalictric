import pygame
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Inki')
screen = pygame.display.set_mode((500,500))
ticktock = pygame.time.Clock()
screen.fill((255,255,255))
pendown = False
while True:
    x,y = pygame.mouse.get_pos()
    if pendown:
        pygame.draw.ellipse(screen, (0,0,0), (x,y,10,10))        
    for event in pygame.event.get():
        if event.type == QUIT:
            execfile('Home.py')
        elif event.type == MOUSEBUTTONDOWN:
            pendown = True
        elif event.type == MOUSEBUTTONUP:
            pendown = False

    ticktock.tick(30)
    pygame.display.update()