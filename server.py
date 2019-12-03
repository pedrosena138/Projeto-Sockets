from socket import *
import threading
import time

class Connection(threading.Thread):
    def __init__(self, connection, room, senderIP, senderPort, myself, myClient, lock):
        threading.Thread.__init__(self)
        self.connection = connection  # Conexão aberta
        self.room = room  # Sala
        self.lock = lock

        self.senderIP = senderIP  # Ip do cliente que abriu a conexão
        self.senderPort = senderPort  # Porta do cliente

        self.myNick = myself[0]  # Nick do peer servidor
        self.myIP = myself[1]  # Ip do peer servidor
        self.myPort = myself[2]  # Porta do peer servidor
        self.myClient = myClient  # Objeto cliente do peer servidor

    def run(self):
        try:
            data = self.connection.recv(1024)  # Este dado é referente ao tipo de mensagem que o cliente quer enviar
            if data:
                data = str(data, 'UTF-8')
                self.lock.acquire()
                if data == 'request':  # Se for um request, ele está querendo entrar na sala
                    adm = (self.room.nickADM == self.myNick and self.room.ipADM == self.myIP and self.room.portADM == self.myPort)
                    if adm:  # Se este servidor for adm da sala
                        nickSender = str(self.connection.recv(1024), 'UTF-8')  # Recebe o nick do cliente
                        print(f'O usuário {nickSender} com ip {self.senderIP} e porta {self.senderPort} está pedindo para entrar na sala'
                        '\nDeseja aceitar a requisição? ')
                        self.myClient.reqEntry = True
                        while self.myClient.reqEntry:
                            pass
                        answer = self.myClient.entry
                        if answer.lower() in ['y', 'yes', 'sim', 's']:
                            print(f'{nickSender} entrou na sala.')
                            # Insere o cliente na sala e envia todas as informações a respeito da sala para ele
                            self.room.queueADM.append(nickSender)
                            self.room.members[nickSender] = (self.senderIP, self.senderPort)
                            self.room.ips[(self.senderIP, self.senderPort)] = nickSender
                            self.myClient.updateRoom('add', nickSender, self.senderIP, self.senderPort)
                            self.connection.sendall('Voce foi aceito na sala'.encode())
                            time.sleep(0.01)
                            self.connection.sendall(self.room.roomName.encode())
                            time.sleep(0.01)
                            self.connection.sendall(self.room.nickADM.encode())
                            time.sleep(0.01)
                            self.connection.sendall(self.room.ipADM.encode())
                            time.sleep(0.01)
                            self.connection.sendall(str(self.room.portADM).encode())
                            time.sleep(0.01)

                            self.connection.sendall(str(len(self.room.queueADM)).encode())
                            time.sleep(0.01)
                            for member in self.room.queueADM:
                                self.connection.sendall(member.encode())  # nick
                                time.sleep(0.01)

                            self.connection.sendall(str(len(self.room.members)).encode())
                            time.sleep(0.01)
                            for member in self.room.members:
                                self.connection.sendall(member.encode())  # nick
                                time.sleep(0.01)
                                self.connection.sendall(self.room.members[member][0].encode())  # ip
                                time.sleep(0.01)
                                self.connection.sendall(str(self.room.members[member][1]).encode())  # port
                                time.sleep(0.01)

                            self.connection.sendall(str(len(self.room.ips)).encode())
                            time.sleep(0.01)
                            for ip in self.room.ips:
                                self.connection.sendall(ip[0].encode())  # ip
                                time.sleep(0.01)
                                self.connection.sendall(str(ip[1]).encode())  # port
                                time.sleep(0.01)
                                self.connection.sendall(self.room.ips[ip].encode())  # nick
                                time.sleep(0.01)

                            self.connection.sendall(str(len(self.room.ban)).encode())
                            time.sleep(0.01)
                            for person in self.room.ban:
                                self.connection.sendall(person[1].encode())  # ip
                                time.sleep(0.01)
                                self.connection.sendall(str(person[2]).encode())  # port
                        else:
                            print('Deseja bani-lo?')
                            self.myClient.reqEntry = True
                            while self.myClient.reqEntry == True:
                                pass
                            answer = self.myClient.entry
                            if answer.lower() in ['y', 'yes', 's', 'sim']:
                                self.room.ban.append((self.senderIP, self.senderPort))
                                self.myClient.updateRoom('ban request', nickSender, self.senderIP, self.senderPort)
                                print(f'Você baniu o usuário de ip {self.senderIP} e porta {self.senderPort}')
                                self.connection.sendall('Seu pedido foi recusado e você foi banido'.encode())
                            else:
                                self.connection.sendall('Recusada, o ADM nao permitiu a sua entrada'.encode())
                    else:
                        self.connection.sendall('Nao sou o adm da sala'.encode())
                elif data == 'text':  # Se for um 'text', basta printar na tela
                    if (self.senderIP, self.senderPort) in self.room.ips:
                        nickSender = self.room.ips[(self.senderIP, self.senderPort)]
                        print(f'{nickSender}: ' + str(self.connection.recv(1024), 'UTF-8'))
                elif data == 'update':  # Se for um update, recebe os dados e atualiza o seu objeto room
                    data = str(self.connection.recv(1024), 'UTF-8')
                    nick = str(self.connection.recv(1024), 'UTF-8')
                    ip = str(self.connection.recv(1024), 'UTF-8')
                    port = int(str(self.connection.recv(1024), 'UTF-8'))
                    if data == 'add':
                        if nick != self.myNick:
                            self.room.queueADM.append(nick)
                            self.room.members[nick] = (ip, port)
                            self.room.ips[(ip, port)] = nick
                            print(f'{nick} entrou na sala.')
                    elif data == 'remove':
                        self.room.members.pop(nick)
                        self.room.ips.pop((ip, port))
                        self.room.queueADM.remove(nick)
                        if nick != self.myNick:
                            print(f'{nick} foi removido da sala.')
                        else:
                            print('Você foi removido da sala.')
                            self.myClient.running = False
                    elif data == 'Disconnected':
                        self.room.members.pop(nick)
                        self.room.ips.pop((ip, port))
                        self.room.queueADM.remove(nick)
                        print(f'O usuário {nick} foi desconectado')
                    elif data == 'sair':
                        self.room.members.pop(nick)
                        self.room.ips.pop((ip, port))
                        try:  # Se fosse um adm daria erro, pois adm não fica nesta lista
                            self.room.queueADM.remove(nick)
                        except:
                            pass
                        print(f'{nick} saiu da sala.')
                    elif data == 'ban request':
                        self.room.ban.append((ip, port))
                    else:
                        self.room.members.pop(nick)
                        self.room.ips.pop((ip, port))
                        self.room.ban.append((ip, port))
                        self.room.queueADM.remove(nick)
                        if nick != self.myNick:
                            print(f'{nick} foi banido da sala.')
                        else:
                            print('Você foi banido da sala!')
                            self.myClient.banned = True
                time.sleep(0.4)
                self.lock.release()
        except:
            pass
        self.connection.close()


class Server(threading.Thread):
    def __init__(self, nick, host, port, room, myClient, lock):
        threading.Thread.__init__(self)
        self.nick = nick
        self.host = host
        self.port = port
        self.room = room
        self.myClient = myClient
        self.lock = lock

    def run(self):
        socket_ = socket(AF_INET, SOCK_STREAM)
        socket_.bind((self.host, self.port))
        socket_.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        socket_.listen(5)
        while True:
            connection, sender = socket_.accept()
            # print(f'Connected to client {sender}')
            senderIP = sender[0]
            senderPort = int(str(connection.recv(1024), 'UTF-8'))
            if (senderIP, senderPort) not in self.room.ban:
                myself = (self.nick, self.host, self.port)
                threadConnection = Connection(connection, self.room, senderIP, senderPort, myself, self.myClient,
                                              self.lock)
                threadConnection.daemon = True
                threadConnection.start()
