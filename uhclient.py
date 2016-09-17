import argparse
import socket
import readchar

def handleCmdArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("server", help="IP address to connect to", type=str)
    parser.add_argument("port", help="port number on server", type=int)
    
    args = parser.parse_args()
    return args

def doMovement( sock ):
    char = readchar.readchar()
    
    if char in ['w', 'a', 's', 'd']:
        sock.send( char )
        response = sock.recv(1)
        print ">", response
        
    elif char == 'q':
        print "quitting"
        return False
        
    else:
        print "use w,a,s or d to control, q to quit"
    
    return True

def client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    try:
        sock.sendall("hello")
        print sock.recv(1024)
        
        print "Now doing movement"
        
        while doMovement( sock ):
            pass
 
        sock.sendall("goodbye")
        print sock.recv(1024)
 
    finally:
        sock.close()

if __name__ == "__main__":
    config = handleCmdArgs()
    
    client( config.server, config.port )
