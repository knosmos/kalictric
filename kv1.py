#Kalictric modules for detection, graphics and MIDI processing.

screenw = 800
screenh = 600

import sys
import os
'''SENSOR LIBRARY'''
import Adafruit_MPR121.MPR121 as sensor
cap = sensor.MPR121()
if not cap.begin():
    print 'initialization error'
    sys.exit(1)

'''MIDI LIBRARY'''
import mido
from mido import MidiFile, MidiTrack, Message
'''GRAPHICS'''
import pygame
from pygame.locals import *
'''WAITING'''
import time
'''THREADING (READ MODULE)'''
from threading import Thread
#pygame.init()
screen = pygame.display.set_mode((screenw,screenh),pygame.RESIZABLE)
pygame.display.set_caption('kmodule')
notes = [] #RECT objects representing notes currently on-screen
keys = [] #notes currently on-screen
msgs = [] #MIDI messages whose notes are on-screen
sentnotes = [] #RECT objects from Composition
score = 0 #Scorekeeper for song teacher
playsong = 'test.mid' #Song to play
def loadfiles(filename):
    listname = []
    with open(filename, 'rU') as f:
        for line in f:
            listname.append(line.rstrip())
    return listname
songs = loadfiles('songs.txt')
mapping = {60:5,62:6,64:4,65:7,67:3,69:8,71:2,72:9,74:1,76:10} #mapping of keyboard to kalimba keys

streak = 0
highstreak = 0
misses = 0
scoremsgs = []
scoremsgy = []
ctr = 0
flashticker = 0
prevNote = ''
gameover = False 
wait = False #PAUSE FOR WHEN NOTE DROPS TOO FAR
#mapping = {:1,:2,:3,:4,60:5,:6,:7,:8,:9,:10}
notespeed = 5 #speed at which notes fall/rise
'''FIRE UP TiMIDIty++'''
'''def starttimidity():
    os.system('timidity -iAqq')

def startstarttimidity():
    timiditythread = Thread(target = starttimidity)
    timiditythread.daemon = True
    timiditythread.start()

startstarttimidity()'''

mido.set_backend('mido.backends.pygame')
port = mido.open_output(mido.get_output_names()[1])
pygame.init()

'''TITLESCREENS'''
def readtitle():
    global screenw,screenh,screen
    while True:
        screen.fill((0,0,0))
        titlefont = pygame.font.Font(None,300)
        normalfont = pygame.font.Font(None,100)
        screen.blit(titlefont.render('Learn',1,(100,100,100)),(screenw*0.1+20,screenh*0.25+20))
        screen.blit(titlefont.render('Learn',1,(100,255,100)),(screenw*0.1,screenh*0.25))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                break
            if event.type == VIDEORESIZE:
                screenw = event.w
                screenh = event.h
                screen = pygame.display.set_mode((screenw,screenh),RESIZABLE)
        if detect() != '':
            break

        time.sleep(0.01)


def writetitle():
    global screenw,screenh,screen
    while True:
        screen.fill((0,0,0))
        titlefont = pygame.font.Font(None,200)
        normalfont = pygame.font.Font(None,100)
        screen.blit(titlefont.render('Compose',1,(50,50,50)),(screenw*0.1+20,screenh*0.25+20))
        screen.blit(titlefont.render('Compose',1,(100,100,255)),(screenw*0.1,screenh*0.25))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                break
            if event.type == VIDEORESIZE:
                screenw = event.w
                screenh = event.h
                screen = pygame.display.set_mode((screenw,screenh),RESIZABLE)
        if detect() != '':
            break

        time.sleep(0.01)


'''THE SENSOR STUFF'''
last_touched = cap.touched()
def constdetect():
    whattouched = ''
    for i in range(12):
        pin_bit = 1 << i
        if cap.touched() & pin_bit:
            whattouched = i+1
    return whattouched
last_touched = cap.touched()
def detect():
    global last_touched
    whattouched = ''
    current_touched = cap.touched()
    # Check each pin's last and current state to see if it was pressed or released.
    for i in range(12):
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
        pin_bit = 1 << i
        # First check if transitioned from not touched to touched.
        if current_touched & pin_bit and not last_touched & pin_bit:
            print('{0} touched!'.format(i))
            whattouched = i+1
            #touched.append(i)
        # Next check if transitioned from touched to not touched.
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))
            #touched.remove(i)
    # Update last state and wait a short period before repeating.
    last_touched = current_touched 
    return whattouched


