import os
import re
import sys
import time
import json
import shutil
import pathlib
import zipfile
import requests


def load_map(RL_PATH, map_title):
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    elif __file__:
        path = os.path.dirname(__file__)
    shutil.copyfile(f"{path}\Map Files\{map_title}", f"{RL_PATH}/Labs_Underpass_P.upk")


class downloadMap:
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