import os
import csv
import string
import webbrowser
from tkinter import *
from tkinter import filedialog
from main import load_map, downloadMap


class RocketLeagueWorkshop:
    def __init__(self):
        with open("rlpath.txt", "r") as f:
            self.RL_PATH = f.readline()
        self.maps = list_files("./Map Files/")
        self.pop_maps = list_csv("maps.csv")
        self.current_maps = self.maps

        self.root = Tk(className="Rocket League Workshop")
        self.root.geometry("750x500")
        self.root.resizable(False, False)

        self.init_ui()
        self.load_content()
        self.your_maps_table(self.current_maps)

        self.root.mainloop()

    def init_ui(self):
        def search_action(event=None):
            self.frame.destroy()
            term = text_input.get()
            results = search(self.current_maps, term)
            self.load_content()

            if len(self.current_maps[0]) == 2:
                self.your_maps_table(results)
            else:
                self.popular_maps_table(results)

        def change_frame(load, maps_list):
            self.frame.destroy()
            self.current_maps = maps_list
            self.load_content()
            if load:
                self.your_maps_table(maps_list)
            else:
                self.popular_maps_table(maps_list)

        def change_rlpath():
            rl_path = filedialog.askdirectory(initialdir="/", title="Select Rocket League Folder")
            if rl_path != "":
                rl_path = f"{rl_path}/TAGame/CookedPCConsole/"
                self.RL_PATH = r'{}'.format(rl_path.replace("/", "\\"))
                with open("rlpath.txt", "w") as f:
                    f.writelines(self.RL_PATH)

        self.menu = LabelFrame(self.root, padx=5, pady=5)

        text_input = Entry(self.menu, width=27, font=("Arial", 13))
        text_input.bind("<Return>", search_action)
        search_button = Button(self.menu, text="Search", command=search_action)
        search_button.config(width=12)

        your_maps_button = Button(self.menu, text="Your Maps",
            command=lambda: change_frame(True, list_files("./Map Files/")))
        your_maps_button.config(width=12)
        popular_maps_button = Button(self.menu, text="Popular Maps",
            command=lambda: change_frame(False, self.pop_maps))
        popular_maps_button.config(width=12)
        
        change_rl_dir_button = Button(self.menu, text="Change rocket league folder",
            command=change_rlpath)
        change_rl_dir_button.config(width=22)
    
        download_input = Entry(self.root, width=53, font=("Arial", 13))
        download_input.bind("<Return>", lambda event: downloadMap(download_input.get()))
        download_button = Button(self.root, text="Download",
            command=lambda: downloadMap(download_input.get()))
        download_button.config(width=12)

        self.menu.pack()
        
        text_input.grid(column=0, row=0)
        search_button.grid(column=1, row=0, padx=(4, 15))

        your_maps_button.grid(column=2, row=0)
        popular_maps_button.grid(column=3, row=0)
        change_rl_dir_button.grid(column=4, row=0)

        download_input.place(relx=0.432, rely=0.1, anchor="n")
        download_button.place(relx=0.885, rely=0.097, anchor="ne")

    def load_content(self):
        def wheel_scroll(event):
            scroll_size = int(-1*(event.delta/120))
            canvas.yview_scroll(scroll_size, "units")

        self.frame = LabelFrame(self.root, text="Maps")
        self.frame.pack(padx=10, pady=45)

        canvas = Canvas(self.frame, height=600, width=700)
        canvas.pack(side="left", fill="both")

        yscrollbar = Scrollbar(self.frame, orient="vertical",
            command=canvas.yview)
        yscrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=yscrollbar.set)
        canvas.bind("<Configure>", lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", wheel_scroll)

        self.content = Frame(canvas)
        canvas.create_window((0, 0), window=self.content, anchor="nw")

    def your_maps_table(self, map_list):
        buttons = []
        for i in range(len(map_list)):
            for j in range(len(map_list[i])):
                self.content.columnconfigure(j, minsize=150)
                l = Label(self.content, text=map_list[i][j][:80])
                l.grid(row=i, column=j)
        
            buttons.append(Button(self.content, text="Load", width=10,
                command=lambda file=map_list[i][0]: load_map(self.RL_PATH, file)))
            buttons[i].grid(row=i, column=2)

    def popular_maps_table(self, map_list):
        buttons = []
        for i in range(len(map_list)):
            for j in range(len(map_list[i])):
                self.content.columnconfigure(j, minsize=150)
                item = map_list[i][j]
                if item.isnumeric() and j == 2:
                    l = Button(self.content, text="Steam link", width=10)
                    l.bind("<Button-1>", lambda event, item=item: webbrowser.open_new(
                        f"https://steamcommunity.com/sharedfiles/filedetails/?id={item}"))
                else:
                    l = Label(self.content, text=item[:50])
                l.grid(row=i, column=j)
                
            buttons.append(Button(self.content, text="Download", width=10,
                command=lambda map_id=map_list[i][2]: downloadMap(map_id)))
            buttons[i].grid(row=i, column=3)


def search(map_list, term):
    result = []
    for file_name in map_list:
        if term.lower() in file_name[0].lower():
            result.append(file_name)
    return result


def list_files(directory):
    maps = []
    for file in os.listdir(directory):
        if file.endswith(".udk"):
            size = os.path.getsize(f"{directory}{file}")
            maps.append([file, f"{round(size / 1000000, 2)} MB"])
    return maps


def list_csv(file):
    maps = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            maps.append(row)
    return maps


def find_rlpath():
    alphabet = list(string.ascii_uppercase)
    for drive in reversed(alphabet):
        for r, d, f in os.walk(f"{drive}:\\"):
            if "rocketleague" in r:
                return r


if __name__ == "__main__":
    RocketLeagueWorkshop()