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
    

class unit( uhgraphics ):
    def __init__( self, info, gamefieldInfo ):
        self._screen =  pygame.image.load( info.filename )
        self._pos = point( 0,0 )
        self._gamefieldInfo = gamefieldInfo
        self._dirty = True
        
    @property
    def pos( self ):
        return pos

    def moveLeft( self ):
        if pos.x > 0:
            pos.x -= 1
            self._dirty = True
    
    def moveRight( self ):
        if pos.x < self._gamefieldInfo.size.x:
            pos.x += 1
            self._dirty = True
    
    def moveUp( self ):
        if pos.y > 0:
            pos.y -= 1
            self._dirty = True

    def moveDown( self ):
        if pos.y < self._gamefieldInfo.size.y:
            pos.y -= 1
            self._dirty = True
