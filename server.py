import socket
import threading
import SocketServer
import time

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(1024)
            #cur_thread = threading.current_thread()
            #response = "{}: {}".format(cur_thread.name, data)
            self.request.send(data)
            
            if data == "goodbye":
                self.request.sendall("goodbye")
                break

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    
    print "Server loop running in thread:", server_thread.name
    print ip, port

    try:
        while True:
            time.sleep( 10 )
            print "."
    except KeyboardInterrupt:
        print "ctrl+c"
        
#    client(ip, port, "Hello World 1")
#    client(ip, port, "Hello World 2")
#    client(ip, port, "Hello World 3")

    server.shutdown()
    server.server_close()
    
