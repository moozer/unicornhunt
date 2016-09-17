import socket
import sys

from uhsupport import *

class keyReceiver():
    def __init__( self, ip, port, user ):
        # Bind the socket to the address given on the command line
        self.server_name = '127.0.0.1'
        self.server_address = (self.server_name, 10000)
        self._user = user

    def _ProcessKeys( self, keys ):
        for ch in keys:
            print ">%s<"%(ch,)
            if ch == 'w':
                pygame.event.post( pygame.event.Event( remoteEvent[self._user]['up'] ) )
            elif ch == 's':
                pygame.event.post( pygame.event.Event( remoteEvent[self._user]['down'] ) )
            elif ch == 'a':
                pygame.event.post( pygame.event.Event( remoteEvent[self._user]['left'] ) )
            elif ch == 'd':
                pygame.event.post( pygame.event.Event( remoteEvent[self._user]['right'] ) )


    def listen( self ):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print >>sys.stderr, 'starting up on %s port %s' % self.server_address
        sock.bind( self.server_address)
        sock.listen(1)

        while True:
            print >>sys.stderr, 'waiting for a connection'
            connection, client_address = sock.accept()
            try:
                print >>sys.stderr, 'client connected:', client_address
                while True:
                    data = connection.recv(16)
                    print >>sys.stderr, 'received "%s"' % data
                    if data:
                        if data == "hello":
                            self.sendGreeting( connection )
                        elif data == "goodbye":
                            self.sendGoodbye( connection)
                        else:
                            connection.sendall(data)
                            self._ProcessKeys( data )
                    else:
                        break
            finally:
                connection.close()
    
    def sendGreeting( self, connection ):
        connection.send( "greetings\n" )
        connection.send( "you are user %s\n"%(self._user,) )
        connection.send( "Now expecting key strokes\n" )
        connection.send( "\n" )
        
    def sendGoodbye( self, connection ):
        connection.send( "goodbye" )
        connection.send( "\n" )
        
        
if __name__ == "__main__":
    kr = keyReceiver( '127.0.0.1', 10000, "userA" )
    kr.listen()
