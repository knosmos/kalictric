'''import os
from multiprocessing import Pool

processes = ('minecraft-pi','python Quit.py')

def run_process(process):
        os.system(process)

pool = Pool(processes = 3)
pool.map(run_process,processes)
'''
from pynput.keyboard import Key, Controller, KeyCode
import Adafruit_MPR121.MPR121 as sensor
import time
import kmodule
import pygame 
from pygame.locals import *

mapping = {0:'a',1:'w',2:'s',3:'d',4:Key.space,6:Key.left,7:Key.up,8:Key.down,9:Key.right}
mapping = {0:'a',1:'w',2:'s',3:'d',4:Key.space,5:Key.shift,6:'e',7:Key.esc,8:Key.down,9:Key.right}
#mapping = {0:'a',1:'w',2:'s',3:'d',4:Key.space,5:'c',6:Key.left,7:Key.up,8:Key.down,9:Key.right,10:'c',11:'c'}

mapping = {0:'a',1:'w',2:'s',3:'d',5:Key.space,4:Key.shift,6:'e',7:Key.esc,8:Key.down,9:Key.right}
keyboard = Controller()
cap = sensor.MPR121()
if not cap.begin():
    print '???'

pygame.init()

'''gamepad_image = pygame.transform.scale(pygame.image.load('gamepadgui.png'),(800,230))'''
screen = pygame.display.set_mode((300,80))
t = pygame.time.Clock()

last_touched = cap.touched()
'''def detect():
    global cap
    global last_touched
    whattouched = ''
    current_touched = cap.touched()
    for i in range(12):
        pin_bit = i << 1
        if current_touched & pin_bit and not last_touched & pin_bit:
            print i
            whattouched = i
    return whattouched
    ''if current_touched & pin_bit:
        return i
    else:
        return ''
    last_touched = current_touched
    #time.sleep(0.1)'''

def main():
    global last_touched
    while True:
        whattouched = ''
        current_touched = cap.touched()
        kmodule.drawbutton(pygame.rect.Rect(10,10,50,20),True,'Minecraft Controller')
        for i in range(12):
            pin_bit = 1 << i
            if current_touched & pin_bit and not last_touched & pin_bit:
                print('{0} touched!'.format(i))
                if i in mapping:
                    keyboard.press(mapping[i])
            if not current_touched & pin_bit and last_touched & pin_bit:
                print('{0} released!'.format(i))
                keyboard.release(mapping[i])
        last_touched = current_touched
        
        #screen.blit(gamepad_image, (0,0))
        #keyboard.press(Key.space)
        #keyboard.release(Key.space)
        #screen.blit(gamepad_image,(0,0))
        '''detection_results = kmodule.constdetect()
        #print detection_results
        if detection_results != '':
            #try:
            if detection_results-1 in mapping:
                keyboard.press(mapping[detection_results-1])
                #keyboard.release(mapping[detection_results])
                print mapping[detection_results-1]
                #except:
                #pass
        else:
            for i in mapping:
                keyboard.release(mapping[i])'''

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        pygame.display.flip()
        t.tick(20)
        time.sleep(0.1)

if __name__ == '__main__':
    main()
