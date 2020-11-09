import tkinter as tk
import util
import champion

root = tk.Tk()
champions = []
person = tk.PhotoImage(file='Icons/person_outline_black_192x192.png')
championNames = util.getChampions()
util.mergeSort(championNames)
championIcons = []
for champ in championNames:
    champions.append(champion.Champion(champ))
util.GUI(root,True,person,champions)

root.mainloop()