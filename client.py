import socket
import threading
import tkinter as tk
import networking
from threading import *

clientTurn = False


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


class connectionThread(threading.Thread):
    sent = True
    yourTurn = False
    message = "no champion"
    chosen = False
    listening = True

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("connection thread running")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), 1234))
        while True:
            #if not self.yourTurn:
               # label['text'] = "Opponent turn"
               # print("ready to recieve")
              #  receive_with_echo(s)
             #   self.yourTurn = True
               # print("sent it back")
           # else:
               # print("my turn")
               # label['text'] = "your turn"
               # if not self.sent:
                   # send_with_echo(s, self.message)
                    # s.send(bytes("I chose "+self.message, "utf-8"))
                    # print("waiting for echo")
                    # msg = s.recv(1024)

                   # self.sent = True
                  #  self.yourTurn = False

            if self.chosen:
                networking.send_move(s, self.message)

                self.yourTurn = False
                self.chosen = False
                self.listening = True
                label['text'] = "Opponent turn"

            elif self.listening:
                removeButton(networking.receive_move(s))
                print("choosing")
                self.yourTurn = True
                self.listening = False
                label['text'] = "your turn"

            # if something needs to send
            # send
            # get echo
            #  then if it is their turn
            #     tell them its their turn
            #  get echo
            #   wait for wait for their pick
            # return the echo

            # if not msg:
            #   print("nothing")
            #    cLabel['text'] = "nothing"
            # elif msg.decode('utf-8') == "":
            #   cLabel['text'] = "nothhintt:"+msg.decode('utf-8')
        # else:
        #   lt.yourTurn = False
        #  cLabel['text'] = "something:" + msg.decode('utf-8')


def switch(champ):
    print("click")
    if ct.yourTurn:
        # lt.yourTurn = False
        ct.message = champ
        removeButton(champ)
        ct.chosen = True
        print("sending")
    else:
        # lt.yourTurn = True
        print("not sending")
        # ct.yourTurn = True


root = tk.Tk()
label = tk.Label(root, text="player")
label.pack()
cLabel = tk.Label(root, text="Oppenent Turn")
cLabel.pack()
ct = connectionThread()
ct.start()
abutton = tk.Button(root, text='Aatrox', command=lambda: switch("Aatrox"))
abutton.pack()
bbutton = tk.Button(root, text='Urgot', command=lambda: switch("Urgot"))
bbutton.pack()
cbutton = tk.Button(root, text='Sion', command=lambda: switch("Sion"))
cbutton.pack()
dbutton = tk.Button(root, text='Xayah', command=lambda: switch("Xayah"))
dbutton.pack()
root.mainloop()
