import kmodule
import pygame
from pygame.locals import *
pygame.init()
'''kmodule.writeinit()
ticker = pygame.time.Clock()
presses = ''
kmodule.writetitle(i)
while True:
    kmodule.renderblocks_write(presses)
    presses = kmodule.detect()
    for event in pygame.event.get():
        if event.type == QUIT:
            kmodule.save()
            kmodule.terminate()
        if event == KEYDOWN:
            for i in range(48,58):
                if event.key == i:
                    presses = i-48
        if event.type == VIDEORESIZE:
            kmodule.screenw = event.w
            kmodule.screenh = event.h
            kmodule.screen = pygame.display.set_mode((event.w,event.h),RESIZABLE)
    ticker.tick(30)'''
def main():
    kmodule.main(True)

if __name__ == '__main__':
    main()
