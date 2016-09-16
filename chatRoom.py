import pygame
from pygame.locals import *
from collections import namedtuple

point = namedtuple( 'point', ['x', 'y'] )

class chatRoom():
    def __init__( self, size, offset = point( 0,0 ) ):
        self._size = size
        self._offset = offset

        self._fontSize = 24
        self._font = pygame.font.Font(None, self._fontSize)
        self._fontColor = (10, 10, 10)
 #       self._screen = screen

        self._bkColor = (250, 250, 250 )
        self.currentLine = -1
        self.maxLines = size.y/self._fontSize
        
        self._initGraphics()

    def _initGraphics( self ):
        # Fill background
        self._crScreen = pygame.Surface(screen.get_size())
        self._crScreen = self._crScreen.convert()
        self._crScreen.fill( self._bkColor )
#        self._screen.blit(self._crScreen, (self._offset.x, self._offset.y ))

        
    @property
    def screen( self):
        return self._crScreen
        
    def addMessage( self, unit, words ):
        self._incrementCurrentLine()

        print "Chatroom: %s: %s"%( unit, words )

        text = self._font.render( "%s: %s"%( unit, words ), 1, self._fontColor )
        textpos = text.get_rect()
        #textpos.centerx = self._crScreen.get_rect().centerx
        textpos.topleft = ( 0, self.currentLine*(self._fontSize+1) )
        self._crScreen.blit(text, textpos)

    def _incrementCurrentLine( self ):
        self.currentLine += 1
        if self.currentLine == self.maxLines:
            self.currentLine = 0
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

    # Fill background
#    background = pygame.Surface(screen.get_size())
#    background = background.convert()
#    background.fill((250, 250, 250))

    cr = chatRoom( crSize )
    cr.addMessage( "maiden", "Come to me" )
    #    cr.addComment( "Unicorn", "eats grass" )
    cr.addMessage( "Badguy", "Hahahaha!" )

    # Display some text
#    font = pygame.font.Font(None, 36)
#    text = font.render("Hello There", 1, (10, 10, 10))
#    textpos = text.get_rect()
#    textpos.centerx = background.get_rect().centerx
#    background.blit(text, textpos)

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