'''THE GRAPHICS STUFF'''
def renderblocks_read(presses = ''): #song-teacher
   myfont = pygame.font.Font(None, 30)
   scorefont = pygame.font.Font(None, 100)
   global msgs,notes,notespeed,keys,song,port,score,screenw,screenh,streak,highstreak,misses,scoremsgs,scoremsgy,gameover,flashticker,wait

   screen.fill((0,0,0))
   greenspace = pygame.rect.Rect(0,screenh*0.6,screenw,screenh/6)
   #switch = pygame.rect.Rect(screenw-100,50,40,200)
   if flashticker > 0:
       greencolor = (255,255,255)
       flashticker -= 1
   else:
       greencolor = (100,255,100)
   pygame.draw.rect(screen, greencolor, greenspace)
   #rawbutton(switch,False,'Switch Song')
   #draw the bars for the notes
   keylen = [70,55,40,25,10,25,40,55,70,85]
   for key in range(10):
       pygame.draw.rect(screen, (100,100,100), ((key+1)*screenw*0.075+50, 0, screenw/40, screenh-keylen[key]))
       p = myfont.render(str(key+1),1,(200,200,255))
       screen.blit(p,((key+1)*screenw*0.075+50,screenh*0.75))
   '''for key in keys:
       notes.append(pygame.rect.Rect(mapping[key+12]*60+50, 20, 20, 20))'''
   p = myfont.render('score: ' + str(score),1,(255,255,255))
   screen.blit(p,(30,30))
   #draw the note-blocks
   if len(notes) > 0:

        for note in notes:
           #print notes
           if note == notes[0]:
               color = (255,100,100)
           else:
               color = (255,255,255)
           pygame.draw.circle(screen, color, note.center,screenw/60)
           note.y+=notespeed
           '''if note.y >= 550:
           notes.remove(note)'''
           #if someone misses a note ...
           if note.y > greenspace.bottom:
               '''song = ''
               notes = []
               msgs = []
               keys = []
               ''screen.fill((255,255,255))
               pygame.display.update()
               time.sleep(0.5)''
               time.sleep(0.5)
               song = playsong
               score = 0'''
               '''port.close()
               exitloop = False
               while True:
                   if exitloop:
                       break
                   for event in pygame.event.get():
                       if event.type == MOUSEBUTTONUP:
                           exitloop = True
               execfile('kmodule.py')'''
               #screen.fill((250,100,100))
               scoremsgs.append('MISSED!')
               scoremsgy.append(200)
               #notes.pop(0)
               misses += 1
               wait = True

               #port.send(Message('note_on',note = 60))
               #port.send(Message('note_off',note = 60))
               #msgs.pop(0)
               streak = 0
               while detect() != (notes[0].x-50)/60:
                    time.sleep(0.001)
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                        elif event.type == KEYDOWN:
                            if event.key == (notes[0].x-50)/60 + 48:
                                break
               msgs[0].note += 2
               port.send(msgs[0])
               offmsg = Message('note_off',note = msgs[0].note)
               port.send(offmsg)   
               notes.pop(0)
               msgs.pop(0)
               wait = False
        #detection handling
        if presses != '':
           #if presses == 0:
           #   presses = 10
           if presses == (notes[0].x-50)/60 and greenspace.collidepoint(0,notes[0].y):
               print (notes[0].x-50)/60
               notes.pop(0)
               streak += 1
               if streak > highstreak:
                   highstreak = streak
               scoremsgs.append('+' + str(streak*10))
               scoremsgy.append(200)
               #port.send(msgs[0])
               msgs[0].note += 2
               port.send(msgs[0])
               offmsg = Message('note_off',note = msgs[0].note)
               port.send(offmsg)
               msgs.pop(0)
               #msgs.pop(1)
               score += streak*10
               flashticker = streak*2
           elif presses == 11:
               song = switchsong()
   if len(notes) == 0 and gameover == 1:
        gameover = 2      
        print 'end'            

        '''else:
           #print 'wrong!'
           pass'''
   for x in range(len(scoremsgs)):
       if scoremsgy[x] > 50:
            screen.blit(scorefont.render(scoremsgs[x],1,(150,255,150)),(200,scoremsgy[x]))
   '''if len(scoremsgs) > 0:
        for x in range(len(scoremsgs)):     
            if scoremsgy[x] < -50:
                scoremsgs.pop(x)
                scoremsgy.pop(x)'''
   for y in range(len(scoremsgy)):
        scoremsgy[y] -= 5
        #print scoremsgy[y]
   global ctr
   if ctr > 100: #scoremsgy[:-1] < 50:
        scoremsgs = []
        scoremsgy = []
        print 'erased'
        ctr = 0
   ctr += 1
   '''if score < 0:
      port.close()
      exitloop = False
      while True:
         if exitloop:
            break
         for event in pygame.event.et():
            if event.type == MOUSEBUTTONUP:
               exitloop = True
            elif event.type == QUIT:
               pygame.quit()

      execfile('kmodule.py')'''
 
   pygame.display.update()




