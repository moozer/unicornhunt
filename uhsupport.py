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
unitList = { 'maiden': unitinfo( "images/princess.png", 'm', 'maiden', 450,
                                  {'maiden': 0.0, 'badguy': -5.0, 'unicorn': 10.0 } ), 
             'badguy': unitinfo( "images/badguy.png", 'b', 'badguy', 350,
                                  {'maiden': 5.0, 'badguy': -1.0, 'unicorn': 10.0 } ), 
             'unicorn': unitinfo( "images/unicorn.png", 'u', 'unicorn', 250,
                                  {'maiden': 10.0, 'badguy': -12.5, 'unicorn': 0.0 } ) }

class directions:
    up, down, left, right = range(4)

def debugprint( str ):
    print str


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
    

