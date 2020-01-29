import pygame
import sys
from pygame.locals import *
import subprocess

import Adafruit_MPR121.MPR121 as MPR121
cap = MPR121.MPR121()
if not cap.begin():
    print '???'

def main():
    pygame.init()
    myfont = pygame.font.Font(None,22)
    titlefont = pygame.font.Font(None,80)
    medfont = pygame.font.Font(None,40)
    screen = pygame.display.set_mode((1000,600))
    pygame.display.set_caption('Kalictric - Detection')

    buttoncolor = (100,100,255)
    newbuttoncolor = (255,100,100)

    t = pygame.time.Clock()

    buttonspace = 25
    buttonwidth = 50
    buttonindent = 25
    buttony = 100
    buttons = []
    ctr = 0
    for x in range(12):
        buttons.append(pygame.Rect(buttonindent+(buttonspace+buttonwidth)*x,buttony,buttonwidth,400))

    title = 'Kalimba Key Detection'
    def drawbutton(RECT,newcolor):
        if newcolor:
            pygame.draw.rect(screen,newbuttoncolor,RECT)
        else:
            pygame.draw.rect(screen,buttoncolor,RECT)


    last_touched = cap.touched()
    while True:
        screen.fill((0,0,0))
        '''DRAW TITLE'''
        screen.blit(titlefont.render(title,1,(255,255,255)),(10,10))

        '''KALIMBA KEY DETECTION'''
        current_touched = cap.touched()
        # Check each pin's last and current state to see if it was pressed or released.
        for i in range(12):
            # Each pin is represented by a bit in the touched value.  A value of 1
            # means the pin is being touched, and 0 means it is not being touched.
            pin_bit = 1 << i
            # First check if transitioned from not touched to touched.
            if current_touched & pin_bit:
                drawbutton(buttons[i],True)
                if not last_touched and pin_bit:
                    print('{0} touched!'.format(i))
            else:
                drawbutton(buttons[i],False)
            # Next check if transitioned from touched to not touched.
            if not current_touched & pin_bit and last_touched & pin_bit:
                print('{0} released!'.format(i))
        # Update last state and wait a short period before repeating.
        last_touched = current_touched

        '''EVENTS'''
        for event in pygame.event.get():
            if event.type == QUIT:
                print 'END'
                import Mainmenu
                Mainmenu.main()
            if event.type == KEYDOWN:
                execfile('Detection.py')

        pygame.display.update()
        t.tick(30)

if __name__ == '__main__':
    main()
