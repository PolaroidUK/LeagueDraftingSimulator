import tkinter as tk
from functools import partial

import networking


def getChampions():
    return ['Aatrox', "Urgot", "Xayah", "Rakan", "Kalista", "Reksai", "Vayne", "Gangplank", "Thresh", "Hecarim",
            "Taric", "Lee_Sin", "Akali", "Velkoz", "Varus", "Zilean", "Vi", "Ahri", "Viktor", "Sivir", "Alistar",
            "Amumu", "Anivia", "Annie", "Aphelios", "Ashe", "Aurelion", "Azir", "Bard", "Blitzcrank", "Brand", "Braum",
            "Caitlyn", "Camille", "Cassiopeia", "ChoGath", "Corki", "Darius", "Diana", "Draven", "DrMundo", "Ekko",
            "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Garen", "Gnar", "Gragas", "Graves",
            "Heimerdinger", "Illaoi", "Irelia", "Ivern", "Janna", "Jarvan", "Jhin", "Jinx", "KaiSa", "Karma", "Karthus",
            "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "KhaZix", "Kindred", "Kled", "KogMaw", "LeBlanc",
            "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "MasterYi",
            "MissFortune", "Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nocturne",
            "Nunu", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn", "Rammus", "Renekton",
            "Rengar", "Riven", "Rumble", "Ryze", "Sejuani", "Senna", "Sett", "Shaco", "Shen", "Shyvana", "Singed",
            "Sion", "Skarner", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "TahmKench", "Taliyah", "Talon", "Teemo",
            "Thresh", "Tristana", "Trundle", "Tryndamere", "TwistedFate", "Twitch", "Udyr", "Veigar", "Vladimir",
            "Warwick", "Wukong", "Xerath", "XinZhao", "Yasuo", "Yorick", "Yuumi", "Zac", "Zed", "Ziggs", "Zoe", "Zyra",
            "Samira", "Seraphine", "Yone"]

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        mergeSort(L)
        mergeSort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def launchGUI(root, host, person, champions):
    # first start the connection thread which maneges all the networking for the project
    ct = networking.connectionThread(host, champions)
    gm = GuiManager(champions, root, ct, person)
    ct.gm = gm
    ct.start()


class ButtonManager:
    buttonList = []
    currentPage = 0
    notChosenChamps = []
    searchInput = ""
    root = None
    ct = None

    def __init__(self, champions, root, ct):
        self.root = root
        self.ct = ct
        self.buttonList = self.loadButtons(champions, 0, self.searchInput, root, ct)
        self.notChosenChamps = champions

    def update(self):
        self.butttonList = self.loadButtons(self.notChosenChamps, self.currentPage, self.searchInput, self.root,
                                            self.ct)

    def remove(self, champ):
        self.notChosenChamps.remove(champ)
        self.currentPage = 0
        self.searchInput = ""
        self.update()

    def search(self, search):
        self.currentPage = 0
        self.searchInput = search
        self.update()

    def turnPageLeft(self):
        self.currentPage += -1
        self.searchInput = ""
        self.update()

    def turnPageRight(self):
        self.currentPage += 1
        self.searchInput = ""
        self.update()

    def loadButtons(self, champions, page, search, root, ct):
        pageSize = 20
        for widget in root.winfo_children():
            widget.destroy()
        l = []
        c = []
        searchLen = len(search)
        for champ in champions:
            champName = champ.name
            if champName[0:searchLen].capitalize() == search.capitalize():
                c.append(champ)
        k = len(c) - (page * pageSize)
        print(k)
        if not self.currentPage == 0:
            btn2 = tk.Button(root, text='<-', command=self.turnPageLeft)
            btn2.grid(row=3, column=0)
        if k > pageSize:
            if len(c) - ((page * pageSize) + (k)) == 0:
                btn1 = tk.Button(root, text='->', command=self.turnPageRight)
                btn1.grid(row=3, column=7)
            k = pageSize

        for i in range(k):
            l.append(tk.Button(root, text=c[i + (page * pageSize)].name, image=c[i + (page * pageSize)].icon,
                               command=partial(networking.switch, ct, champions[i + (page * pageSize)].name)))
            l[i].grid(row=int(i / 5) + 2, column=(i % 5) + 1)

        return l


class FrameManager:
    root = None
    frames = []
    bt = []
    rt = []
    bb = []
    rb = []
    labels = []
    person = None
    champions = []

    def __init__(self, root, person, champions):
        self.root = root
        for c in champions:
            self.champions.append(c)
        self.person = person
        self.labels.append(tk.Label(root, text="Blue Team"))
        self.labels.append(tk.Label(root, text="Red Team"))
        self.labels.append(tk.Label(root, text="Blue Ban"))
        self.labels.append(tk.Label(root, text="Red Ban"))
        self.labels[0].grid(row=0, column=2)
        self.labels[1].grid(row=2, column=2)
        self.labels[2].grid(row=4, column=2)
        self.labels[3].grid(row=6, column=2)

        for i in range(5):
            self.bt.append(tk.Label(root, image=person, text='person'))
            self.rt.append(tk.Label(root, image=person, text='person'))
            self.rb.append(tk.Label(root, image=person, text='person'))
            self.bb.append(tk.Label(root, image=person, text='person'))
            self.bt[i].grid(row=1, column=i)
            self.rt[i].grid(row=3, column=i)
            self.rb[i].grid(row=5, column=i)
            self.bb[i].grid(row=7, column=i)
        self.frames.append(self.bt)
        self.frames.append(self.rt)
        self.frames.append(self.bb)
        self.frames.append(self.rb)

    def add(self, champion, tracker):
        switcher = {
            0: 2,
            1: 3,
            2: 2,
            3: 3,
            4: 2,
            5: 3,
            6: 0,
            7: 1,
            8: 1,
            9: 0,
            10: 0,
            11: 1,
            12: 3,
            13: 2,
            14: 3,
            15: 2,
            16: 1,
            17: 0,
            18: 0,
            19: 1
        }
        pick = switcher.get(tracker)
        print("adding")
        for i in range(5):
            if self.frames[pick][i]['text'] == 'person':
                print("and adding")
                self.frames[pick][i]['text'] = 'champ'
                for c in self.champions:
                    print(champion.name + c.name)
                    if champion.name == c.name:
                        self.frames[pick][i]['image'] = c.icon
                        return


class GuiManager:
    root = None
    fm = None
    bm = None
    champions = []
    ct = None
    lt = None
    label = None
    searchBox = None

    def __init__(self, champions, root, ct, person):
        self.root = root
        self.ct = ct
        self.champions = champions
        self.label = tk.Label(root, text="waiting for connection")
        self.label.pack()
        self.searchBox = tk.Entry(root)
        self.searchBox.pack(side='top')

        searchButton = tk.Button(root, text='Search', command=lambda: self.bm.search(self.searchBox.get()))
        searchButton.pack(side='top')
        buttonFrame = tk.Frame(root)
        buttonFrame.pack()
        teamFrame = tk.Frame(root)
        teamFrame.pack()
        self.fm = FrameManager(teamFrame, person, champions)
        self.bm = ButtonManager(champions, buttonFrame, ct)
