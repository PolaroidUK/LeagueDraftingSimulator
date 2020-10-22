import tkinter as tk


class Champion:
    name = "Champion"
    icon = None

    def __init__(self, name):
        self.name = name
        self.icon = tk.PhotoImage(file='Icons/' + name + 'Square.png')
