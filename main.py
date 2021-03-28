import os
import re
import csv
import sys
import json
import time
import ctypes
import shutil
import string
import pathlib
import zipfile
import requests
import webbrowser
from tkinter import *
from tkinter import ttk, filedialog, messagebox


class RocketLeagueWorkshop:
    def __init__(self):
        self.TITLE = " Rocket League Workshop"
        self.FONT_SIZE = 11
        self.BUTTON_SIZE = 13

        self.root = Tk(className=self.TITLE)
        self.root.geometry("750x500")
        self.root.resizable(False, False)
        self.root.iconbitmap("./examples/rocketleague.ico")
        
        with open("config.json") as f:
            self.config = json.load(f) 
        try:
            self.maps = list_files(self.config['mapfiles'])
        except Exception:
            self.maps = []
        self.pop_maps = list_csv("maps.csv")
        self.current_maps = self.maps

        self.init_ui()
        self.your_maps_table(self.current_maps)

        self.root.after(100, self.config_setup)
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

        menu = Frame(self.root, padx=5, pady=5)
        download_frame = Frame(self.root)

        text_input = ttk.Entry(menu, width=40, font=("Arial", self.FONT_SIZE))
        text_input.bind("<Return>", search_action)
        search_button = ttk.Button(menu, text="Search", command=search_action)
        search_button.config(width=self.BUTTON_SIZE)

        your_maps_button = ttk.Button(menu, text="Your Maps",
            command=lambda: self.change_frame(True, list_files(self.config['mapfiles'])))
        your_maps_button.config(width=self.BUTTON_SIZE)
        popular_maps_button = ttk.Button(menu, text="Popular Maps",
            command=lambda: self.change_frame(False, self.pop_maps))
        popular_maps_button.config(width=self.BUTTON_SIZE)
    
        download_input = ttk.Entry(download_frame, width=79, font=("Arial", self.FONT_SIZE))
        download_input.bind("<Return>", lambda event: self.download_map(
            download_input.get(), self.config['mapfiles']))
        download_button = ttk.Button(download_frame, text="Download",
            command=lambda: self.download_map(download_input.get(), 
            "Couldn't download the map, check the URL of the map"))
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

    def download_map(self, map_id, error_message):
        self.make_popup("Downloading a map, please wait")
        try:
            DownloadMap(map_id, self.config['mapfiles'])
            self.popup.destroy()
            messagebox.showinfo(self.TITLE, "Map successfully downloaded")
        except Exception:
            messagebox.showerror(self.TITLE, error_message)

    def change_frame(self, load, maps_list):
        self.frame.destroy()
        self.current_maps = maps_list
        self.load_content()
        if load:
            self.your_maps_table(maps_list)
        else:
            self.popular_maps_table(maps_list)

    def load_options(self):
        def change_config(key, text):
            path = filedialog.askdirectory(initialdir=os.path.dirname(self.config[key]), title=text)
            if path != "":
                if key == "mapfiles":
                    move_mapfiles(key, path)
                self.config[key] = path
                self.write_config()
                if key == "mapfiles":
                    messagebox.showinfo(self.TITLE, "Map Files folder successfully changed")
                elif key == "rocketleague":
                    messagebox.showinfo(self.TITLE, "Rocket League folder successfully changed")
                self.change_frame(True, list_files(self.config['mapfiles']))

        def move_mapfiles(key, path):
            try:
                for subdir, dirs, files in os.walk(self.config[key]):
                    for file in files:
                        shutil.copy(f"{self.config[key]}/{file}", path)
                        os.remove(f"{self.config[key]}/{file}")
                os.rmdir(self.config[key])
            except Exception:
                pass

        self.options = Frame(self.root)

        change_rl_dir_button = ttk.Button(self.options, text="Change Rocket League folder",
        command=lambda: change_config("rocketleague", 
            "Select Rocket League Folder, usually (rocketleage/TAGame/CookedPCConsole)"))
        change_rl_dir_button.config(width=26)

        change_maps_dir_button = ttk.Button(self.options, text="Change Map Files folder",
            command=lambda: change_config("mapfiles", "Select your new Map Files folder"))
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
                shutil.copyfile(f"{self.config['mapfiles']}\{file}", f"{self.config['rocketleague']}/Labs_Underpass_P.upk")
            except Exception:
                messagebox.showerror(self.TITLE, 
                    "Couldn't load the map, try to change your Rocket League path in the bottom right corner")

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
                command=lambda map_id=map_list[i][2]: self.download_map(map_id, 
                    "Couldn't download the map, check your internet connection")))
            buttons[i].grid(row=i, column=3)

    def write_config(self):
        with open("config.json", "w") as outfile:
            json.dump(self.config, outfile)

    def make_popup(self, text):
        self.popup = Toplevel(self.root)
        self.popup.title(self.TITLE)
        self.popup.iconbitmap("./examples/rocketleague.ico")
        self.popup.configure(background="white")

        self.popup.geometry(f"250x75")
        self.root.eval(f'tk::PlaceWindow {str(self.popup)} center')
        self.popup.resizable(False, False)

        message = Label(self.popup, text=text)
        message.place(rely=0.5, relx=0.5, anchor="center")
        message.configure(background="white")
        self.popup.update()

    def config_setup(self):
        def find_rl_path():
            alphabet = list(string.ascii_uppercase)
            for drive in reversed(alphabet):
                for r, d, f in os.walk(f"{drive}:\\"):
                    if "rocketleague\\TAGame\\CookedPCConsole" in r:
                        r = r.replace("\\", "/")
                        messagebox.showinfo(self.TITLE, 
                            "Rocket League folder was successfully located")
                        return r
            else:
                messagebox.showerror(self.TITLE, 
                    "Couldn't find Rocket League folder, try to locate it manually in the bottom right corner")
                self.config['rocketleague'] = None

        def find_mapfiles_path():
            if getattr(sys, 'frozen', False):
                path = os.path.dirname(sys.executable)
            elif __file__:
                path = os.path.dirname(__file__)
            path = path.replace("\\", "/")
            return f"{path}/Map Files"

        if self.config['rocketleague'] == "":
            self.make_popup("Finding Rocket League folder, please wait")
            self.config['rocketleague'] = find_rl_path()
            self.write_config()
            self.popup.destroy()
            try:
                self.change_frame(True, list_files(self.config['mapfiles']))
            except Exception:
                pass

        if self.config['mapfiles'] == "":
            self.config['mapfiles'] = find_mapfiles_path()
            self.write_config()
            self.change_frame(True, list_files(self.config['mapfiles']))
    

