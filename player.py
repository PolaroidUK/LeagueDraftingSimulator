import tkinter as tk
import UI
import champion

root = tk.Tk()

# load place holders and champion objects
champions = []
person = tk.PhotoImage(file='Icons/person_outline_black_192x192.png')
championNames = UI.getChampions()
UI.mergeSort(championNames)
championIcons = []
for champ in championNames:
    champions.append(champion.Champion(champ))

# launch the GUI which then launches a connection if host variable is true
UI.launchGUI(root, False, person, champions)

root.mainloop()
