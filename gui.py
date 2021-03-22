import os
import csv
import string
import webbrowser
from tkinter import *
from load_map import load_map, downloadMap
from tkinter import ttk, filedialog, messagebox


class RocketLeagueWorkshop:
    def __init__(self):
        with open("rlpath.txt", "r") as f:
            self.RL_PATH = f.readline()
        self.maps = list_files("./Map Files/")
        self.pop_maps = list_csv("maps.csv")
        self.current_maps = self.maps

        self.FONT_SIZE = 11
        self.BUTTON_SIZE = 13

        self.root = Tk(className="Rocket League Workshop")
        self.root.geometry("750x500")
        self.root.resizable(False, False)
        self.root.iconbitmap("rocketleague.ico")

        self.init_ui()
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

        def download_map_try(map_id):
            try:
                downloadMap(map_id)
            except Exception:
                messagebox.showerror("Error popup", 
                    "Couldn't download the map, check the URL of the map")

        menu = Frame(self.root, padx=5, pady=5)
        download_frame = Frame(self.root)

        text_input = ttk.Entry(menu, width=40, font=("Arial", self.FONT_SIZE))
        text_input.bind("<Return>", search_action)
        search_button = ttk.Button(menu, text="Search", command=search_action)
        search_button.config(width=self.BUTTON_SIZE)

        your_maps_button = ttk.Button(menu, text="Your Maps",
            command=lambda: change_frame(True, list_files("./Map Files/")))
        your_maps_button.config(width=self.BUTTON_SIZE)
        popular_maps_button = ttk.Button(menu, text="Popular Maps",
            command=lambda: change_frame(False, self.pop_maps))
        popular_maps_button.config(width=self.BUTTON_SIZE)
    
        download_input = ttk.Entry(download_frame, width=79, font=("Arial", self.FONT_SIZE))
        download_input.bind("<Return>", lambda event: downloadMap(download_input.get()))
        download_button = ttk.Button(download_frame, text="Download",
            command=lambda: download_map_try(download_input.get()))
        download_button.config(width=self.BUTTON_SIZE)

        menu.pack()
        text_input.grid(column=0, row=0)
        search_button.grid(column=1, row=0, padx=(0, 136))
        your_maps_button.grid(column=2, row=0)
        popular_maps_button.grid(column=3, row=0)

        download_frame.pack()
        download_input.grid(column=0, row=0)
        download_button.grid(column=1, row=0)

        self.load_options()
        self.load_content()

    def load_options(self):
        def change_rlpath():
            rl_path = filedialog.askdirectory(initialdir="/", 
                title="Select Rocket League maps folder (usually rocketleague/TAGame/CookedPCConsole)")
            if rl_path != "":
                self.RL_PATH = rl_path
                with open("rlpath.txt", "w") as f:
                    f.writelines(self.RL_PATH)

        self.options = Frame(self.root)

        change_rl_dir_button = ttk.Button(self.options, text="Change Rocket League folder",
        command=change_rlpath)
        change_rl_dir_button.config(width=26)
        change_maps_dir_button = ttk.Button(self.options, text="Change Map Files folder",
            command=change_rlpath)
        change_maps_dir_button.config(width=26)

        self.options.pack(pady=(5, 0))
        self.options.columnconfigure(0, minsize=395)
        change_maps_dir_button.grid(column=1, row=0)
        change_rl_dir_button.grid(column=2, row=0)

    def load_content(self):
        def wheel_scroll(event):
            scroll_size = int(-1*(event.delta/120))
            canvas.yview_scroll(scroll_size, "units")

        self.frame = LabelFrame(self.root, text="Maps")
        self.frame.pack(padx=10)

        canvas = Canvas(self.frame, height=380, width=700)
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
        self.options.destroy()
        self.load_options()

    def your_maps_table(self, map_list):
        def load_map_try(file):
            try:
                load_map(self.RL_PATH, file)
            except Exception:
                messagebox.showerror("Error popup", 
                    "Couldn't load the map, try to change your Rocket League path in the top right corner")

        buttons = []
        for i in range(len(map_list)):
            for j in range(len(map_list[i])):
                if j == 0:
                    self.content.columnconfigure(j, minsize=510)
                else:
                    self.content.columnconfigure(j, minsize=100)
                l = ttk.Label(self.content, text=map_list[i][j][:85])
                l.grid(row=i, column=j, sticky="W")
        
            buttons.append(ttk.Button(self.content, text="Load", width=self.BUTTON_SIZE,
                command=lambda file=map_list[i][0]: load_map_try(file)))
            buttons[i].grid(row=i, column=2)

    def popular_maps_table(self, map_list):
        def download_map_try(map_id):
            downloadMap(map_id)
            '''
            try:
                downloadMap(map_id)
            except Exception:
                messagebox.showerror("Error popup", 
                    "Couldn't download the map, check your internet connection")
            '''

        buttons = []
        for i in range(len(map_list)):
            for j in range(len(map_list[i])):
                item = map_list[i][j]
                if j == 0:
                    self.content.columnconfigure(j, minsize=410)
                else:
                    self.content.columnconfigure(j, minsize=100)
                if j == 2:
                    l = ttk.Button(self.content, text="Steam link", width=self.BUTTON_SIZE)
                    l.bind("<Button-1>", lambda event, item=item: webbrowser.open_new(
                        f"https://steamcommunity.com/sharedfiles/filedetails/?id={item}"))
                else:
                    l = Label(self.content, text=item[:68])
                l.grid(row=i, column=j, sticky="W")
                
            buttons.append(ttk.Button(self.content, text="Download", width=self.BUTTON_SIZE,
                command=lambda map_id=map_list[i][2]: download_map_try(map_id)))
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
        if file.endswith(".udk") or file.endswith(".upk"):
            size = os.path.getsize(f"{directory}{file}")
            maps.append([file, f"{round(size / 1000000, 2)} MB"])
    return maps


def list_csv(file):
    maps = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            maps.append(row)
    maps.pop(0)
    return maps


def find_rlpath():
    alphabet = list(string.ascii_uppercase)
    for drive in reversed(alphabet):
        for r, d, f in os.walk(f"{drive}:\\"):
            if "rocketleague" in r:
                return r


if __name__ == "__main__":
    RocketLeagueWorkshop()