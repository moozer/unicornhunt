# uh-support.py
# supporting functions, classes and so on

from collections import namedtuple
import pygame
import numpy
import time

point = namedtuple( 'point', ['x', 'y'] )
tileinfo = namedtuple( 'tileInfo', ['filename', 'symbol'] )
unitinfo = namedtuple( 'unitInfo', ['filename', 'symbol', 'name', 'attract'] )

tileList = { 'grass': tileinfo( "images/grass.png", "s" ) }
unitList = { 'maiden': unitinfo( "images/princess.png", 'm', 'maiden',
                                  {'maiden': 0.0, 'badguy': -5.0, 'unicorn': 10.0 } ), 
             'badguy': unitinfo( "images/badguy.png", 'b', 'badguy',
                                  {'maiden': 5.0, 'badguy': -1.0, 'unicorn': 10.0 } ), 
             'unicorn': unitinfo( "images/unicorn.png", 'u', 'unicorn',
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
    

class unit( uhgraphics ):
    def __init__( self, info, gamefield, chatroom, initialPos = point(0,0) ):
        self._screen =  pygame.image.load( info.filename )
        self._pos = initialPos
        self._dirty = True
        self._gamefield = gamefield
        self.name = info.name
        self.info = info
        self._actions = {}
        self.nextActionTime = time.time() * 1000 # in ms
        self._chatroom = chatroom

    def comment( self, string ):
        self._chatroom.addComment( self.name, string )

    def talk( self, string ):
        self._chatroom.addMessage( self.name, string )
        
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

    @property
    def action( self ):
        return self._actions

    def doAction( self, actionName ):
        print "%s doing %s"%( self.name, actionName )
        self._actions[actionName]( self )

def moveUnit( unit, unitList ):
    moveDirection = [0.0, 0.0]

    for otherUnit in unitList:
        if unit == otherUnit:
            continue

        vect = [otherUnit.pos.x - unit.pos.x, otherUnit.pos.y - unit.pos.y]
        dist = numpy.linalg.norm( vect )

        force = unit.info.attract[otherUnit.name]/dist/dist
        
        moveInc = vect * 1/dist*force
        moveDirection = moveDirection + moveInc
        
    if moveDirection[0] > 0.5:
        unit.moveRight()
        return True
    elif moveDirection[0] < -0.5:
        unit.moveLeft()
        return True

    if moveDirection[1] > 0.5:
        unit.moveDown()
        return True
    elif moveDirection[1] < -0.5:
        unit.moveUp()
        return True
    
    return False
    