'''THE STUFF THAT READS MIDI FILES'''
def read():
   global keys
   global song
   global notes
   global mapping
   global msgs
   global notespeed
   global port
   global score,gameover
   global wait
   tck = pygame.time.Clock()
   #while True:
   if song != '':
       for msg in MidiFile(song):
           time.sleep(msg.time*4)
           if not msg.is_meta:
               #port.send(msg)
               #msg.note += 2 #Convert to D Major.
               if msg.type == 'note_on':
                   #print msg.note
                   #msg.note += 2
                   msgs.append(msg)
                   keys.append(msg.note+12)
                   notes.append(pygame.rect.Rect(mapping[msg.note]*screenw*0.075+50, 0, screenw*0.025, screenh*0.033))
               if msg.type == 'note_off':
                   keys.remove(msg.note+12)
                   #msgs.append(msg)
           if gameover == 2:
               break
           while wait:
               time.sleep(0.01)

           if song == '':
               break
               print 'broken'

   gameover = 1
        #tck.tick(10)   


def simpleread(song):
   def play(song):
      while True:
         for msg in MidiFile(song):
            time.sleep(msg.time)
            if not msg.is_meta:
               port.send(msg)
   playthread = Thread(target = play(song))
   playthread.daemon = True
   playthread.start()

'''SWITCHING SONGS'''
def switchsong():
    global songs
    songrects = []
    t = pygame.time.Clock()
    ctr = 1
    for song in songs:
        songrects.append(pygame.rect.Rect(20,ctr*40,100,30))
        ctr += 1
    while True:
        x,y = pygame.mouse.get_pos()
        screen.fill((0,0,0))
        for i in range(len(songrects)):
            if clicked(x,y,songrects[i]):
                drawbutton(songrects[i],True,songs[i])
            else:
                drawbutton(songrects[i],False,songs[i])
        pressed = detect()
        if pressed != '':
            print songs[pressed]
            return songs[pressed]
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                for i in range(len(songrects)):
                    if clicked(x,y,songrects[i-1]):
                        print songs[i-1]
                        return songs[i-1]
                        print songs[i-1]
                      
            elif event.type == QUIT:
                pygame.quit()
        pygame.display.flip()
        t.tick(20)

'''SHOWING FINAL SCORE'''
def finalScore():
    global score,highstreak,misses,port
    print 'final scores'
    screen.fill((30,30,30))
    f = pygame.font.Font(None,50)
    words = f.render('FINAL STANDINGS ',1,(255,100,100))
    screen.blit(words,(50,50))
    showscore = f.render('SCORE -> ' + str(score),1,(255,255,255))
    screen.blit(showscore,(60,100))
    showstreak = f.render('STREAK -> ' + str(highstreak),1,(255,255,255))
    screen.blit(showstreak,(60,150))
    showmisses = f.render('MISSES -> ' + str(misses),1,(255,255,255))
    screen.blit(showmisses,(60,200))
    pygame.display.update()
    port.close()
    #time.sleep(1)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        if detect() == 5:
            execfile('kmodule.py')
        elif detect() == 1:
            execfile('Home.py')

        
'''BUTTON MANAGEMENT'''
def drawbutton(RECT,newcolor,text):
    myfont = pygame.font.Font(None, 40)
    buttoncolor = (100,100,255)
    newbuttoncolor = (100,255,100)
    if newcolor:
        pygame.draw.rect(screen,newbuttoncolor,RECT)
    else:
        pygame.draw.rect(screen,buttoncolor,RECT)
    p = myfont.render(text,1,(250,250,250))
    screen.blit(p,(RECT.left, RECT.top - 2))
