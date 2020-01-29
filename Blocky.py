import pygame
import kmodule
from random import randint
from pygame.locals import *
pygame.init()

def main():
    global r1,r2,r3,screen
    t = pygame.time.Clock()
    r1 = [0,0,0]
    r2 = [0,0,0]
    r3 = [0,0,0]

    pygame.display.set_caption('512')
    screen = pygame.display.set_mode((600,600))
    def getNewPiece():
        global r1,r2,r3
        rows = [r1,r2,r3]
        while True:
            row = randint(0,2)
            col = randint(0,2)
            if rows[row][col] == 0:
                rows[row][col] = 2
                print r1,r2,r3
                return r1,r2,r3

    def drawSquares():
        global r1,r2,r3
        row = 0
        global screen
        screen.fill((0,0,0))
        colors = {0:(100,100,100),2:(200,200,200),4:(200,100,100),8:(255,200,0),16:(100,200,100),32:(200,0,100),64:(100,0,200),128:(100,100,255),256:(255,100,100),512:(0,0,0)}
        squarefont = pygame.font.Font(None,100)
        for x in [r1,r2,r3]:
            col = 0
            for y in x:
                color = colors[y]
                pygame.draw.rect(screen,color,((col*180)+20,(row*180)+20,140,140))
                screen.blit(squarefont.render(str(y),1,(255,255,255)),((col*180)+40,(row*180)+40))
                col += 1
            row += 1
        pygame.display.update()

    def moveUp():
        global r1,r2,r3
        possible = False
        for x in range(3):
            if r1[x] == 0: #Move one space up
                r1[x] = r2[x]
                r2[x] = 0
                possible = True
            elif r1[x] == r2[x]: #Merge
                r1[x] *= 2
                r2[x] = 0
                possible = True
            if r2[x] == 0:
                r2[x] = r3[x]
                r3[x] = 0
                possible = True
            elif r2[x] == r3[x]:
                r2[x] *= 2
                r3[x] = 0
                possible = True
        if possible:
            getNewPiece()
        return r1,r2,r3

    def moveDown():
        global r1,r2,r3
        possible = False
        for x in range(3):
            if r3[x] == 0: #Move one space down
                r3[x] = r2[x]
                r2[x] = 0
                possible = True
            elif r3[x] == r2[x]: #Merge
                r3[x] *= 2
                r2[x] = 0
                possible = True
            if r2[x] == 0:
                r2[x] = r1[x]
                r1[x] = 0
                possible = True
            elif r2[x] == r1[x]:
                r2[x] *= 2
                r1[x] = 0      
                possible = True
        if possible:
            getNewPiece()
        return r1,r2,r3

    def moveRight():
        global r1,r2,r3
        possible = False
        for x in [r1,r2,r3]:
            if x[2] == 0:
                x[2] = x[1]
                x[1] = 0
                possible = True
            elif x[1] == x[2]:
                x[2] *= 2
                x[1] = 0
                possible = True
            if x[1] == 0:
                x[1] = x[0]
                x[0] = 0
                possible = True
            elif x[0] == x[1]:
                x[1] *= 2
                x[0] = 0
                possible = True
        if possible:
            getNewPiece()

    def moveLeft():
        global r1,r2,r3
        possible = False
        for x in [r1,r2,r3]:
            if x[0] == 0:
                x[0] = x[1]
                x[1] = 0
                possible = True
            elif x[0] == x[1]:
                x[0] *= 2
                x[1] = 0
                possible = True
            if x[1] == 0:
                x[1] = x[2]
                x[2] = 0
                possible = True
            elif x[1] == x[2]:
                x[1] *= 2
                x[2] = 0       
                possible = True
        if possible:
            getNewPiece()

    t = pygame.time.Clock()
    while True:
        drawSquares()
        detect = kmodule.detect()
        if detect == 7:
            moveLeft()
        elif detect == 8:
            moveUp()
        elif detect == 9:
            moveDown()
        elif detect == 10:
            moveRight()
        elif detect == 1:
            main()
        elif detect == 3:
            import Arcade
            Arcade.main()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    for x in range(3):
                        moveUp()
                    #getNewPiece()
                elif event.key == K_DOWN:
                    for x in range(3):
                        moveDown()
                    #getNewPiece()
                elif event.key == K_RIGHT:
                    moveRight()
                    #getNewPiece()
                elif event.key == K_LEFT:
                    moveLeft()
                    #getNewPiece()
                elif event.key == K_r:
                    main()
            elif event.type == QUIT:
                import Arcade
                Arcade.main()
        t.tick(20)

if __name__ =='__main__':
    main()
