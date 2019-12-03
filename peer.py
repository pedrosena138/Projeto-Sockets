from server import *
from room import *
from client import *
import time

def startPeer():
    global lock  # Variável utilizada para processar separadamente os pedidos na thread do servidor, evitando conflitos
    nick = input("Olá, qual é o seu nome? ")  # Nick do peer
    host = input(f'Qual é o seu ip, {nick}? ')  # Ip do peer
    port = int(input('Qual é a sua porta? '))  # Porta do peer
    firstEntry = True  # Variável utilizada para criar o servidor apenas na primeira iteração, pois ao abrir outro servidor com a mesma porta um erro é gerado
    cmd = ''
    roomsBanned = []  # Lista de salas em que o cliente foi banido, evitando requests desnecessários
    while cmd != '3':
        cmd = input(
            "\nBem-vindo ao nosso app de mensagem, digite: \n1 - Se deseja criar uma sala\n2 - Se deseja se conectar a "
            "uma sala\n3 - Para sair\n")
        if cmd == '1':  # Criar sala
            roomName = input('Qual será o nome da sala? ')
            room = Room(roomName, nick, host, port)
            adm = True
            client = Client(nick, host, port, adm, room)  # Cliente é uma classe normal
            if firstEntry:
                server = Server(nick, host, port, room, client, lock)  # Server é uma thread
                server.start()
                firstEntry = False
            else:
                server.myClient = client  # A partir da segunda iteração no menu, somente o objeto client e a room são atualizados, já que o server foi inicializado anteriormente
                server.room = room

            print(f'Sua sala foi criada no endereço {host} e porta {port}!!')
            time.sleep(0.01)
            chekingMembers = CheckMembers(room, client)  # Nesta thread, o adm checa continuamente se algum membro foi desconectado
            chekingMembers.start()
            client.chatPeer()

        elif cmd == '2':
            roomIP = input('Qual é o IP da sala? ')  # Ip do adm da sala
            roomPort = int(input('Qual é a porta da sala? '))  # Porta do adm da sala
            if (roomIP, roomPort) in roomsBanned:
                print('Você está banido desta sala!')
            else:
                try:
                    socket_ = socket(AF_INET, SOCK_STREAM)
                    socket_.connect((roomIP, roomPort))
                    socket_.sendall(str(int(port)).encode())  # Envia sua porta para ser cadastrada caso o peer seja aceito na sala
                    time.sleep(0.01)

                    socket_.sendall(
                        'request'.encode())  # Envia 'request' para indicar que o peer quer fazer uma requisição para entrar na sala
                    print('Conectando...')
                    time.sleep(0.01)

                    socket_.sendall(nick.encode())  # Envia o seu nick para ser cadastrado na sala
                    answer = str(socket_.recv(1024), 'UTF-8')  # Resposta do servidor, se foi aceito ou não na sala
                    if answer == 'Voce foi aceito na sala':
                        print('Você entrou na sala!!')
                        # Todas as informações a seguir são da sala, enviadas pelo adm
                        roomName = str(socket_.recv(1024), 'UTF-8')
                        print('-'*40 + '\n' + f'Bem-vindo à sala {roomName}\n' + '-'*40)
                        nickADM = str(socket_.recv(1024), 'UTF-8')
                        ipADM = str(socket_.recv(1024), 'UTF-8')
                        portADM = int(str(socket_.recv(1024), 'UTF-8'))
                        qntQueueADM = int(str(socket_.recv(1024), 'UTF-8'))

                        queueADM = []
                        for i in range(qntQueueADM):
                            nickMember = str(socket_.recv(1024), 'UTF-8')
                            queueADM.append(nickMember)

                        qntMembers = int(str(socket_.recv(1024), 'UTF-8'))
                        members = {}
                        for i in range(qntMembers):
                            nickMember = str(socket_.recv(1024), 'UTF-8')
                            ipMember = str(socket_.recv(1024), 'UTF-8')
                            portMember = int(str(socket_.recv(1024), 'UTF-8'))
                            members[nickMember] = (ipMember, portMember)

                        qntIps = int(str(socket_.recv(1024), 'UTF-8'))
                        ips = {}
                        for i in range(qntIps):
                            ipMember = str(socket_.recv(1024), 'UTF-8')
                            portMember = int(str(socket_.recv(1024), 'UTF-8'))
                            nickMember = str(socket_.recv(1024), 'UTF-8')
                            ips[(ipMember, portMember)] = nickMember

                        qntBans = int(str(socket_.recv(1024), 'UTF-8'))
                        ban = []
                        for i in range(qntBans):
                            ipBan = str(socket_.recv(1024), 'UTF-8')
                            portBan = int(str(socket_.recv(1024), 'UTF-8'))
                            ban.append((ipBan, portBan))

                        room = Room(roomName, nickADM, ipADM, portADM, queueADM, members, ips,
                                    ban)  # Cria um objeto Room com os dados recebidos pelo adm da sala
                        adm = False
                        client = Client(nick, host, port, adm, room)  # Inicializa sua classe cliente com seus dados e a Room criada
                        if firstEntry:
                            server = Server(nick, host, port, room, client, lock)  # Inicializa a thread server
                            server.start()
                            firstEntry = False
                        else:
                            server.room = room
                            server.myClient = client

                        chekingADM = CheckADM(room, nick, client)  # Todos os usuários da sala checam continuamente se o adm não se desconectou de forma inesperada
                        chekingADM.start()
                        # A partir deste ponto o usuário já pode interagir com o chat
                        client.chatPeer()
                        # A partir deste ponto, o usuário saiu ou foi removido da sala
                        client.running = False
                        if client.banned:
                            roomsBanned.append((roomIP, roomPort))


                    elif answer == 'Recusada, o ADM nao permitiu a sua entrada':
                        print(answer)
                    else:  # Nesta condição, o adm da sala recusou e baniu o usuário de entrar na sala
                        roomsBanned.append((roomIP, roomPort))
                        print(answer)
                except:
                    print('Sala não encontrada')
        elif cmd == '3':
            pass
        else:
            print('Comando inválido\n')







lock = threading.Lock()
if __name__ == "__main__":
    startPeer()
