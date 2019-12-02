import threading

'''
class CheckADM(threading.Thread):
    def __init__(self, room):
        threading.Thread.__init__(self)
        self.room = room
        self.adm = self.room.nickADM
        self.members = self.room.members

    def run(self):
        while True:
            time.sleep(5)
            try:
                socket_ = socket(AF_INET, SOCK_STREAM)
                hostADM, portADM = self.room.members[self.adm]
                socket_.connect((hostADM, int(portADM)))
            except:
                self.changeADM()

    def changeADM(self):
        self.members.pop(self.adm)
        newADM = list(self.members.keys())[0]
        self.room.nickADM = newADM
        self.room.ipADM = self.room.members[newADM][0]
        self.room.portADM = self.room.members[newADM][1]
'''

class Room():
    def __init__(self, roomName, nickADM, ipADM, portADM, members={}, ips={}, ban=[]):
        self.roomName = roomName  # Nome da sala
        self.nickADM = nickADM  # Nick do adm da sala
        self.ipADM = ipADM  # Ip do adm da sala
        self.portADM = portADM  # Porta do adm da sala
        self.members = members if members != {} else {nickADM: (ipADM, portADM)}  # Dicionário com membros da sala -> nick: (ip,porta)
        self.ips = ips if ips != {} else {(ipADM,portADM): nickADM}  # Dicionário com membros da sala -> (ip,porta): nick
        self.ban = ban  # Lista de pessoas banidas da sala

