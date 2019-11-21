#!usr/bin/env python

import socket
import threading
import select
import time
from argparse import ArgumentParser

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
            
class Text_Input(threading.Thread):
        def __init__(self, thread):
            threading.Thread.__init__(self)
            self.running = 1
            self.thread = thread
        def run(self):
            while self.running == True:
              print('waiting for text')
              text = input()
              byteArray = text.encode('UTF-8')
              try:
                  self.thread.socket.sendall(byteArray)
                  print('sent text '+text)
              except Exception as e:
                  print('error '+str(e))
              time.sleep(0)
        def kill(self):
            self.running = 0

def str2bool(v):
  if isinstance(v, bool):
      return v
  if v.lower() in ('yes', 'true', 't', 'y', '1'):
      return True
  elif v.lower() in ('no', 'false', 'f', 'n', '0'):
      return False
  else:
      raise Exception('Boolean value expected.')

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-i', '--invert', default=False, type=str2bool, help='Invert defaults')
    parser.add_argument('-op', '--openport', default=5000, type=int, help='port to listen on')
    parser.add_argument('-cp', '--connectport', default=5001, type=int, help='port to send on')
    parser.add_argument('-w', '--wait', default=True, type=str2bool, help='wait before running client')
    args = parser.parse_args()
    openport = args.openport
    connectport = args.connectport
    wait = args.wait
    invert = args.invert

    if invert:
      openport2 = connectport
      connectport2 = openport
      connectport = connectport2
      openport = openport2

    chat_server = Chat_Server(openport)
    chat_server.start()

    while wait:
      print('type something to continue')
      x = input()
      wait = False

    chat_client = Chat_Client(connectport)
    chat_client.host = '127.0.0.1'
    chat_client.start()
    text_input = Text_Input(chat_client)
    text_input.start()


