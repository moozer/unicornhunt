# unicorn hunt
import pygame
from pygame.locals import *

from gameField import gameField, point
from chatRoom import chatRoom



if __name__ == "__main__":
    pygame.init()
    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()

    tilesGeo =  point( 31, 22 )
    screenSize = point( 1200, 700 )
    gfOffset = point( 0,0 )
    crSize = point( 200, 700 )
    crOffset = point( 1000, 0 )

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('game field test program')

    # --- chat room part -------
    cr = chatRoom( crSize )
    cr.addMessage( "maiden", "Come to me" )
    cr.addComment( "Unicorn", "eats grass" )
    cr.addMessage( "Badguy", "Hahahaha!" )
    # --- chat room part -------

    def dprint( str ):
        cr.addMessage( "system", str )

    # --- game field part -------
    gf = gameField( tilesGeo, debugprint=dprint )
    # --- game field part -------


    # Blit everything to the screen
    screen.blit( gf.screen, gfOffset )
    pygame.display.flip()

    # Event loop
    quitLoop = False
    while not quitLoop:
        for event in pygame.event.get():
            if event.type == QUIT:
                quitLoop = True

        screen.blit(gf.screen, gfOffset)
        screen.blit(cr.screen, crOffset)
        pygame.display.flip()


