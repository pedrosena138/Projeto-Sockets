import socket, threading, sys, time
from random import randint

class Server:
    connections = list()
    peers = list()
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 10000))
        sock.listen(1)
        print('server is running...')
        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            print(str(a[0]) + ': ' + str(a[1]), 'connected')
            self.sendPeers()

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(bytes(data))
            if not data:
                print(str(a[0]) + ': ' + str(a[1]), 'disconnected')
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break

    def sendPeers(self):
        p = str()
        for peer in self.peers:
            p += peer + ','
        
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, 'utf-8'))

class Client: 
    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, 10000))

        iThread = threading.Thread(target=self.sendMsg, args=(sock))
        iThread.daemon = True
        iThread.start()

        while True:
            data =  sock.recv(1024)
            if data:
                break    
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data, 'utf-8'))
    
    def sendMsg(self, sock):
        while True:
            sock.send(bytes(input(''), 'utf-8'))
    
    def updatePeers(self, peerData):
        p2p.peer = str(peerData, 'utf-8').split(',')[:-1]

class Peer:
    peers = ['127.0.0.1']

if __name__ == "__main__":
    while True:
        try:
            print('trying to connect...')
            time.sleep(randint(1,5))
            for peer in p2p.peers:
                try:
                    client = Client(peer)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass
                try:
                    server = Server()
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    print('Couldnt start the server...')
        except KeyboardInterrupt:
            sys.exit(0)

