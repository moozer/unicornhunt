from uhsupport import *
from actions import *

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
        
        self._addMoveActions()

    def _addMoveActions( self ):   
        self._actions["moveLeft"]  = move( self.info.speed, directions.left )    
        self._actions["moveRight"] = move( self.info.speed, directions.right )    
        self._actions["moveUp"]    = move( self.info.speed, directions.up )    
        self._actions["moveDown"]  = move( self.info.speed, directions.down )    

        self._actions["pushedLeft"]  = fall( directions.left )    
        self._actions["pushedRight"] = fall( directions.right )    
        self._actions["pushedUp"]    = fall( directions.up )    
        self._actions["pushedDown"]  = fall( directions.down )    
        
        self._actions["idle"]      = action()

    def comment( self, string ):
        self._chatroom.addComment( self.name, string )

    def talk( self, string ):
        self._chatroom.addMessage( self.name, string )
        
    @property
    def pos( self ):
        return self._pos

    def moveLeft( self, units ):
        nextPos = point( self._pos.x - 1, self._pos.y )
        
        noObstacle = True
        for unit in units:
            if unit.pos == nextPos:
                noObstacle = unit.doAction('pushedLeft', units )
                print "pushing?", noObstacle
                break

        
        if not noObstacle:
            return False
        
        if self._pos.x > 0:
            self._gamefield.updateTile( self._pos )
            self._pos = nextPos
            self._dirty = True
            return True
            
        print "ret false"
        return False
        
    def moveRight( self, units ):
        nextPos = point( self._pos.x + 1, self._pos.y )

        noObstacle = True
        for unit in units:
            if unit.pos == nextPos:
                noObstacle = unit.doAction('pushedRight', units )
                print "pushing?", noObstacle
                break
        
        if not noObstacle:
            return False
                
        if self._pos.x < self._gamefield.tilesGeo.x-1:
            self._gamefield.updateTile( self._pos )
            self._pos = nextPos
            self._dirty = True
            return True
            
        return False
    
    def moveUp( self, units  ):
        nextPos = point( self._pos.x, self._pos.y-1 )

        noObstacle = True
        for unit in units:
            if unit.pos == nextPos:
                noObstacle = unit.doAction('pushedUp', units )
                break                
        
        if not noObstacle:
            return False

        if self._pos.y > 0:
            self._gamefield.updateTile( self._pos )
            self._pos = nextPos
            self._dirty = True
            return True
            
        return False

    def moveDown( self, units  ):
        nextPos = point( self._pos.x, self._pos.y+1 )

        noObstacle = True
        for unit in units:
            if unit.pos == nextPos:
                noObstacle = unit.doAction('pushedDown', units )
                break                

        
        if not noObstacle:
            return False

        if self._pos.y < self._gamefield.tilesGeo.y-1:
            self._gamefield.updateTile( self._pos )
            self._pos = nextPos
            self._dirty = True
            return True
            
        return False

    def update( self, screen, gfOffset ):
        tilePos = self._gamefield.tilePos( self._pos )
        unitOffset = (gfOffset.x + tilePos.x, gfOffset.y + tilePos.y )
        screen.blit(self.screen, unitOffset)
        self._dirty = False

    @property
    def action( self ):
        return self._actions

    def doAction( self, actionName, units ):
        #print "%s doing %s"%( self.name, actionName )
        return self._actions[actionName]( self, units )

    def autoMove( self, otherUnits ):
#        if self.nextActionTime > time.time()*1000:
#            return False

        moveDirection = [0.0, 0.0]
        for otherUnit in otherUnits:
            if self == otherUnit:
                continue

            vect = [otherUnit.pos.x - self.pos.x, otherUnit.pos.y - self.pos.y]
            dist = numpy.linalg.norm( vect )

            force = self.info.attract[otherUnit.name]/dist/dist
            
            moveInc = vect * 1/dist*force
            moveDirection = moveDirection + moveInc
        
        ret = True
        if moveDirection[0] > 0.5:
            ret = self._actions['moveRight']( self, otherUnits )
        elif moveDirection[0] < -0.5:
            ret = self._actions['moveLeft']( self, otherUnits )

        if not ret:
            if self.pos.y > self._gamefield.tilesGeo.y/2:
                self._actions['moveUp']( self, otherUnits )                
            else:
                self._actions['moveDown']( self, otherUnits )

        ret = True
        if moveDirection[1] > 0.5:
            ret = self._actions['moveDown']( self, otherUnits )
        elif moveDirection[1] < -0.5:
            ret = self._actions['moveUp']( self, otherUnits )
        
        if not ret:
            if self.pos.x > self._gamefield.tilesGeo.x/2:
                self._actions['moveLeft']( self, otherUnits )                
            else:
                self._actions['moveRight']( self, otherUnits )

        return False
        
