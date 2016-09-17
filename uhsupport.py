# uh-support.py
# supporting functions, classes and so on

from collections import namedtuple
import pygame
import numpy
import time

point = namedtuple( 'point', ['x', 'y'] )
tileinfo = namedtuple( 'tileInfo', ['filename', 'symbol'] )
unitinfo = namedtuple( 'unitInfo', ['filename', 'symbol', 'name', 'speed', 'attract'] )

tileList = { 'grass': tileinfo( "images/grass.png", "s" ) }
unitList = { 'maiden': unitinfo( "images/princess.png", 'm', 'maiden', 350,
                                  {'maiden': 0.0, 'badguy': -250.0, 'unicorn': 1000.0 } ), 
             'badguy': unitinfo( "images/badguy.png", 'b', 'badguy', 250,
                                  {'maiden': 5.0, 'badguy': -1.0, 'unicorn': 50.0 } ), 
             'unicorn': unitinfo( "images/unicorn.png", 'u', 'unicorn', 150,
                                  {'maiden': 50.0, 'badguy': -12.5, 'unicorn': 0.0 } ) }

class directions:
    up, down, left, right = range(4)

class gameStates:
    startup, rungame, evilwins, maidenwins, quit = range(5)

def debugprint( str ):
    print str

E_EVILWINS = pygame.USEREVENT  + 1
E_MAIDENWINS = pygame.USEREVENT + 2
E_REMOTE_A_UP    = pygame.USEREVENT + 3
E_REMOTE_A_DOWN  = pygame.USEREVENT + 4
E_REMOTE_A_LEFT  = pygame.USEREVENT + 5
E_REMOTE_A_RIGHT = pygame.USEREVENT + 6
E_REMOTE_B_UP    = pygame.USEREVENT + 7
E_REMOTE_B_DOWN  = pygame.USEREVENT + 8
E_REMOTE_B_LEFT  = pygame.USEREVENT + 9
E_REMOTE_B_RIGHT = pygame.USEREVENT + 10

remoteEvent = { "userA": {'up': E_REMOTE_A_UP, 'down': E_REMOTE_A_DOWN , 
                          'right': E_REMOTE_A_RIGHT, 'left': E_REMOTE_A_LEFT,
                          'port': 10000 },
                "userB": {'up': E_REMOTE_B_UP, 'down': E_REMOTE_B_DOWN , 
                          'right': E_REMOTE_B_RIGHT, 'left': E_REMOTE_B_LEFT,
                          'port': 10001} }

gameOverMatrix = { 'maiden':  { 'unicorn': E_MAIDENWINS },
                   'unicorn': { 'maiden': E_MAIDENWINS, 'badguy': E_EVILWINS },
                   'badguy':  { 'unicorn': E_EVILWINS } }
                   
class uhgraphics:
    _dirty = True
    _screen = None
    
    @property
    def dirty( self ):
        return self._dirty
        
    def update( self, screen, offset ):
        screen.blit(self.screen, offset)
        self._dirty = False

    @property
    def screen( self):
        return self._screen


class tile( uhgraphics ):
    def __init__( self, filename ):
        self._screen = pygame.image.load( filename )
    

