#Lines (A Tron Clone)
#Created by Jieruei Chang
import pygame
import kmodule
from pygame.locals import *
pygame.init()

greenline = []
greendirection = 'right'
greenx = 100
greeny = 250

blueline = []
bluedirection = 'left'
bluex = 400
bluey = 250


t = pygame.time.Clock()

def main():
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('Lines')    
    global screen,greenline,greendirection,greenx,greeny, blueline,bluedirection,bluex,bluey, move, isValidTurn, detectCollision
    while True:
        screen.fill((0,0,0))
        greenx,greeny = move(greenline,greendirection,greenx,greeny)
        bluex,bluey = move(blueline,bluedirection,bluex,bluey)
        for piece in greenline:
            pygame.draw.rect(screen,(100,255,100),piece)
    
        for piece in blueline:
            pygame.draw.rect(screen,(100,100,255),piece)
        
        if detectCollision(greenline,blueline) or detectCollision(blueline,greenline):
            if detectCollision(greenline,blueline) and detectCollision(blueline,greenline):
                myfont = pygame.font.Font(None,40)
                screen.blit(myfont.render('TIE!',1,(255,255,255)),(100,100))
            else:
                if detectCollision(greenline,blueline) == True:
                    kmodule.drawbutton(pygame.rect.Rect(100,100,300,100),False,'BLUE WINS!')
                if detectCollision(blueline,greenline) == True:
                    kmodule.drawbutton(pygame.rect.Rect(100,100,300,100),True,'GREEN WINS!')
            greenline = []
            greendirection = 'right'
            greenx = 100
            greeny = 250

            blueline = []
            bluedirection = 'left'
            bluex = 400
            bluey = 250

            exitloop = False
            pygame.display.update()
            while True:
                if kmodule.detect() != '':
                    break
                for event in pygame.event.get():
                    if event.type == QUIT:
                        import Arcade
                        Arcade.main()
                    elif event.type == KEYDOWN:
                        exitloop = True
                if exitloop:
                    break

        detection = kmodule.detect()
        if detection == 2 and isValidTurn(greendirection,'up'):
            greendirection = 'up'
        if detection == 1 and isValidTurn(greendirection,'left'):
            greendirection = 'left'
        if detection == 3 and isValidTurn(greendirection,'down'):
            greendirection = 'down'
        if detection == 4 and isValidTurn(greendirection,'right'):
            greendirection = 'right'
        if detection == 7 and isValidTurn(bluedirection,'left'):
            bluedirection = 'left'
        if detection == 10 and isValidTurn(bluedirection,'right'):
            bluedirection = 'right'
        if detection == 8 and isValidTurn(bluedirection,'up'):
            bluedirection = 'up'
        if detection == 9 and isValidTurn(bluedirection, 'down'):
            bluedirection = 'down'        

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_w and isValidTurn(greendirection,'up'):
                    greendirection = 'up'
                if event.key == K_a and isValidTurn(greendirection,'left'):
                    greendirection = 'left'
                if event.key == K_s and isValidTurn(greendirection,'down'):
                    greendirection = 'down'
                if event.key == K_d and isValidTurn(greendirection,'right'):
                    greendirection = 'right'
                if event.key == K_LEFT and isValidTurn(bluedirection,'left'):
                    bluedirection = 'left'
                if event.key == K_RIGHT and isValidTurn(bluedirection,'right'):
                    bluedirection = 'right'
                if event.key == K_UP and isValidTurn(bluedirection,'up'):
                    bluedirection = 'up'
                if event.key == K_DOWN and isValidTurn(bluedirection, 'down'):
                    bluedirection = 'down'
            elif event.type == QUIT:
                return

        pygame.display.flip()
        t.tick(10)


def move(line,direction,x,y):
    if direction == 'right':
        line.append(pygame.rect.Rect(x + 10,y,10,10))
        x+=10
        return x,y
    elif direction == 'left':
        line.append(pygame.rect.Rect(x - 10,y,10,10))
        x-=10
        return x,y
    elif direction == 'up':
        line.append(pygame.rect.Rect(x,y - 10,10,10))
        y-=10
        return x,y
    elif direction == 'down':
        line.append(pygame.rect.Rect(x,y + 10,10,10))
        y+=10
        return x,y

def isValidTurn(olddir,newdir):
    if (newdir == 'up' or newdir == 'down') and (olddir == 'right' or olddir == 'left'):
        return True
    elif (newdir == 'right' or newdir == 'left') and (olddir == 'up' or olddir == 'down'):
        return True
    else:
        return False

def detectCollision(firstline,secondline):
    for i in secondline:
        if firstline[-1] == i:
            print 'Hit other'
            return True
    head = firstline[-1]
    firstline.pop(-1)
    for i in firstline:
        if head == i:
            print 'Hit self'
            return True
    firstline.append(head)

    if firstline[-1].x > 500 or firstline[-1].x < 0 or firstline[-1].y > 500 or firstline[-1].y < 0:
        print 'Hit edge'
        return True
    
if __name__ == '__main__':
    main()
