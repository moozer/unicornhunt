# uh-support.py
# supporting functions, classes and so on

from collections import namedtuple
import pygame

point = namedtuple( 'point', ['x', 'y'] )
tileinfo = namedtuple( 'tileInfo', ['filename', 'symbol'] )

tileList = { 'grass': tileinfo( "images/grass.png", "s" ) }

def debugprint( str ):
    print str

class tile():
    def __init__( self, filename ):
        self._image = pygame.image.load( filename )
    
    @property
    def image( self ):
        return self._image
