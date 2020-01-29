import kmodule
from mido import Message
import pygame
import time
import pygame.midi
from pygame.locals import *
pygame.midi.init()
player = pygame.midi.Output(3)
pygame.init()
kmodule.screen = pygame.display.set_mode((800,600))

playnotes = []
keybrightness = 100
def renderblocks_play():
    myfont = pygame.font.Font(None, 30)
    global keybrightness
    kmodule.screen.fill((0,0,0))
    bluespace = pygame.rect.Rect(0,kmodule.screenh*0.5,kmodule.screenw,kmodule.screenh/7)
    if keybrightness > 100:
        keybrightness -= 10
    pygame.draw.rect(kmodule.screen, (255,keybrightness,keybrightness), bluespace)
    keylen = [100,80,60,40,20,40,60,80,100,120]
    for key in range(10):
        pygame.draw.rect(kmodule.screen, (100,100,100), ((key+1)*kmodule.screenw*0.075+50, 0, kmodule.screenw*0.025, kmodule.screenh-keylen[key]))
        p = myfont.render(str(key+1),1,(200,200,255))
        kmodule.screen.blit(p,((key+1)*kmodule.screenw*0.075+50,kmodule.screenh*0.75))
    for note in kmodule.notes:
        pygame.draw.circle(kmodule.screen, (255,255,255), note.center, kmodule.screenw/60)
        note.y+=3
        if note.y > kmodule.screenh*0.5:
            kmodule.notes.remove(note)
            #kmodule.port.send(kmodule.msgs[0])
            #kmodule.msgs[0].type == 'note_off'
            #kmodule.port.send(kmodule.msgs[0])
            kmodule.msgs.pop(0)
    detect = kmodule.detect()
    if detect != '':
        keybrightness = 255
        #player.note_on(64, 127)
        #time.sleep(0.25)
        #player.note_off(64);
        kmodule.port.send(Message('note_on',note = kmodule.mapping.keys()[kmodule.mapping.values().index(detect)],time = 10))
        kmodule.port.send(Message('note_off',note = kmodule.mapping.keys()[kmodule.mapping.values().index(detect)],time = 10))
    pygame.display.flip()

kmodule.song = kmodule.switchsong()
from threading import Thread
play = Thread(target = kmodule.read)
play.daemon = True
play.start()
while True:
    renderblocks_play()
    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            kmodule.screenh = event.h
            kmodule.screenw = event.w
            screen = pygame.display.set_mode((event.w,event.h),RESIZABLE)
        elif event.type == QUIT:
            pygame.quit()
