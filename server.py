from socket import *
import threading
import time


class Connection(threading.Thread):
    def __init__(self, connection, room, senderIP, senderPort, myself, myClient):
        threading.Thread.__init__(self)
        self.connection = connection  # Conexão aberta
        self.room = room  # Sala

        self.senderIP = senderIP  # Ip do cliente que abriu a conexão
        self.senderPort = senderPort  # Porta do cliente

        self.myNick = myself[0]  # Nick do peer servidor
        self.myIP = myself[1]  # Ip do peer servidor
        self.myPort = myself[2]  # Porta do peer servidor
        self.myClient = myClient  # Objeto cliente do peer servidor

    def run(self):
        while True:
            data = self.connection.recv(1024)  # Este dado é referente ao tipo de mensagem que o cliente quer enviar
            if data:
                data = str(data, 'UTF-8')

                if data == 'request':  # Se for um request, ele está querendo entrar na sala
                    adm = (self.room.nickADM == self.myNick and self.room.ipADM == self.myIP and self.room.portADM == self.myPort)
                    if adm:  # Se este servidor for adm da sala
                        nickSender = str(self.connection.recv(1024), 'UTF-8')  # Recebe o nick do cliente
                        print(
                            f'O usuário {nickSender} com ip {self.senderIP} e porta {self.senderPort} está pedindo para entrar na sala\nDeseja aceitar a requisição? ')
                        self.myClient.reqEntry = True
                        while self.myClient.reqEntry == True:
                            pass
                        answer = self.myClient.entry
                        if answer.lower() in ['y', 'yes', 'sim', 's']:
                            # Insere o cliente na sala e envia todas as informações a respeito da sala para ele
                            self.room.members[nickSender] = (self.senderIP, self.senderPort)
                            self.room.ips[(self.senderIP, self.senderPort)] = nickSender
                            self.myClient.updateRoom('add', nickSender, self.senderIP, self.senderPort)
                            self.connection.send('Voce foi aceito na sala'.encode())
                            time.sleep(0.1)
                            self.connection.send(self.room.roomName.encode())
                            time.sleep(0.1)
                            self.connection.send(self.room.nickADM.encode())
                            time.sleep(0.1)
                            self.connection.send(self.room.ipADM.encode())
                            time.sleep(0.1)
                            self.connection.send(str(self.room.portADM).encode())
                            time.sleep(0.1)

                            self.connection.send(str(len(self.room.members)).encode())
                            time.sleep(0.1)
                            for member in self.room.members:
                                self.connection.send(member.encode())  # nick
                                time.sleep(0.1)
                                self.connection.send(self.room.members[member][0].encode())  # ip
                                time.sleep(0.1)
                                self.connection.send(str(self.room.members[member][1]).encode())  # port
                                time.sleep(0.1)

                            self.connection.send(str(len(self.room.ips)).encode())
                            time.sleep(0.1)
                            for ip in self.room.ips:
                                self.connection.send(ip[0].encode())  # ip
                                time.sleep(0.1)
                                self.connection.send(str(ip[1]).encode())  # port
                                time.sleep(0.1)
                                self.connection.send(self.room.ips[ip].encode())  # nick
                                time.sleep(0.1)

                            self.connection.send(str(len(self.room.ban)).encode())
                            time.sleep(0.1)
                            for person in self.room.ban:
                                self.connection.send(person[0].encode())  # nick
                                time.sleep(0.1)
                                self.connection.send(person[1].encode())  # ip
                                time.sleep(0.1)
                                self.connection.send(str(person[2]).encode())  # port
                        else:
                            self.connection.send('Recusada, o ADM nao permitiu a sua entrada'.encode())
                    else:
                        self.connection.send('Nao sou o adm da sala'.encode())
                elif data == 'text':  # Se for um 'text', basta printar na tela
                    nickSender = self.room.ips[(self.senderIP), self.senderPort]
                    print(f'{nickSender}: ' + str(self.connection.recv(1024), 'UTF-8'))
                elif data == 'update':  # Se for um update, recebe os dados e atualiza o seu objeto room
                    data = str(self.connection.recv(1024), 'UTF-8')
                    if data == 'add':
                        nick = str(self.connection.recv(1024), 'UTF-8')
                        ip = str(self.connection.recv(1024), 'UTF-8')
                        port = int(str(self.connection.recv(1024), 'UTF-8'))
                        self.room.members[nick] = (ip, port)
                        self.room.ips[(ip, port)] = nick



class Server(threading.Thread):
    def __init__(self, nick, host, port, room, myClient):
        threading.Thread.__init__(self)
        self.nick = nick
        self.host = host
        self.port = port
        self.running = 1
        self.room = room
        self.myClient = myClient

    def run(self):
        socket_ = socket(AF_INET, SOCK_STREAM)
        socket_.bind((self.host, self.port))
        socket_.listen(1)
        while self.running:
            connection, sender = socket_.accept()
            # print(f'Connected to client {sender}')
            senderIP = sender[0]
            senderPort = int(str(connection.recv(1024), 'UTF-8'))
            myself = (self.nick, self.host, self.port)
            threadConnection = Connection(connection, self.room, senderIP, senderPort, myself, self.myClient)
            threadConnection.start()
