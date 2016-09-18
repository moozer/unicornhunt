# unicorn hunt
import pygame
from pygame.locals import *

import threading

from uhsupport import *
from gameField import gameField, point
from chatRoom import chatRoom
from actions import *
from units import *
from popup import *
from thrserver import *

class game():
    def __init__( self ):
        pygame.init()
    #    FPS = 30 # frames per second setting
    #    fpsClock = pygame.time.Clock()

        tilesGeo =  point( 31, 21 )
        screenSize = point( 1300, 700 )
        self.gfOffset = point( 0,0 )
        crSize = point( 300, 700 )
        self.crOffset = point( 1000, 0 )

        # Initialise screen
        pygame.init()
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption('Unicorn hunt program')

        # --- chat room part -------
        self.cr = chatRoom( crSize )
        # --- chat room part -------

        def dprint( str ):
            self.cr.addMessage( "system", str )

        # --- game field part -------
        self.gf = gameField( tilesGeo, debugprint=dprint )
        # --- game field part -------

        # --- units part -------
        self.unicorn = unit( unitList['unicorn'], self.gf, self.cr, point(4,4) )
        self.cr.addMessage( "system", "Unicorn at %s"%( self.unicorn.pos, ) )
        self.unicorn.action["idle"] = eatGrass()    
        self.badguy = unit( unitList['badguy'], self.gf, self.cr, point(10,10) )
        self.cr.addMessage( "system", "Badguy at %s"%( self.badguy.pos, ) )
        self.maiden = unit( unitList['maiden'], self.gf, self.cr, point(20,20) )
        self.cr.addMessage( "system", "maiden at %s"%( self.maiden.pos, ) )
        
        self.units = [self.badguy, self.maiden, self.unicorn]

        # --- units part -------

        self.popupMaidenWins = popup( (300, 300), "and they rode into the sunset..." )
        self.popupEvilWins = popup( (600, 300), "Evil conquered beauty and darkness fell" )

        # Blit everything to the screen
        self.cr.update( self.screen, self.crOffset)
        self.gf.update( self.screen, self.crOffset)


        # remote access
        kr = {}
        kr_thr = {}
        for user in ["userA", "userB", "userC"]:
            kr[user] = keyReceiver( '0.0.0.0', remoteEvent[user]['port'], user )
            kr_thr[user] = threading.Thread(name="%s_remote"%(user, ), target=kr[user].listen)
            kr_thr[user].setDaemon( True )
            kr_thr[user].start()
            self.cr.addMessage( "system", "%s on port %d"%(user, remoteEvent[user]['port']) )

        pygame.display.flip()
        # Event loop

        quitLoop = False
        self._state = gameStates.startup
        self.unitToMove = self.badguy
        self.unitToMove.controlled = True

        self.remoteA_enable = True
        self.remoteB_enable = True
        
        print "press space to start, q to quit"
        
        while not quitLoop:
            refresh = False
            
            if self._state == gameStates.rungame:
                quitLoop, refresh, nextState = self.runGame()
            elif self._state == gameStates.startup:
                quitLoop, refresh, nextState = self.runStartup()
            elif self._state == gameStates.maidenwins:
                quitLoop, refresh, nextState = self.runMaidenWins()
            elif self._state == gameStates.evilwins:
                quitLoop, refresh, nextState = self.runEvilWins()
            elif self._state == gameStates.quit:
                quitLoop = True
            else:
                print "current state is", self._state

            self._state = nextState

    def runGame( self ):
        quitLoop = False
        refresh = False
        nextState = gameStates.rungame

        for event in pygame.event.get():
            print event
            quitLoop = self.checkQuit( event )

            #if self.remoteA_enable:
            self.handleRemoteEvents( "userA", self.badguy, event )
