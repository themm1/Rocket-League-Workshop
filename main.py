import os
import re
import time
import json
import shutil
import pathlib
import zipfile
import requests


class loadMap:
    def __init__(self, RL_PATH, map_title):
        self.RL_PATH = RL_PATH
        self.map_title = map_title

    def make_backup(self):
        underpass = r'{}\Labs_Underpass_P.upk'.format(self.RL_PATH)
        size = os.path.getsize(underpass)
        if size > 2200000 and size < 2210000:
            os.rename(underpass, 
                r'{}\Labs_Underpass_P_BACKUP.upk'.format(self.RL_PATH))

    def load_map(self):
        PATH = pathlib.Path(__file__).parent.absolute()
        shutil.copyfile(r'{}\Map Files\{}'.format(PATH, self.map_title),
                    r'{}\Labs_Underpass_P.upk'.format(self.RL_PATH))

class downloadMap:
    def __init__(self, link, unzip=True):
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
                    f.extract(file, "./Map Files/")
        os.remove(f"{self.map_id}.zip")


#loadmap = loadMap(r'E:\Rocket\rocketleague\TAGame\CookedPCConsole', "gpeppersRings.udk")
#loadmap.load_map()
#download = downloadMap("https://steamcommunity.com/sharedfiles/filedetails/?id=2347189620&searchtext=")
