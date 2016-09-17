# possible actions
import time, random
from uhsupport import *

class action():
    _time = 500
    _comment = None
    _message = None

    def __call__( self, unit, units ):
        if unit.nextActionTime > time.time() * 1000:
            return False

        if self._comment:
            unit.comment( self._comment )
        if self._message:
            unit.message( self._message )

        if self._doAction( unit, units ):
            unit.nextActionTime = time.time()*1000 + self._time
            return True
        
        return False

    def _doAction( self, unit, units ):
        return True
        
class eatGrass( action ):
    def __init__( self ):
        self._time = 500
        self._comment = "eats grass"
        
    def _doAction( self, unit, units ):
        moves = [(-1, 0), (0,0), (1, 0), (0, -1), (0,0), (0, 1)]
        move = moves[random.randint(0, 5)]
    
        print "%s eats grass and moves %s"%( unit.name, move )
    
        if move[0] == -1:
            unit.moveLeft( units )
        elif move[0] == 1:
            unit.moveRight( units )
        elif move[1] == -1:
            unit.moveUp( units )
        elif move[1] == 1:
            unit.moveDown( units )
    
        return True

class move( action ):
    def __init__( self, time, direction ):
        self._time = time
        self._direction = direction
        
    def _doAction( self, unit, units ):
        if self._direction == directions.right:
            ret = unit.moveRight( units )
        elif self._direction == directions.left:
            ret = unit.moveLeft( units )
        elif self._direction == directions.down:
            ret = unit.moveDown( units )
        elif self._direction == directions.up:
            ret = unit.moveUp( units )

        return ret
        
class fall( action ):
    def __init__( self, direction ):
        self._time = 1000
        self._direction = direction
        self._comment = "falls"
        
    def _doAction( self, unit, units ):
        if self._direction == directions.right:
            ret = unit.moveRight( units )
        elif self._direction == directions.left:
            ret = unit.moveLeft( units )
        elif self._direction == directions.down:
            ret = unit.moveDown( units )
        elif self._direction == directions.up:
            ret = unit.moveUp( units )

        return ret
    
    
