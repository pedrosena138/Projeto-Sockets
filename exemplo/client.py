import socket
import threading
import select
import time

class Chat_Client(threading.Thread):
        def __init__(self, port):
            threading.Thread.__init__(self)
            self.host = None
            self.socket = None
            self.port = port
            self.running = 1

        def run(self):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            # Select loop for listen
            while self.running == True:  
                data = self.socket.recv(1024)
                if data:
                    print("The client received: " + str(data))
              
        def kill(self):
            self.running = 0