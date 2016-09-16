import pygame
from pygame.locals import *

from uhsupport import *

class chatRoom( uhgraphics ):
    def __init__( self, size ):
        self._size = size

        self._fontSize = 24
        self._font = pygame.font.Font(None, self._fontSize)
        self._fontColor = (10, 10, 10)

        self._bkColor = (250, 250, 250 )
        self._currentLine = -1
        self._maxLines = size.y/self._fontSize
        
        self._dirty = True
        
        self._initGraphics()

    def _initGraphics( self ):
        self._crScreen = pygame.Surface( self._size)
        self._crScreen = self._crScreen.convert()
        self._crScreen.fill( self._bkColor )
        
    @property
    def screen( self):
        return self._crScreen
        
    def addMessage( self, unit, words ):
        self._incrementCurrentLine()

        print "Chatroom: %s: %s"%( unit, words )

        text = self._font.render( "%s: %s"%( unit, words ), 1, self._fontColor )
        textpos = text.get_rect()
        textpos.topleft = ( 0, self._currentLine*(self._fontSize+1) )
        self._crScreen.blit(text, textpos)
        self._dirty = True

    def addComment( self, unit, action ):
        self._incrementCurrentLine()

        print "Chatroom action: %s %s"%( unit, action )

        text = self._font.render( "%s %s"%( unit, action ), 1, self._fontColor )
        textpos = text.get_rect()
        textpos.topleft = ( 0, self._currentLine*(self._fontSize+1) )
        self._crScreen.blit(text, textpos)
        self._dirty = True

    def _incrementCurrentLine( self ):
        self._currentLine += 1
        if self._currentLine == self._maxLines:
            self._currentLine = 0
            print "TBD -> scroll now"


    
if __name__ == "__main__":
    pygame.init()
    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()

    crSize = point(200, 500)
    crOffset = point( 0,0 )

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode(crSize)
    pygame.display.set_caption('chat room test program')

    # --- chat room part -------
    cr = chatRoom( crSize )
    cr.addMessage( "maiden", "Come to me" )
    cr.addComment( "Unicorn", "eats grass" )
    cr.addMessage( "Badguy", "Hahahaha!" )
    # --- chat room part -------

    # Blit everything to the screen
    screen.blit( cr.screen, crOffset )
    pygame.display.flip()

    # Event loop
    quitLoop = False
    while not quitLoop:
        for event in pygame.event.get():
            if event.type == QUIT:
                quitLoop = True

        screen.blit(cr.screen, (0, 0))
        pygame.display.flip()

