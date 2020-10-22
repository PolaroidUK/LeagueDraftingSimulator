import tkinter as tk
from functools import partial
from champion import Champion

tracker = 0
blueTurn = True
ban = True
pick = 0
root = tk.Tk()

champions = []

champions.append(Champion('Aatrox'))
champions.append(Champion('Ahri'))
champions.append(Champion('Vayne'))
champions.append(Champion('Xayah'))
champions.append(Champion('Rakan'))

champions.append(Champion('Gangplank'))
champions.append(Champion('Urgot'))
champions.append(Champion('Lee_Sin'))
champions.append(Champion('Viktor'))
champions.append(Champion('Vi'))

champions.append(Champion('Sivir'))
champions.append(Champion('Zilean'))
champions.append(Champion('Varus'))
champions.append(Champion('Velkoz'))
champions.append(Champion('Akali'))

champions.append(Champion('Taric'))
champions.append(Champion('Hecarim'))
champions.append(Champion('Thresh'))
champions.append(Champion('Kalista'))
champions.append(Champion('Reksai'))


def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves

        mergeSort(L)  # Sorting the first half
        mergeSort(R)  # Sorting the second half

        i = j = k = 0
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i].name < R[j].name:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def printList(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()


mergeSort(champions)
cbtns = []
tally = 0
for champion in champions:
    cbtns.append(tally)
    tally = tally + 1

person = tk.PhotoImage(file='Icons/person_outline_black_192x192.png')


def pickTracker():
    global tracker
    global blueTurn
    global pick
    global ban
    if tracker > 20:
        print("over 20 turns")
        return
    switcher = {
        1: 0,
        2: 1,
        3: 1,
        4: 2,
        5: 2,
        6: 0,
        7: 0,
        8: 1,
        9: 1,
        10: 2,
        11: 2,
        12: 3,
        13: 3,
        14: 4,
        15: 4,
        16: 3,
        17: 3,
        18: 4,
        19: 4
    }
    pick = switcher.get(tracker)

    if tracker == 6:
        ban = False
    elif tracker == 12:
        ban = True
    elif tracker == 16:
        ban = False

    turnSwitcher = {
        0: True,
        1: False,
        2: True,
        3: False,
        4: True,
        5: False,
        6: True,
        7: False,
        8: False,
        9: True,
        10: True,
        11: False,
        12: False,
        13: True,
        14: False,
        15: True,
        16: False,
        17: True,
        18: True,
        19: False
    }
    blueTurn = turnSwitcher.get(tracker)


def test(champion, window):
    global tracker
    global blueTurn
    global pick
    if ban:
        if blueTurn:
            window.champsBB[pick]['image'] = champions[champion].icon
        else:
            window.champsRB[pick]['image'] = champions[champion].icon
    else:
        if blueTurn:
            window.champsL[pick]['image'] = champions[champion].icon
        else:
            window.champsR[pick]['image'] = champions[champion].icon
    tracker = tracker + 1
    pickTracker()
    cbtns.remove(champion)
    window.popuFrame("")


def search(ser):

    window1.popuFrame(ser)


class Window:
    canvas = None

    def __init__(self, canvas):
        self.canvas = canvas

    searchBox = tk.Entry(canvas)
    searchBox.pack(side='top')

    searchButton = tk.Button(canvas, text='Search', command=lambda: search(window1.searchBox.get()))
    searchButton.pack(side='top')
    frameT = tk.Frame(canvas)
    frameT.pack(side='top')
    frameL = tk.Frame(canvas)
    frameL.pack(side='left')
    champsL = [None] * 5
    frameR = tk.Frame(canvas)
    frameR.pack(side='right')
    champsR = [None] * 5
    frameBB = tk.Frame(canvas)
    frameBB.pack(side='bottom')
    champsBB = [None] * 5
    frameRB = tk.Frame(canvas)
    frameRB.pack(side='bottom')
    champsRB = [None] * 5

    for i in range(5):
        champsL[i] = tk.Label(frameL, text="Bchamp " + str(i), image=person)
        champsL[i].grid(row=i, column=0)
        champsR[i] = tk.Label(frameR, text="Rchamp " + str(i), image=person)
        champsR[i].grid(row=i, column=0)
        champsBB[i] = tk.Label(frameBB, text="Banchamp " + str(i), image=person)
        champsBB[i].grid(row=0, column=i)
        champsRB[i] = tk.Label(frameBB, text="Banchamp " + str(i), image=person)
        champsRB[i].grid(row=0, column=i + 5)

    def popuFrame(self, search):
        for widget in self.frameT.winfo_children():
            widget.destroy()
        if blueTurn:
            turnLabel = tk.Label(self.frameT, text="Your Turn")
        else:
            turnLabel = tk.Label(self.frameT, text="Opponent Turn")
        turnLabel.grid(row=1, column=2)
        buttons = []
        searchLen = len(search)
        print(searchLen)
        k = 0
        for i in range(len(cbtns)):

            champName = champions[cbtns[i]].name
            if champName[0:searchLen].capitalize() == search.capitalize():
                buttons.append(
                tk.Button(self.frameT, image=champions[cbtns[i]].icon, command=partial(test, cbtns[i], self)))
                buttons[k].grid(row=int(k / 5) + 2, column=k % 5)
                k+=1


window1 = Window(root)
window1.popuFrame("")
root.mainloop()
