import socket
import threading
import tkinter


def trackerID(tracker, ispick):
    turnSwitcher = {
        0: 2,
        1: 3,
        2: 2,
        3: 3,
        4: 2,
        5: 3,
        6: 4,
        7: 5,
        8: 5,
        9: 4,
        10: 4,
        11: 5,
        12: 3,
        13: 2,
        14: 3,
        15: 2,
        16: 5,
        17: 4,
        18: 4,
        19: 5
    }
    listenSwitcher = {
        0: False,
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False,
        7: True,
        8: False,
        9: True,
        10: False,
        11: True,
        12: False,
        13: False,
        14: False,
        15: False,
        16: False,
        17: True,
        18: False,
        19: False
    }
    if ispick:
        id = turnSwitcher.get(tracker)
    else:
        id = listenSwitcher.get(tracker)

    return id


def removeButton( champ,champions,gm, tracker):
    for champs in champions:
        name = champs.name
        if name.capitalize() == champ.capitalize():
            champIcon = champs.icon
            gm.bm.remove(champs)
            gm.fm.add(champs, tracker)







def switch(ct, champ):
    if not ct.chosen:
        if not ct.listening:
            ct.currentChampion = champ
            ct.chosen = True


class connectionThread(threading.Thread):
    host = True
    currentChampion = "no champion"
    chosen = False
    listening = False
    s = None
    tracker = 0
    gm = None
    champions = []

    def __init__(self, host,champions):
        threading.Thread.__init__(self)
        self.host = host
        self.champions = champions
        if not host:
            self.listening = True
        else:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((socket.gethostname(), 1234))
            self.s.listen(5)

    def run(self):
        print("connection thread running")
        while True:
            if self.host:
                clientsocket, address = self.s.accept()
                print(f"Connection from {address} has been established.")
                self.gm.label['text'] = "Your turn"
            else:
                clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientsocket.connect((socket.gethostname(), 1234))
                self.gm.label['text'] = "Opponent turn"
            while True:

                if self.chosen:
                    clientsocket.send(bytes(self.currentChampion, "utf-8"))
                    clientsocket.recv(1024)
                    removeButton(self.currentChampion,self.champions,self.gm,self.tracker)
                    self.chosen = False
                    if not trackerID(self.tracker, False):
                        self.listening = True
                        self.gm.label['text'] = "Opponent turn"
                    self.tracker += 1


                elif self.listening:
                    msg = clientsocket.recv(1024)
                    if not self.currentChampion == msg.decode('utf-8'):
                        clientsocket.send(msg)
                        self.currentChampion = msg.decode('utf-8')
                        removeButton(self.currentChampion,self.champions,self.gm,self.tracker)

                        if not trackerID(self.tracker, False):
                            self.listening = False
                            self.gm.label['text'] = "Your turn"
                        self.tracker += 1



