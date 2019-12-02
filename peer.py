from server import *
from room import *
from client import *
import time
import _thread


def startPeer():
    nick = input("Olá, qual é o seu nome? ")  # Nick do peer
    host = input(f'Qual é o seu ip, {nick}? ')  # Ip do peer
    port = int(input('Qual é a sua porta? '))  # Porta do peer
    cmd = input(
        "\nBem-vindo ao nosso app de mensagem, digite: \n1 - Se deseja criar uma sala\n2 - Se deseja se conectar a "
        "uma sala\n")

    if cmd == '1':  # Criar sala
        roomName = input('Qual será o nome da sala? ')
        room = Room(roomName, nick, host, port)
        client = Client(nick, host, port, room)  # Cliente é uma classe normal
        server = Server(nick, host, port, room, client)  # Server é uma thread
        server.start()

        print(f'Sua sala foi criada no endereço {host} e porta {port}!!')
        time.sleep(1)
        client.chatPeer()
        # checkingThread = CheckADM(room)  # Checagem se o adm saiu da sala (precisa ser pensada)
        # checkingThread.start()
    elif cmd == '2':
        roomIP = input('Qual é o IP da sala? ')  # Ip do adm da sala
        roomPort = int(input('Qual é a porta da sala? '))  # Porta do adm da sala

        socket_ = socket(AF_INET, SOCK_STREAM)
        socket_.connect((roomIP, roomPort))
        socket_.send(str(int(port)).encode())  # Envia sua porta para ser cadastrada caso o peer seja aceito na sala
        time.sleep(1)

        socket_.send(
            'request'.encode())  # Envia 'request' para indicar que o peer quer fazer uma requisição para entrar na sala
        print('Conectando...')
        time.sleep(1)

        socket_.send(nick.encode())  # Envia o seu nick para ser cadastrado na sala
        answer = str(socket_.recv(1024), 'UTF-8')  # Resposta do servidor, se foi aceito ou não na sala
        if answer == 'Voce foi aceito na sala':
            print('Você entrou na sala!!')
            # Todas as informações a seguir são da sala, enviadas pelo adm
            roomName = str(socket_.recv(1024), 'UTF-8')
            nickADM = str(socket_.recv(1024), 'UTF-8')
            ipADM = str(socket_.recv(1024), 'UTF-8')
            portADM = int(str(socket_.recv(1024), 'UTF-8'))
            qntMembers = int(str(socket_.recv(1024), 'UTF-8'))
            members = {}
            for i in range(qntMembers):
                nick = str(socket_.recv(1024), 'UTF-8')
                ip = str(socket_.recv(1024), 'UTF-8')
                port = int(str(socket_.recv(1024), 'UTF-8'))
                members[nick] = (ip, port)
            qntIps = int(str(socket_.recv(1024), 'UTF-8'))
            ips = {}
            for i in range(qntIps):
                ip = str(socket_.recv(1024), 'UTF-8')
                port = int(str(socket_.recv(1024), 'UTF-8'))
                nick = str(socket_.recv(1024), 'UTF-8')
                ips[(ip, port)] = nick

            qntBans = int(str(socket_.recv(1024), 'UTF-8'))
            ban = []
            for i in range(qntBans):
                nick = str(socket_.recv(1024), 'UTF-8')
                ip = str(socket_.recv(1024), 'UTF-8')
                port = int(str(socket_.recv(1024), 'UTF-8'))
                ban.append((nick, ip, port))

            room = Room(roomName, nickADM, ipADM, portADM, members, ips,
                        ban)  # Cria um objeto Room com os dados recebidos pelo adm da sala
            client = Client(nick, host, port, room)  # Inicializa sua classe cliente com seus dados e a Room criada
            server = Server(nick, host, port, room, client)  # Inicializa a thread server
            server.start()

            # A partir deste ponto o usuário já pode interagir com o chat
            client.chatPeer()






if __name__ == "__main__":
    startPeer()