#            self.handleRemoteEvents( "userB", self.maiden, event )
#            self.handleRemoteEvents( "userC", self.unicorn, event )
#            self.unitToMove.controlled = True
#            self.unitToMove.controlled = True
#            self.unitToMove.controlled = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    self.cr.addComment( "system", "Now moving unicorn" )
                    self.unitToMove.controlled = False
                    self.unitToMove = self.unicorn
                    self.unitToMove.controlled = True
                if event.key == pygame.K_b:
                    self.cr.addComment( "system", "Now moving badguy" )
                    self.unitToMove.controlled = False
                    self.unitToMove = self.badguy
                    self.unitToMove.controlled = True
                if event.key == pygame.K_m:
                    self.cr.addComment( "system", "Now moving maiden" )
                    self.unitToMove.controlled = False
                    self.unitToMove = self.maiden
                    self.unitToMove.controlled = True

                if event.key == pygame.K_LEFT:
                    print self.unitToMove.name
                    self.unitToMove.doAction( "moveLeft", self.units )
                if event.key == pygame.K_RIGHT:
                    self.unitToMove.doAction( "moveRight", self.units )
                if event.key == pygame.K_DOWN:
                    self.unitToMove.doAction( "moveDown", self.units )
                if event.key == pygame.K_UP:
                    self.unitToMove.doAction( "moveUp", self.units)
        
            if event.type == E_EVILWINS:
                self.cr.addComment( "system", "Evil wins!!" )
                nextState = gameStates.evilwins

            if event.type == E_MAIDENWINS:
                self.cr.addComment( "system", "Maiden wins!!" )
                nextState = gameStates.maidenwins

        
        for unit in self.units:
            if not unit.autoMove( self.units ):
                unit.doAction( "idle", self.units )

        if self.gf.dirty:
            self.gf.update( self.screen, self.gfOffset)
            for unit in self.units:
                unit.update( self.screen, self.gfOffset)
            refresh = True
            
        if self.cr.dirty:
            #print "cr update"
            self.cr.update( self.screen, self.crOffset)
            refresh = True

        if refresh:
            #print "refreshing"
            pygame.display.flip()
            refresh = False

        return quitLoop, refresh, nextState

    def checkQuit( self, event ):
        if event.type == QUIT:
            return True
        return False

    def runMaidenWins( self ):
        quitLoop = False
        refresh = False
        nextState = gameStates.maidenwins

        for event in pygame.event.get():
            quitLoop = self.checkQuit( event )

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitLoop = True

        if self.popupMaidenWins.dirty:
            self.popupMaidenWins.update( self.screen, self.gfOffset)
            refresh = True
                            
        if refresh:
            pygame.display.flip()
            refresh = False

        return quitLoop, refresh, nextState


    def runEvilWins( self ):
        quitLoop = False
        refresh = False
        nextState = gameStates.evilwins

        for event in pygame.event.get():
            quitLoop = self.checkQuit( event )

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitLoop = True

        if self.popupEvilWins.dirty:
            self.popupEvilWins.update( self.screen, self.gfOffset)
            refresh = True
                            
        if refresh:
            pygame.display.flip()
            refresh = False

        return quitLoop, refresh, nextState

    def runStartup( self ):
        quitLoop = False
        refresh = False
        nextState = gameStates.startup

        for event in pygame.event.get():
            quitLoop = self.checkQuit( event )

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitLoop = True

                if event.key == pygame.K_SPACE:
                    nextState = gameStates.rungame
            
        if refresh:
            pygame.display.flip()
            refresh = False

        return quitLoop, refresh, nextState

    def handleRemoteEvents( self, user, unit, event ):
        if event.type == remoteEvent[user]['up']:
            unit.doAction( "moveUp", self.units )
        elif event.type == remoteEvent[user]['down']:
            unit.doAction( "moveDown", self.units )
        elif event.type == remoteEvent[user]['left']:
            unit.doAction( "moveLeft", self.units )
        elif event.type == remoteEvent[user]['right']:
            unit.doAction( "moveRight", self.units )



if __name__ == "__main__":
    g = game()
#    g.run()
