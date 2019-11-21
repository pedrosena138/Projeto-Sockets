import socket
import threading
import select
import time

class Chat_Server(threading.Thread):
        def __init__(self, port):
            threading.Thread.__init__(self)
            self.running = 1
            self.socket = None
            self.addr = None
            self.port = port

        def run(self):
            HOST = '127.0.0.1'
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST,self.port))
            s.listen(1)
            self.socket, self.addr = s.accept()

            # Select loop for listen
            while self.running == True:  
              data = self.socket.recv(1024)
              if data:
                  print("The server received: " + str(data))
                
        def kill(self):
            self.running = 0