from pynput.keyboard import Controller,Key
import kmodule
import time
import pygame
from pygame.locals import *
pygame.init()

#firstline = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i'}
#secondline = {0:'j',1:'k',2:'l',3:'m',4:'n',5:'o',6:'p',7:'q'8:'r'}
#thirdline = {0:'s',1:'t',2:'u',3:'v',4:'w',5:'x',6:'y',7:'z',8:'0'}
#fourthline = {0:'1',1:'2',2:'3:4:5:6:7:8:}
def main():
    firstline  =['a','b','c','d','e','f','g','h','i']
    secondline =['j','k','l','m','n','o','p','q','r']
    thirdline  =['s','t','u','v','w','x','y','z','0']
    fourthline =['1','2','3','4','5','6','7','8','9']
    fifthline  =[Key.space,Key.enter,Key.backspace,Key.caps_lock,Key.tab,Key.left,Key.up,Key.down,Key.right,Key.esc]
    fifthline_words = ['[]','Enter','Delete','Caps','Tab','Left','Up','Down','Right']

    lines = [firstline,secondline,thirdline,fourthline,fifthline]
    characters = [firstline,secondline,thirdline,fourthline,fifthline_words]
    keyboard = Controller()
    boardnumber = 0
    currentline = lines[boardnumber]

    t = pygame.time.Clock()
    screen = pygame.display.set_mode((1000,150))
    while True:
        screen.fill((30,30,30))
        for x in range(len(characters[boardnumber])):
            kmodule.drawbutton(pygame.rect.Rect(100*x+20,50,50,40),False,characters[boardnumber][x])
        keys = kmodule.constdetect()
        if keys != '':
            if keys == 10:
                boardnumber += 1
                if boardnumber > len(lines)-1:
                    boardnumber = 0
                currentline = lines[boardnumber]
                print 'Switched!'
                #time.sleep(0.3)
            else:
                keyboard.press(currentline[keys-1])
                print currentline[keys-1]
        else:
            for x in currentline:
                keyboard.release(x)

        for event in pygame.event.get():
            if event.type == QUIT:
                execfile(Mainmenu.py)
        pygame.display.update()
        t.tick(10)
if __name__ == '__main__':
    main()

