import pygame
import sys
from pygame.locals import *
import subprocess




def main():
    screenw = 800
    screenh = 600

    import Adafruit_MPR121.MPR121 as MPR121
    cap = MPR121.MPR121()
    if not cap.begin():
        print '???'

    import mido
    import kmodule
    import compose
    import song
    import Detection
    import gamepad
    import keyboard
    import launchminecraft
    import tetromino
    
    pygame.init()
    myfont = pygame.font.Font(None,22)
    titlefont = pygame.font.Font(None,80)
    medfont = pygame.font.Font(None,40)
    screen = pygame.display.set_mode((screenw,screenh),RESIZABLE)
    pygame.display.set_caption('Kalictric - Home')

    buttoncolor = (100,100,255)
    newbuttoncolor = (255,100,100)
    keylen = [80,60,40,20,0,-20,0,20,40,60]

    t = pygame.time.Clock()

    buttonspace = screenw / 32
    buttonwidth = buttonspace * 2
    buttonindent = buttonspace
    buttonheight = screenh * 0.8
    buttony = 100
    detect = pygame.Rect(buttonindent,buttony,buttonwidth,buttonheight)
    learn = pygame.Rect(buttonspace+buttonwidth+buttonindent,buttony,buttonwidth,buttonheight)
    composer = pygame.Rect((buttonspace+buttonwidth)*2+buttonindent,buttony,buttonwidth,buttonheight)
    songs = pygame.Rect((buttonspace+buttonwidth)*3+buttonindent,buttony,buttonwidth,buttonheight)
    gamecontrol = pygame.Rect((buttonspace+buttonwidth)*4+buttonindent,buttony,buttonwidth,buttonheight)
    kkeyboard = pygame.Rect((buttonspace+buttonwidth)*5+buttonindent,buttony,buttonwidth,buttonheight)
    minecraftpi = pygame.Rect((buttonspace+buttonwidth)*6+buttonindent,buttony,buttonwidth,buttonheight)
    tetris = pygame.Rect((buttonspace+buttonwidth)*7+buttonindent,buttony,buttonwidth,buttonheight)
    exit = pygame.Rect((buttonspace+buttonwidth)*8+buttonindent,buttony,buttonwidth,buttonheight)
        
    buttons = [detect,learn,composer,songs,gamecontrol,kkeyboard,minecraftpi,tetris,exit]
    names = ['Detect','Learn','Compose','Songs','Controller','Keyboard','Minecraft','Tetris','Exit']
    fullnames = ['Detection','Learn','Composition Maker','Song playback','Game Controller', 'Minecraft-Pi', 'Tetris clone','Kalimba Keyboard','The Arcade','Exit']
    links = [Detection,kmodule,compose,song,gamepad, keyboard, launchminecraft, tetromino]

    for x in range(len(buttons)):
        buttons[x].height -= keylen[x]

    title = 'KALICTRIC'
    def drawbutton(RECT,newcolor,text):
        if newcolor:
            pygame.draw.rect(screen,newbuttoncolor,RECT)
        else:
            pygame.draw.rect(screen,buttoncolor,RECT)
        p = myfont.render(text,1,(250,250,250))
        screen.blit(p,(RECT.left,RECT.top - 25))
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
        pygame.draw.rect(screen, (100,200,100), (0,screenh*0.4,screenw,screenh*0.05))
        '''KALIMBA KEY DETECTION'''
        current_touched = cap.touched()
        # Check each pin's last and current state to see if it was pressed or released.
        for i in range(len(links)):
            # Each pin is represented by a bit in the touched value.  A value of 1
            # means the pin is being touched, and 0 means it is not being touched.
            pin_bit = 1 << i
            # First check if transitioned from not touched to touched.
            if current_touched & pin_bit and not last_touched & pin_bit:
                print('{0} touched!'.format(i))
                links[i].main()
            # Next check if transitioned from touched to not touched.
            if not current_touched & pin_bit and last_touched & pin_bit:
                print('{0} released!'.format(i))
        # Update last state and wait a short period before repeating.
        last_touched = current_touched
        if cap.is_touched(6):
            pygame.quit()
        '''EVENTS'''
        for event in pygame.event.get():
            if event.type == QUIT:
                print 'END'
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if clicked(x,y,exit):
                    pygame.quit()
                else:    
                    for i in range(len(buttons)):
                        if clicked(x,y,buttons[i]):
                            links[i].main()

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
                songs = pygame.Rect((buttonspace+buttonwidth)*3+buttonindent,buttony,buttonwidth,buttonheight)
                gamecontrol = pygame.Rect((buttonspace+buttonwidth)*4+buttonindent,buttony,buttonwidth,buttonheight)
                keyboard = pygame.Rect((buttonspace+buttonwidth)*5+buttonindent,buttony,buttonwidth,buttonheight)
                other = pygame.Rect((buttonspace+buttonwidth)*6+buttonindent,buttony,buttonwidth,buttonheight)
                exit = pygame.Rect((buttonspace+buttonwidth)*7+buttonindent,buttony,buttonwidth,buttonheight)
                
                buttons = [detect,learn,compose,songs,gamecontrol,keyboard,other,exit]
                for x in range(len(buttons)):
                    buttons[x].height -= keylen[x]

        pygame.display.update()
        t.tick(30)

if __name__ == '__main__':
    main()
