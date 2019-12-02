from socket import *
import time


class Client():
    def __init__(self, nick, ip, port, room):
        self.nick = nick
        self.ip = ip
        self.port = port
        self.room = room
        self.reqEntry = False  # Este atributo indice se outra thread requisitou input
        self.entry = ''  # Indica o input requisitado

    def sendText(self, text, dic, blackList):
        '''Recebe um texto e um dicionário contendo pessoas. Envia o texto para cada pessoa do dicionário'''
        for person in dic:
            if person not in blackList:
                host, port = dic[person][0], dic[person][1]
                socket_ = socket(AF_INET, SOCK_STREAM)
                socket_.connect((host, port))
                socket_.send(str(self.port).encode())
                time.sleep(0.1)
                socket_.send('text'.encode())
                time.sleep(0.1)
                socket_.send(text.encode())

    def chatPeer(self):
        entry = ''
        print('Siga as instruções:'
              '\nPara enviar uma mensagem para toda a sala -> /all msg '
              '\nPara enviar uma mensagem privada para algum membro -> /nick msg '
              '\nPara visualizar a lista de integrantes da sala -> /members'
              '\nPara sair da sala -> /sair')
        while entry != '/sair':
            entry = input('')
            if entry[0:4] == '/all':
                self.sendText(entry[5:], self.room.members, [self.nick])
            elif entry[0:5] == '/nick':
                pass
            elif entry[0:9] == '/members':
                pass
            elif entry[0:5] == '/sair':
                pass
            elif self.reqEntry:
                self.entry = entry
                self.reqEntry = False
            else:
                print('Comando inválido!!')


    def updateRoom(self, type, nick, ip, port):
        '''Manda atualizações da sala para todos os membros'''
        # Incompleta
        if type == 'add':
            for person in self.room.members:
                if person != nick:
                    ipMember, portMember = self.room.members[person][0], self.room.members[person][1]
                    socket_ = socket(AF_INET, SOCK_STREAM)
                    socket_.connect((ipMember, portMember))
                    socket_.send(str(self.port).encode())
                    time.sleep(0.1)
                    socket_.send('update'.encode())
                    time.sleep(0.1)
                    socket_.send('add'.encode())
                    time.sleep(0.1)
                    socket_.send(nick.encode())
                    time.sleep(0.1)
                    socket_.send(ip.encode())
                    time.sleep(0.1)
                    socket_.send(str(port).encode())
