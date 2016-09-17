# possible actions
import time, random
from uhsupport import *

class action():
    _time = 500
    _comment = None
    _message = None

    def __call__( self, unit ):
        if unit.nextActionTime > time.time() * 1000:
            return False

        if self._comment:
            unit.comment( self._comment )
        if self._message:
            unit.message( self._message )

        self._doAction( unit )
        
        unit.nextActionTime = time.time()*1000 + self._time

    def _doAction( self, unit ):
        return
        
class eatGrass( action ):
    def __init__( self ):
        self._time = 500
        self._comment = "eats grass"
        
    def _doAction( self, unit ):
        moves = [(-1, 0), (0,0), (1, 0), (0, -1), (0,0), (0, 1)]
        move = moves[random.randint(0, 5)]
    
        print "%s eats grass and moves %s"%( unit.name, move )
    
        if move[0] == -1:
            unit.moveLeft()
        elif move[0] == 1:
            unit.moveRight()
        elif move[1] == -1:
            unit.moveUp()
        elif move[1] == 1:
            unit.moveDown()

class move( action ):
    def __init__( self, time, direction ):
        self._time = time
        self._direction = direction
        
    def _doAction( self, unit ):
        if self._direction == directions.right:
            unit.moveRight()
        elif self._direction == directions.left:
            unit.moveLeft()
        elif self._direction == directions.down:
            unit.moveDown()
        elif self._direction == directions.up:
            unit.moveUp()
        
