import os
from os import listdir
from tkinter import *
from main import loadMap, downloadMap


class MyApp:
    def __init__(self):
        self.root = Tk(className="My Window")
        self.root.geometry("700x500")
        self.initUI()
        self.root.mainloop()

    def initUI(self):
        frame = self.makeTable()
        text_input = Entry(self.root, width=30, borderwidth=5)
        loadMapButton = Button(self.root, text="Load Map", padx=20)
        downloadButton = Button(self.root, text="Download Map", padx=20)

        frame.pack(padx=10, pady=30)
        text_input.place(anchor="nw")
        loadMapButton.place(relx=0.8, y=0, anchor="ne")
        downloadButton.place(relx=1, y=0, anchor="ne")

    def makeTable(self):
        maps = self.listFiles("./Map Files/")
        frame = LabelFrame(self.root, text="Maps", padx=5, pady=5)

        def load(map_title):
            load = loadMap(r'E:\Rocket\rocketleague\TAGame\CookedPCConsole', map_title)
            load.load_map()

        buttons = []
        for i in range(len(maps)):
            for j in range(len(maps[i])):
                l = Label(frame, text=maps[i][j], padx=50)
                l.grid(row=i, column=j)
            map_file = maps[i][0]
            buttons.append(Button(frame, text="Load", padx=50, command=lambda file=maps[i][0]:load(file)))
            buttons[i].grid(row=i, column=2)

        return frame

    @staticmethod
    def listFiles(directory):
        maps = []
        for file in os.listdir(directory):
            if file.endswith(".udk"):
                size = os.path.getsize(f"{directory}{file}")
                maps.append([file, f"{round(size / 1000000, 2)} MB"])
        return maps

if __name__ == "__main__":
    MyApp()