import os
import csv
from os import listdir
from tkinter import *
from main import loadMap, downloadMap


class MyApp:
    def __init__(self):
        self.root = Tk(className="Rocket League Workshop")
        self.root.geometry("700x500")
        self.initUI()
        self.root.mainloop()

    def initUI(self):
        frame = self.downloadMapsTable()
        text_input = Entry(self.root, width=30, borderwidth=5)
        loadMapButton = Button(self.root, text="Load Map", padx=20)
        downloadButton = Button(self.root, text="Download Map", padx=20)

        frame.pack(padx=10, pady=35)
        text_input.place(relx=0.01, rely=0.01, anchor="nw")
        loadMapButton.place(relx=0.8, rely=0.01, anchor="ne")
        downloadButton.place(relx=0.99, rely=0.01, anchor="ne")

    def loadMapsTable(self):
        self.RL_PATH = r'E:\Rocket\rocketleague\TAGame\CookedPCConsole'
        maps = self.listFiles("./Map Files/")
        frame = LabelFrame(self.root, text="Maps", padx=5, pady=5)

        buttons = []
        for i in range(len(maps)):
            for j in range(len(maps[i])):
                l = Label(frame, text=maps[i][j], padx=50)
                l.grid(row=i, column=j)
        
            buttons.append(Button(frame, text="Load", padx=50,
                command=lambda file=maps[i][0]:loadMap(self.RL_PATH, file)))
            buttons[i].grid(row=i, column=2)

        return frame

    def downloadMapsTable(self):
        maps = self.listCSV("maps.csv")
        frame = LabelFrame(self.root, text="Popular Worshop Maps", padx=5, pady=5)

        buttons = []
        for i in range(len(maps)):
            for j in range(len(maps[i])):
                frame.columnconfigure(j, minsize=100)
                l = Label(frame, text=maps[i][j])
                l.grid(row=i, column=j)
        
            buttons.append(Button(frame, text="Download", padx=10,
                command=lambda map_id=maps[i][2]:downloadMap(map_id)))
            buttons[i].grid(row=i, column=3)

        return frame

    @staticmethod
    def listFiles(directory):
        maps = []
        for file in os.listdir(directory):
            if file.endswith(".udk"):
                size = os.path.getsize(f"{directory}{file}")
                maps.append([file, f"{round(size / 1000000, 2)} MB"])
        return maps

    @staticmethod
    def listCSV(file):
        maps = []
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                maps.append(row)
        return maps


if __name__ == "__main__":
    MyApp()