def clicked(x,y,RECT):
    if RECT.collidepoint(x,y) == True:
        return True
    else:
        return False
        

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''GRAPHICS FOR COMPOSITION'''
def renderblocks_write(presses = ''):
   myfont = pygame.font.Font(None, 30)
   global port
   global sentnotes
   global prevNote
   global ctr
   screen.fill((0,0,0))
   bluespace = pygame.rect.Rect(0,screenh-screenh/8,screenw,screenh/6)
   pygame.draw.rect(screen, (100,100,255), bluespace)
   keylen = [50,40,30,20,10,20,30,40,50,60]
   for key in range(10):
       pygame.draw.rect(screen, (100,100,100), ((key+1)*screenw*0.075, 0, screenw*0.025, screenh-keylen[key]))
       p = myfont.render(str(key+1),1,(200,200,255))
       screen.blit(p,((key+1)*screenw*0.075,screenh*0.75))
   for note in sentnotes:
       pygame.draw.circle(screen, (255,255,255), note.center, screenw/60)
       note.y-=5

   ctr += 2
   if presses != '':
       if presses == 0:
           presses = 10
       #write(mapping.keys()[mapping.values().index(presses)])
       if prevNote != '':
           write(prevNote,ctr)
           print ctr
           ctr = 0
           print ctr
       sentnotes.append(pygame.rect.Rect(presses*screenw*0.075, screenh, screenw*0.025, screenh*0.033))
       print presses
       prevNote = mapping.keys()[mapping.values().index(presses)]
       port.send(Message('note_on', note = mapping.keys()[mapping.values().index(presses)]+2, velocity = 100, time = 50))
       port.send(Message('note_off', note = mapping.keys()[mapping.values().index(presses)]+2, velocity = 100, time = 32))
   pygame.display.update()


'''THE COMPOSITION INITIALIZATION STUFF'''
def writeinit():
   global mid
   global track
   mid = MidiFile()
   track = MidiTrack()
   mid.tracks.append(track)


'''THE COMPOSITION STUFF'''
def write(key,waittime):
   global track
   track.append(Message('note_on', note = key, velocity = 100, time = 200))
   track.append(Message('note_off', note = key, velocity = 100, time = waittime))


'''THE STUFF THAT SAVES MIDI FILES'''
def rendersave():
   global screen
   name = ''
   namefont = pygame.font.Font(None,70)
   t = pygame.time.Clock()
   while True:
      screen.fill((255,255,255))
      text = namefont.render(name,1,(0,0,0))
      screen.blit(text,(50,20))
      for event in pygame.event.get():
         if event.type == KEYUP:
            if event.key == K_RETURN: #Enter |
               print 'name captured'
               return name
            elif event.key == K_BACKSPACE: #Backspace [
               name = name[:-1]
               print 'deleted'
            else:
               name = name + chr(event.key)
      t.tick(25)
      pygame.display.flip()

def save():
    global mid
    global songs

    savefile = open('songs.txt','a')
    name = rendersave()
    if name != 'nosave':
        mid.save(name)
        if not name in songs:
            savefile.write(name+'\r\n')
    savefile.close()
    print 'save successful'

'''Terminate the program'''
def terminate():
    global port
    port.close()
    pygame.quit()
    sys.exit()

'''Create threads
def createthread(target):
    t = Thread(target = target)
    t.daemon = True
    t.start()'''

''' THE STUFF THAT RUNS IF THIS PROGRAM LAUNCHES AS __main__'''
def main(mode = False):
   global keys
   global screenw
   global screenh
   global song
   global gameover
   global score

   if not mode:
       readtitle()
       song = switchsong()
   else:
       writetitle()
   if not mode:
       #createthread(read)
       t = Thread(target = read)
       t.daemon = True
       t.start()
   else:
       writeinit()
   presses = ''
   ticker = pygame.time.Clock()
   while True: 
       if not mode:
           renderblocks_read(presses)
       else:
           renderblocks_write(presses)
       if gameover == 2:
           finalScore()
           print'ender'
           break
       presses = detect()           
       for event in pygame.event.get():
           if event.type == QUIT:
               if mode: 
                   #name = raw_input('name>')
                   #if name != 'nosave':
                   #    save(name)
                   save()
               terminate()
               print 'GOOD-BYE'
           if event.type  == KEYDOWN:
               for i in range(48,58):
                   if event.key == i:
                       presses = i-48
                       if presses == 0:
                           presses = 10
           if event.type == VIDEORESIZE:
               screenw = event.w
               screenh = event.h
               pygame.display.set_mode((screenw,screenh),RESIZABLE)
       ticker.tick(30)
   finalScore()
if __name__ == '__main__':
   main()
   
