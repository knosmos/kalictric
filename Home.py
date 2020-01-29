screenw = 800
screenh = 600
import pygame
import sys
from pygame.locals import *
import subprocess
import kmodule

import Adafruit_MPR121.MPR121 as MPR121
cap = MPR121.MPR121()
if not cap.begin():
    print '???'

import mido

pygame.init()
myfont = pygame.font.Font(None,22)
titlefont = pygame.font.Font(None,80)
medfont = pygame.font.Font(None,40)
screen = pygame.display.set_mode((screenw,screenh),RESIZABLE)
pygame.display.set_caption('Kalictric - Home')

buttoncolor = (100,100,255)
newbuttoncolor = (255,100,100)

t = pygame.time.Clock()

buttonspace = screenw / 32
buttonwidth = buttonspace * 2
buttonindent = buttonspace
buttonheight = screenh * 0.8
buttony = 100
detect = pygame.Rect(buttonindent,buttony,buttonwidth,buttonheight)
learn = pygame.Rect(buttonspace+buttonwidth+buttonindent,buttony,buttonwidth,buttonheight)
compose = pygame.Rect((buttonspace+buttonwidth)*2+buttonindent,buttony,buttonwidth,buttonheight)
gamecontrol = pygame.Rect((buttonspace+buttonwidth)*3+buttonindent,buttony,buttonwidth,buttonheight)
keyboard = pygame.Rect((buttonspace+buttonwidth)*4+buttonindent,buttony,buttonwidth,buttonheight)
other = pygame.Rect((buttonspace+buttonwidth)*5+buttonindent,buttony,buttonwidth,buttonheight)
exit = pygame.Rect((buttonspace+buttonwidth)*6+buttonindent,buttony,buttonwidth,buttonheight)
#exit = pygame.Rect((buttonspace+buttionwidth)*7+buttonindent,buttony,buttonwidth,400)

    
buttons = [detect,learn,compose,gamecontrol,keyboard,other,exit]
names = ['Detect','Learn','Compose','Controller','Keyboard','Arcade','Exit']
fullnames = ['Detection','Learn','Composition Maker','Game Controller','Kalimba Keyboard','The Arcade','Exit']
links = ['Detection.py','kmodule.py','compose.py','gamepad.py', 'keyboard.py', 'Arcade.py', 'Quit.py']
title = 'KALICTRIC'
def drawbutton(RECT,newcolor,text):
    if newcolor:
        pygame.draw.rect(screen,newbuttoncolor,RECT)
    else:
        pygame.draw.rect(screen,buttoncolor,RECT)
    p = myfont.render(text,1,(250,250,250))
    screen.blit(p,(RECT.left - 2,RECT.top - 2))
def clicked(x,y,RECT):
    if RECT.collidepoint(x,y) == True:
        return True
    else:
        return False

last_touched = cap.touched()
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
            screen.blit(keyName,(buttonindent,buttonheight+30))
        else:
            drawbutton(buttons[i],False,names[i])

    '''KALIMBA KEY DETECTION'''
    current_touched = cap.touched()
    # Check each pin's last and current state to see if it was pressed or released.
    for i in range(12):
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
        pin_bit = 1 << i
        # First check if transitioned from not touched to touched.
        if current_touched & pin_bit and not last_touched & pin_bit:
            print('{0} touched!'.format(i))
            execfile(links[i])
        # Next check if transitioned from touched to not touched.
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))
    # Update last state and wait a short period before repeating.
    last_touched = current_touched

    '''EVENTS'''
    for event in pygame.event.get():
        if event.type == QUIT:
            print 'END'
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            for i in range(len(buttons)):
                if clicked(x,y,buttons[i]):
                    execfile(links[i])
        if event.type == KEYUP:
            if event.key == K_BACKSPACE:
                exit = False
                while True:
                    for event in pygame.event.get():
                        if event.type == KEYUP:
                            if event.key == K_RETURN:
                                title = 'MANGOES'
                                names = ['mango','mango','mango','mango','mango','mango','mango']
                                buttoncolor = (250,170,0)
                                exit = True
                    if exit:
                        break
                    t.tick(20)
        if event.type == VIDEORESIZE:
            screenw = event.w
            screenh = event.h
            pygame.display.set_mode((screenw,screenh),pygame.RESIZABLE)

            buttonspace = screenw / 32
            buttonwidth = buttonspace * 2
            buttonindent = buttonspace
            buttonheight = screenh * 0.8
            buttony = screenh / 6
            detect = pygame.Rect(buttonindent,buttony,buttonwidth,buttonheight)
            learn = pygame.Rect(buttonspace+buttonwidth+buttonindent,buttony,buttonwidth,buttonheight)
            compose = pygame.Rect((buttonspace+buttonwidth)*2+buttonindent,buttony,buttonwidth,buttonheight)
            gamecontrol = pygame.Rect((buttonspace+buttonwidth)*3+buttonindent,buttony,buttonwidth,buttonheight)
            keyboard = pygame.Rect((buttonspace+buttonwidth)*4+buttonindent,buttony,buttonwidth,buttonheight)
            other = pygame.Rect((buttonspace+buttonwidth)*5+buttonindent,buttony,buttonwidth,buttonheight)
            exit = pygame.Rect((buttonspace+buttonwidth)*6+buttonindent,buttony,buttonwidth,buttonheight)
            
            buttons = [detect,learn,compose,gamecontrol,keyboard,other,exit]
            

    pygame.display.update()
    t.tick(30)
