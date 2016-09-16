# uh-support.py
# supporting functions, classes and so on

from collections import namedtuple
import pygame

point = namedtuple( 'point', ['x', 'y'] )
tileinfo = namedtuple( 'tileInfo', ['filename', 'symbol'] )
unitinfo = namedtuple( 'unitInfo', ['filename', 'symbol'] )


tileList = { 'grass': tileinfo( "images/grass.png", "s" ) }
unitList = { 'maiden': unitinfo( "images/maiden.png", 'm' ), 
             'badguy': unitinfo( "images/badguy.png", 'b' ),
             'unicorn': unitinfo( "images/unicorn.png", 'u' ) }

def debugprint( str ):
    print str

class tile():
    def __init__( self, filename ):
        self._image = pygame.image.load( filename )
    
    @property
    def image( self ):
        return self._image

class unit():
    def __init__( self, info ):
        self._image =  pygame.image.load( info.filename )
        self._pos = point( 0,0 )
        
    @property
    def pos( self ):
        return pos
    
    @property
    def image( self ):
        return self._image
