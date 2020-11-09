import socket
import threading
import tkinter as tk
import networking
from threading import *

def removeButton(champ):
    if champ == "Aatrox":
        abutton.forget()
    elif champ == "Urgot":
        bbutton.forget()
    elif champ == "Sion":
        cbutton.forget()
    elif champ == "Xayah":
        dbutton.forget()
    return
class labelThread(threading.Thread):
    yourTurn = False

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self.yourTurn:
                label['text'] = "opponent turn"
            else:
                label['text'] = "your turn"


class connectionThread(threading.Thread):
    yourTurn = True
    sent = True
    message = "no champion"
    chosen = False
    listening = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(5)
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        print("connection thread running")

        while True:
            label['text'] = "waiting for connection"
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = self.s.accept()
            print(f"Connection from {address} has been established.")
            label['text'] = "your turn"
            while True:
                #print(self.sent)
                if self.chosen:
                    networking.send_move(clientsocket, self.message)
                    self.yourTurn = False
                    self.chosen = False
                    self.listening = True
                    label['text'] = "Opponent turn"
                elif self.listening:
                    removeButton(networking.receive_move(clientsocket))
                    print("choosing")
                    self.yourTurn = True
                    self.listening = False
                    label['text'] = "your turn"

               # if not self.yourTurn:
                    #print("sending 1")
                 #   label['text'] = "opponent turn"
                 #   print("waiting for opponent to move")
                  #  msg = clientsocket.recv(1024)
                 #   if not msg:
                 #       break
                 #   print(msg)
                #    clientsocket.send(msg)
                #    self.yourTurn = True
                #    print("got somthing")
                #    #clientsocket.send(bytes("", "utf-8"))
             #   else:
                    #print("sending 3")
                 #   label['text'] = "your turn"
                    #clientsocket.send(bytes("3", "utf-8"))
                 #   if not self.sent:
                  #      clientsocket.send(bytes("I chose "+self.message, "utf-8"))
                  #      print("waiting for echo")
                  #      msg = clientsocket.recv(1024)
                  #      if not msg:
                   #         break
                   #     print(msg)
                   #     self.sent = True


            # clientsocket.close()


def switch(ct,champ):
    print("click")

    if ct.yourTurn:
        ct.message = champ
        ct.chosen = True
        removeButton(champ)
        print("sending")
    else:
        #lt.yourTurn = True
        print("not sending")
        #ct.yourTurn = True


root = tk.Tk()
label = tk.Label(root, text="waiting for connection")
label.pack()
ct = connectionThread()
ct.start()
abutton = tk.Button(root, text='Aatrox', command=lambda: switch(ct,"Aatrox"))
abutton.pack()
bbutton = tk.Button(root, text='Urgot', command=lambda: switch(ct,"Urgot"))
bbutton.pack()
cbutton = tk.Button(root, text='Sion', command=lambda: switch(ct,"Sion"))
cbutton.pack()
dbutton = tk.Button(root, text='Xayah', command=lambda: switch(ct,"Xayah"))
dbutton.pack()
root.mainloop()
