import pygame
from pygame.locals import *

from uhsupport import *

class gameField( uhgraphics ):
    def __init__( self, tilesGeo, tileList = tileList, debugprint = debugprint ):
        self._print = debugprint

        self._tileSize = point( 32, 32 )
        self._tilesGeo = tilesGeo
        self._tileList = tileList
        self._loadTiles()
        
        self._dirty = True

        self._size = (self._tileSize.x * self._tilesGeo.x,  self._tileSize.y * self._tilesGeo.y ) 
        self._print("Game field size is %s"%(self._size, ) )
        self._initGraphics()

    def _loadTiles( self ):
        self._print("Loading tiles")
        self._tiles = []
        for t in self._tileList.keys():
            self._print("- loading %s"%(t,) )
            self._tiles.append( tile( self._tileList[t].filename ) )
    
    def _addTiles( self ):
        self._print("Populating game field")
        for x in range( 0, self._tilesGeo.x ):
            for y in range( 0, self._tilesGeo.y ):
                self._tiles[0].update( self._screen, (x*self._tileSize.x, y*self._tileSize.y) )
    
    def _initGraphics( self ):
        self._screen = pygame.Surface(self._size)
        self._screen = self._screen.convert()
        self._addTiles()

    @property
    def tilesGeo( self ):
        return self._tilesGeo
    
    def tilePos( self, tileXY ):
        return point( tileXY.x*self._tileSize.x, tileXY.y*self._tileSize.y )
    
    def updateTile( self, pos ):
        self._tiles[0].update( self._screen, (pos.x*self._tileSize.x, pos.y*self._tileSize.y) )
        self._dirty = True
    
if __name__ == "__main__":
    pygame.init()
    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()

    screenSize = point( 32*30, 32*20)
    gfOffset = point( 0,0 )

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('game field test program')

    # --- game field part -------
    gf = gameField( point( 30, 20 ) )
    # --- game field part -------

    # Blit everything to the screen
    screen.blit( gf.screen, gfOffset )
    pygame.display.flip()

    # Event loop
    quitLoop = False
    while not quitLoop:
        for event in pygame.event.get():
            if event.type == QUIT:
                quitLoop = True

        screen.blit(gf.screen, gfOffset)
        pygame.display.flip()

