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
        self.maps = listFiles("./Map Files/")
        self.pop_maps = listCSV("maps.csv")

        def searchAction():
            self.frame.destroy()
            term = textInput.get()
            result = search(self.pop_maps, term)
            self.frame = self.downloadMapsTable(result)
            self.frame.pack(padx=10, pady=80)

        def changeFrame(load_func):
            self.frame.destroy()
            self.frame = load_func
            self.frame.pack(padx=10, pady=80)

        self.frame = self.loadMapsTable()
        textInput = Entry(self.root, width=30, borderwidth=5)
        searchButton = Button(self.root, text="Search", padx=20, command=searchAction)

        yourMapsButton = Button(self.root, text="Your Maps", padx=20,
            command=lambda: changeFrame(self.loadMapsTable()))
        popularMapsButton = Button(self.root, text="Popular Maps", padx=20,
            command=lambda: changeFrame(self.downloadMapsTable(self.pop_maps)))

        downloadInput = Entry(self.root, width=70, borderwidth=5)
        downloadButton = Button(self.root, text="Download", padx=20,
            command=lambda: downloadMap(downloadInput.get()))

        self.frame.pack(padx=10, pady=80)

        downloadInput.place(relx=0.43, rely=0.09, anchor="n")
        downloadButton.place(relx=0.9, rely=0.09, anchor="ne")

        textInput.place(relx=0.01, rely=0.01, anchor="nw")
        searchButton.place(relx=0.29, rely=0.01, anchor="nw")

        yourMapsButton.place(relx=0.8, rely=0.01, anchor="ne")
        popularMapsButton.place(relx=0.99, rely=0.01, anchor="ne")

    def loadMapsTable(self):
        self.RL_PATH = r'E:\Rocket\rocketleague\TAGame\CookedPCConsole'
        self.maps = listFiles("./Map Files/")
        frame = LabelFrame(self.root, text="Maps", padx=5, pady=5)

        buttons = []
        for i in range(len(self.maps)):
            for j in range(len(self.maps[i])):
                l = Label(frame, text=self.maps[i][j], padx=50)
                l.grid(row=i, column=j)
        
            buttons.append(Button(frame, text="Load", padx=50,
                command=lambda file=self.maps[i][0]: loadMap(self.RL_PATH, file)))
            buttons[i].grid(row=i, column=2)

        return frame

    def downloadMapsTable(self, maps):
        frame = LabelFrame(self.root, text="Popular Worshop Maps", padx=5, pady=5)

        buttons = []
        for i in range(len(maps)):
            for j in range(len(maps[i])):
                frame.columnconfigure(j, minsize=100)
                l = Label(frame, text=maps[i][j])
                l.grid(row=i, column=j)
        
            buttons.append(Button(frame, text="Download", padx=10,
                command=lambda map_id=maps[i][2]: downloadMap(map_id)))
            buttons[i].grid(row=i, column=3)

        return frame


def search(map_list, term):
    result = []
    for file_name in map_list:
        if term.lower() in file_name[0].lower():
            result.append(file_name)
    return result

def listFiles(directory):
    maps = []
    for file in os.listdir(directory):
        if file.endswith(".udk"):
            size = os.path.getsize(f"{directory}{file}")
            maps.append([file, f"{round(size / 1000000, 2)} MB"])
    return maps

def listCSV(file):
    maps = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            maps.append(row)
    return maps


if __name__ == "__main__":
    MyApp()