def search(map_list, term):
    result = []
    for file_name in map_list:
        if term.lower() in file_name[0].lower():
            result.append(file_name)
    return result


def list_files(directory):
    maps = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".udk") or file.endswith(".upk"):
                size = os.path.getsize(f"{directory}/{file}")
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


class DownloadMap:
    def __init__(self, link, mapfiles_folder, unzip=True):
        self.mapfiles_folder = mapfiles_folder
        if link.isnumeric():
            self.map_id = link
        else:
            try:
                self.map_id = re.search('id=(.*)&', link).group(1)
            except:
                self.map_id = re.search('id=(.*)', link).group(1)

        self.map_id = int(self.map_id)
        self.download_map(unzip)

    def download_map(self, unzip):
        s = requests.session()
        data = {
            "publishedFileId": self.map_id,
            "collectionId": None,
            "extract": True,
            "hidden": False,
            "direct": False,
            "autodownload": False
        }
        r = s.post("https://backend-01-prd.steamworkshopdownloader.io/api/download/request", data=json.dumps(data))
        uuid = r.json()['uuid']
        data = f'{{"uuids":["{uuid}"]}}'

        while True:
            r = s.post("https://backend-01-prd.steamworkshopdownloader.io/api/download/status", data=data)
            if r.json()[uuid]['status'] == 'prepared':
                break
            time.sleep(1)
        params = (("uuid", uuid),)

        r = s.get("https://backend-01-prd.steamworkshopdownloader.io/api/download/transmit", params=params, stream=True) 
        with open(f"./{self.map_id}.zip", "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        if unzip == True: self.unzip_file()

    def unzip_file(self):
        with zipfile.ZipFile(f"./{self.map_id}.zip", "r") as f:
            for file in f.namelist():
                if file.endswith(".udk"):
                    f.extract(file, f"{self.mapfiles_folder}/")
        os.remove(f"./{self.map_id}.zip")


if __name__ == "__main__":
    RocketLeagueWorkshop()