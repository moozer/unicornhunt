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
E_MAIDENWINS = pygame.USEREVENT  + 2

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
    

