# uh-support.py
# supporting functions, classes and so on

from collections import namedtuple
import pygame

point = namedtuple( 'point', ['x', 'y'] )
tileinfo = namedtuple( 'tileInfo', ['filename', 'symbol'] )
unitinfo = namedtuple( 'unitInfo', ['filename', 'symbol', 'name'] )


tileList = { 'grass': tileinfo( "images/grass.png", "s" ) }
unitList = { 'maiden': unitinfo( "images/princess.png", 'm', 'maiden' ), 
             'badguy': unitinfo( "images/badguy.png", 'b', 'badguy' ),
             'unicorn': unitinfo( "images/unicorn.png", 'u', 'unicorn' ) }

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
    def __init__( self, info, gamefield, initialPos = point(0,0) ):
        self._screen =  pygame.image.load( info.filename )
        self._pos = initialPos
        self._dirty = True
        self._gamefield = gamefield
        self.name = info.name
        
    @property
    def pos( self ):
        return self._pos

    def moveLeft( self ):
        if self._pos.x > 0:
            self._gamefield.updateTile( self._pos )
            self._pos = point( self._pos.x - 1, self._pos.y )
            self._dirty = True
    
    def moveRight( self ):
        if self._pos.x < self._gamefield.tilesGeo.x-1:
            self._gamefield.updateTile( self._pos )
            self._pos = point( self._pos.x +1 , self._pos.y )
            self._dirty = True
    
    def moveUp( self ):
        if self._pos.y > 0:
            self._gamefield.updateTile( self._pos )
            self._pos = point( self._pos.x, self._pos.y -1 )
            self._dirty = True

    def moveDown( self ):
        if self._pos.y < self._gamefield.tilesGeo.y-1:
            self._gamefield.updateTile( self._pos )
            self._pos = point( self._pos.x, self._pos.y + 1 )
            self._dirty = True

    def update( self, screen, gfOffset ):
        tilePos = self._gamefield.tilePos( self._pos )
        unitOffset = (gfOffset.x + tilePos.x, gfOffset.y + tilePos.y )
        screen.blit(self.screen, unitOffset)
        self._dirty = False
