import pygame
from uhsupport import *

class popup( uhgraphics ):
    def __init__( self, size, text ):
        self._size = size
        self._bkColor = ( 100, 100, 100)
    
        self._fontSize = 24
        self._font = pygame.font.Font(None, self._fontSize)
        self._fontColor = (10, 10, 10)
    
        self._screen = pygame.Surface( self._size )
        self._screen = self._screen.convert()
        self._screen.fill( self._bkColor )
        
        self._dirty = True

        text = self._font.render( text, 1, self._fontColor )
        textpos = text.get_rect()
        textpos.center = self._screen.get_rect().center
        self._screen.blit(text, textpos)
        self._dirty = True
