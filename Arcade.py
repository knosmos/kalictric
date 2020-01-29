import kmodule
import pygame
import sys
from pygame.locals import *
import subprocess

import Adafruit_MPR121.MPR121 as MPR121
cap = MPR121.MPR121()
if not cap.begin():
    print '???'
pygame.init()

def main():
    import time
    time.sleep(0)

    myfont = pygame.font.Font(None,22)
    titlefont = pygame.font.Font(None,80)
    medfont = pygame.font.Font(None,40)
    screen = pygame.display.set_mode((700,500))
    pygame.display.set_caption('Kalictric - Arcade')


    buttoncolor = (100,255,100)
    newbuttoncolor = (255,100,100)

    t = pygame.time.Clock()

    buttonspace = 40
    buttonwidth = 50
    buttonindent = 25
    buttony = 100
    collide = pygame.Rect(buttonindent,buttony,50,200)
    minecraft = pygame.Rect(buttonspace+buttonwidth+buttonindent,buttony,buttonwidth,200)
    tetris = pygame.Rect((buttonspace+buttonwidth)*2+buttonindent,buttony,buttonwidth,200)
    pingpong = pygame.Rect((buttonspace+buttonwidth)*3+buttonindent,buttony,buttonwidth,200)
    blocks512 = pygame.Rect((buttonspace+buttonwidth)*4+buttonindent,buttony,buttonwidth,200)
    back = pygame.Rect((buttonspace+buttonwidth)*5+buttonindent,buttony,buttonwidth,200)
    exit = pygame.Rect((buttonspace+buttonwidth)*6+buttonindent,buttony,buttonwidth,200)
    #exit = pygame.Rect((buttonspace+buttonwidth)*7+buttonindent,buttony,buttonwidth,200)

    #Programs to run
    import Collide
    import lines
    import tetromino
    import pong
    import launchminecraft
    import Mainmenu
    import Blocky
    #import Quit

        
    buttons = [collide,minecraft,tetris,pingpong,blocks512,back,exit]
    names = ['Collide','Minecraft','Lines','Tetromino','Pong','512','Back','Exit']
    fullnames = ["Don't hit the yellow squares",'Minecraft Pi','Lines (Tron Clone)','Tetromino (Tetris clone)','Make your opponent miss the ball','A Game like 2048','Back to Homescreen','Exit']
    links = [Collide,launchminecraft,lines,tetromino,pong,Blocky,Mainmenu,'Quit.py']
    title = 'Arcade'
    def drawbutton(RECT,newcolor,text):
        if newcolor:
            pygame.draw.rect(screen,newbuttoncolor,RECT)
        else:
            pygame.draw.rect(screen,buttoncolor,RECT)
        p = myfont.render(text,1,(255,255,255))
        screen.blit(p,(RECT.left,RECT.top-20))
    def clicked(x,y,rect):
        if rect.collidepoint(x,y) == True:
            return True
        else:
            return False

    #last_touched = cap.touched()
    while True:
        x,y = pygame.mouse.get_pos()
        screen.fill((0,0,0))
        '''DRAW TITLE'''
        screen.blit(titlefont.render(title,1,(255,255,255)),(10,10))
        '''DRAW BUTTONS'''
        for i in range(len(buttons)):
            if clicked(x,y,buttons[i]):
                drawbutton(buttons[i],True,names[i])
                keyName = myfont.render(fullnames[i],1,(255,255,255))
                screen.blit(keyName,(buttonindent,400))
            else:
                drawbutton(buttons[i],False,names[i])

        '''KALIMBA KEY DETECTION'''
        '''current_touched = cap.touched()
        # Check each pin's last and current state to see if it was pressed or released.
        for i in range(12):
            # Each pin is represented by a bit in the touched value.  A value of 1
            # means the pin is being touched, and 0 means it is not being touched.
            pin_bit = 1 << i
            # First check if transitioned from not touched to touched.
            if current_touched & pin_bit and not last_touched & pin_bit:
                print('{0} touched!'.format(i))
                try:
                    execfile(links[i])
                except IndexError:
                    print "That's not an option"
            # Next check if transitioned from touched to not touched.
            if not current_touched & pin_bit and last_touched & pin_bit:
                print('{0} released!'.format(i))
        # Update last state and wait a short period before repeating.
        last_touched = current_touched'''
        detection = kmodule.detect()
        if detection <= len(links)-1:
            links[detection-1].main()

        '''EVENTS'''
        for event in pygame.event.get():
            if event.type == QUIT:
                print 'END'
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if clicked(x,y,buttons[i]):
                        links[i].main()
                        

        pygame.display.update()
        t.tick(30)

if __name__ == '__main__':
    main()
