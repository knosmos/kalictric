import pygame
import time
from pygame.locals import *
pygame.init()
keys = pygame.transform.scale(pygame.image.load('KaliKaliUIDesign.png'),(1000,700))
pygame.display.set_caption('Kali Kali v1.0')
z=pygame.display.set_mode((1000,700))
t = pygame.time.Clock()
while True:
    z.blit(keys,(0,0))
    pygame.display.update()
    t.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            execfile('Home.py')
