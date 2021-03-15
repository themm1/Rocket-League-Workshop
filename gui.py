import os
import csv
import string
import webbrowser
from os import listdir
from tkinter import *
from tkinter import filedialog
from main import loadMap, downloadMap


class MyApp:
    def __init__(self):
        with open("rlpath.txt", "r") as f:
            self.RL_PATH = f.readline()
        self.maps = listFiles("./Map Files/")
        self.pop_maps = listCSV("maps.csv")
        self.current_maps = self.maps
        self.root = Tk(className="Rocket League Workshop")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.initUI()
        self.root.mainloop()

    def initUI(self):
        def searchAction():
            self.frame.destroy()
            term = textInput.get()
            result = search(self.current_maps, term)
            if len(self.current_maps[0]) == 2:
                self.frame = self.loadMapsTable(result)
            else:
                self.frame = self.downloadMapsTable(result)
            self.frame.pack(padx=10, pady=80)

        def changeFrame(load):
            self.frame.destroy()
            if load == True:
                self.current_maps = listFiles("./Map Files/")
                self.frame = self.loadMapsTable(self.current_maps)
            else:
                self.current_maps = self.pop_maps
                self.frame = self.downloadMapsTable(self.current_maps)
            self.frame.pack(padx=10, pady=80)

        def changeRL_PATH():
            rl_path = filedialog.askdirectory(initialdir="/", title="Select Rocket League Folder")
            rl_path = f"{rl_path}/TAGame/CookedPCConsole/"
            self.RL_PATH = r'{}'.format(rl_path.replace("/", "\\"))
            print(self.RL_PATH)
            with open("rlpath.txt", "w") as f:
                f.writelines(self.RL_PATH)

        self.frame = self.loadMapsTable(self.current_maps)
        textInput = Entry(self.root, width=30, borderwidth=5)
        searchButton = Button(self.root, text="Search", padx=20, command=searchAction)

        yourMapsButton = Button(self.root, text="Your Maps", padx=20,
            command=lambda: changeFrame(True))
        popularMapsButton = Button(self.root, text="Popular Maps", padx=20,
            command=lambda: changeFrame(False))
        
        changeRLDirButton = Button(self.root, text="Change rocket league folder",
            command=changeRL_PATH)
    
        downloadInput = Entry(self.root, width=70, borderwidth=5)
        downloadButton = Button(self.root, text="Download", padx=20,
            command=lambda: downloadMap(downloadInput.get()))

        self.frame.pack(padx=10, pady=80)

        downloadInput.place(relx=0.43, rely=0.09, anchor="n")
        downloadButton.place(relx=0.9, rely=0.09, anchor="ne")

        textInput.place(relx=0.01, rely=0.01, anchor="nw")
        searchButton.place(relx=0.29, rely=0.01, anchor="nw")

        yourMapsButton.place(relx=0.57, rely=0.01, anchor="ne")
        popularMapsButton.place(relx=0.75, rely=0.01, anchor="ne")
        changeRLDirButton.place(relx=0.99, rely=0.01, anchor="ne")

    def loadMapsTable(self, map_list):
        frame = LabelFrame(self.root, text="Maps", padx=5, pady=5)

        buttons = []
        for i in range(len(map_list)):
            for j in range(len(map_list[i])):
                l = Label(frame, text=map_list[i][j], padx=50)
                l.grid(row=i, column=j)
        
            buttons.append(Button(frame, text="Load", padx=50,
                command=lambda file=map_list[i][0]: loadMap(self.RL_PATH, file)))
            buttons[i].grid(row=i, column=2)

        return frame

    def downloadMapsTable(self, map_list):
        frame = LabelFrame(self.root, text="Popular Worshop Maps", padx=5, pady=5)

        buttons = []
        for i in range(len(map_list)):
            for j in range(len(map_list[i])):
                frame.columnconfigure(j, minsize=100)
                item = map_list[i][j]
                if item.isnumeric():
                    l = Button(frame, text="Steam link", padx=10)
                    l.bind("<Button-1>", lambda e, item=item: webbrowser.open_new(
                        f"https://steamcommunity.com/sharedfiles/filedetails/?id={item}"))
                else:
                    l = Label(frame, text=item)
                l.grid(row=i, column=j)
            buttons.append(Button(frame, text="Download", padx=10,
                command=lambda map_id=map_list[i][2]: downloadMap(map_id)))
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

def find_RL_PATH():
    alphabet = list(string.ascii_uppercase)
    for drive in reversed(alphabet):
        for r, d, f in os.walk(f"{drive}:\\"):
            if "rocketleague" in r:
                return r


if __name__ == "__main__":
    MyApp()
    #print(find_RL_PATH())