import pygame
import sys
from pygame.locals import *

def main():
    print 'Started shutdown...'
    pygame.quit()
    print 'Goodbye!'
    print '...For now'
    sys.exit()

if __name__ == '__main__':
    main()
