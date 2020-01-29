import pygame
from pygame.locals import *
import random
import kmodule
pygame.init()



balldirx = random.choice((-10,10))
balldiry = random.randint(-10,10)
ball = pygame.rect.Rect(300,200,20,20)
ballshadow = []
leftscore = 0
rightscore = 0

leftpaddle = pygame.rect.Rect(50,175,15,50)
rightpaddle = pygame.rect.Rect(550,175,15,50)
t = pygame.time.Clock()
def main():
    screen = pygame.display.set_mode((600,400))
    pygame.display.set_caption('Pong')    
    global ball,balldirx,balldiry,leftscore,rightscore,t, wallbounce, rebounce, detectscore, detectwin, moveball,leftpaddle,rightpaddle,ballshadow,screen
    leftdir = ''
    rightdir = ''
    pongfont = pygame.font.Font(None,50)

    screen.fill((20,20,20))
    screen.blit(pongfont.render('Pong - Press a key to start',1,(255,255,255)),(50,100))
    pygame.display.flip()
    start = False
    while True:
        if kmodule.detect() != '':
            break
        for event in pygame.event.get():
            if event.type == KEYUP:
                start = True
        if start:
            break

    while True:
        screen.fill((20,20,20))
        balldiry = wallbounce(ball,balldiry)
        balldirx, balldiry = rebounce(ball,leftpaddle,balldirx, balldiry)
        balldirx, balldiry = rebounce(ball,rightpaddle,balldirx, balldiry)
        
        ballshadow.append(ball)
        #if len(ballshadow) > 2000:
        #    ballshadow.pop(0)
        for x in ballshadow:
            pygame.draw.rect(screen, (50,50,50), x)

        ball = moveball(ball,balldirx,balldiry)
        rightscore,leftscore = detectscore(ball,rightscore,leftscore)
        pygame.draw.rect(screen, (255,255,255), ball)
        pygame.draw.rect(screen, (255,255,255), leftpaddle)
        pygame.draw.rect(screen, (255,255,255), rightpaddle)
        
        scr = pongfont.render(str(leftscore),1,(255,255,255))
        screen.blit(scr,(220,50))
        scr = pongfont.render(str(rightscore),1,(255,255,255))
        screen.blit(scr,(350,50))
        
        presses = kmodule.constdetect()
        if presses != '':
            if presses == 1 and leftpaddle.y > 0:
                leftdir = 'up'
            elif presses == 2 and leftpaddle.y < 350:
                leftdir = 'down'
            elif presses == 9 and rightpaddle.y > 0:
                rightdir = 'up'
            elif presses == 10 and rightpaddle.y < 350:
                rightdir = 'down'
        else:
            leftdir = ''
            rightdir = ''

        if leftdir == 'up' and leftpaddle.y > 0:
            leftpaddle.y -=20
        elif leftdir == 'down' and leftpaddle.y < 350:
            leftpaddle.y += 20
        elif rightdir == 'up' and rightpaddle.y > 0:
            rightpaddle.y -= 20
        elif rightdir == 'down' and rightpaddle.y < 350:
            rightpaddle.y += 20

        leftscore,rightscore = detectwin(leftscore,rightscore,pongfont)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_w and leftpaddle.y > 0:
                    leftdir = 'up'
                elif event.key == K_s and leftpaddle.y < 350:
                    leftdir = 'down' 
                elif event.key == K_UP and rightpaddle.y > 0:
                    rightdir = 'up'
                elif event.key == K_DOWN and rightpaddle.y < 350:
                    rightdir = 'down'
            elif event.type == KEYUP:
                leftdir = ''
                rightdir = ''
            elif event.type == QUIT:
                return
        t.tick(20)
        pygame.display.flip()

def wallbounce(ball,balldiry):
    if ball.y < 0 or ball.y > 400:
        return balldiry*-1
    else:
        return balldiry

def rebounce(ball, paddle, balldirx, balldiry):
    if ball.colliderect(paddle):
        balldiry = (ball.centery - paddle.centery)*0.8
        balldirx *= -1
    return balldirx,balldiry

def detectscore(ball,rightscore,leftscore):
    if ball.x > 600:
        leftscore += 1
        ball.x = 300
        ball.y = 200
        balldirx = random.choice((-10,10))
        balldiry = random.randint(-10,10)
    if ball.x < 0:
        rightscore += 1
        ball.x = 300
        ball.y = 200
        balldirx = random.choice((-10,10))
        balldiry = random.randint(-10,10)

    return rightscore,leftscore
def detectwin(leftscore,rightscore,font):
    if leftscore > 10 or rightscore > 10:
        if leftscore > 10:
            wintext = font.render('Left Wins!',1,(255,255,255))
        elif rightscore > 10:
            wintext = font.render('Right Wins!',1,(255,255,255))
        screen.blit(wintext,(250,150))
        pygame.display.flip()
        restart = False
        leftscore = 0
        rightscore = 0
        while True:
            if kmodule.detect() == 5:
                return leftscore,rightscore
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return leftscore,rightscore
                elif event.type == QUIT:
                    pygame.quit()
    else:
        return leftscore,rightscore
def moveball(ball,balldirx,balldiry):
    ball.x += balldirx
    ball.y += balldiry
    return ball

if __name__ == '__main__':
    main()

