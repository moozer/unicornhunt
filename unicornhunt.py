# unicorn hunt
import pygame
from pygame.locals import *

from uhsupport import *
from gameField import gameField, point
from chatRoom import chatRoom



if __name__ == "__main__":
    pygame.init()
#    FPS = 30 # frames per second setting
#    fpsClock = pygame.time.Clock()

    tilesGeo =  point( 31, 21 )
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
#    cr.addMessage( "maiden", "Come to me" )
#    cr.addComment( "Unicorn", "eats grass" )
#    cr.addMessage( "Badguy", "Hahahaha!" )
    # --- chat room part -------

    def dprint( str ):
        cr.addMessage( "system", str )

    # --- game field part -------
    gf = gameField( tilesGeo, debugprint=dprint )
    # --- game field part -------

    # --- units part -------
    unicorn = unit( unitList['unicorn'], gf, point(0,0) )
    cr.addMessage( "system", "Unicorn at %s"%( unicorn.pos, ) )
    badguy = unit( unitList['badguy'], gf, point(10,10) )
    cr.addMessage( "system", "Badguy at %s"%( badguy.pos, ) )
    maiden = unit( unitList['maiden'], gf, point(20,20) )
    cr.addMessage( "system", "maiden at %s"%( maiden.pos, ) )
    # --- units part -------


    # Blit everything to the screen
    screen.blit( gf.screen, gfOffset )
    screen.blit(cr.screen, crOffset)
    pygame.display.flip()

    # Event loop
    quitLoop = False
    while not quitLoop:
        refresh = False
        for event in pygame.event.get():
            if event.type == QUIT:
                quitLoop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    badguy.moveLeft()
                if event.key == pygame.K_RIGHT:
                    badguy.moveRight()
                if event.key == pygame.K_DOWN:
                    badguy.moveDown()
                if event.key == pygame.K_UP:
                    badguy.moveUp()

        if gf.dirty:
            print "gf update"
            gf.update( screen, gfOffset)
            for unit in [unicorn, maiden, badguy]:
                print "%s update"%(unit.name, )
                unit.update( screen, gfOffset)
            refresh = True
            
        if cr.dirty:
            print "cr update"
            cr.update( screen, crOffset)
            refresh = True

        if refresh:
            print "refreshing"
            pygame.display.flip()
            refresh = False


