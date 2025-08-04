VERSION = (0, 0, 5)


import cgi
import urllib
import urllib.request
verline = urllib.request.urlopen('https://alexferras.github.io/votv.txt').read()
NEW_VERSION = tuple([int(i) for i in verline.decode().split('.')])
if VERSION < NEW_VERSION:
    print('need update')
    import os
    os.system('start updater -f -r')
    import sys
    sys.exit()

import sys
sys.stderr = open("errors.txt", "w")


import pythonnet
pythonnet.load("coreclr")
import clr
import os

import sys
import struct
import zipfile
import shutil

from json import loads
if os.path.exists('updater.bak'):
    os.replace('updater.bak', 'updater.exe')

with open('secrets.json') as f:
    SECRETS = loads(f.read())

os.environ['GIT_PYTHON_REFRESH'] = 'q'
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = os.path.join(os.getcwd(), 'mingit', 'cmd', 'git.exe')
print(os.getenv('GIT_PYTHON_GIT_EXECUTABLE'))
import git
GIT_PATH = os.path.join(os.getcwd(), 'mingit', 'cmd', 'git.exe')
git.refresh(GIT_PATH)
GIT_STAGING = os.path.join(os.getcwd(), 'git_staging')
VOTV = os.path.join(os.getenv('LOCALAPPDATA'), 'VotV')
REPO_URL = SECRETS['github_login']




asm_path = r'CS'
sys.path.append(asm_path)
clr.AddReference('Memory')
from Memory import Mem

import socket
HOSTNAME = socket.gethostname()

import discord
DISCORD_TOKEN = SECRETS['discord_token']

s_path = os.path.join(os.getcwd(), 'data', 'a_MySlot.sav')

timeentry = b'totalTime\0\x0E\0\0\0FloatProperty\0\x04\0\0\0\0\0\0\0\0'
try: 
    with open(s_path, 'rb') as sf:
        contents = sf.read()
        index = contents.find(timeentry)
        time_b = contents[index + len(timeentry):index + len(timeentry) + 4]
        time = struct.unpack('f', time_b)[0]
        print(time)
except:
    pass

Mem = Mem()

secondsAddress = "VotV-Win64-Shipping.exe+0x04E4EB70,8,A0,228,DC"

def get_local_savefile_path(save_name:str) -> str:
    localappdata = os.getenv('LOCALAPPDATA')
    return os.path.join(localappdata, 'VotV', 'Saved', 'SaveGames', save_name)

def set_w_subtext(in_text:str):
    global widget
    try:
        widget
    except:
        return
    
    widget.subtext.setText(in_text)

def zip_save(bad_folders:str):
    bf = [b.replace('/', '\\') for b in bad_folders.splitlines()]
    localappdata = os.getenv('LOCALAPPDATA')
    votv = os.path.join(localappdata, 'VotV')
    zip_path = os.path.join(votv, 'saved.zip')
    with zipfile.ZipFile(zip_path, mode="w") as archive:
        for dirpath,_,filenames in os.walk(votv):
            f:str
            for f in filenames:
                p = os.path.abspath(os.path.join(dirpath, f))
                in_bad = False
                for b in bf:
                    if b in p:
                        in_bad = True
                        break
                if in_bad:
                    continue
                file_name = p.replace(votv, '')
                archive.write(p, file_name)

def copy_to_directory(src:str, dist:str, bad_folders:str):
    bf = [b.replace('/', '\\') for b in bad_folders.splitlines()]
    for dirpath,_,filenames in os.walk(src):
        f:str
        for f in filenames:
            p = os.path.abspath(os.path.join(dirpath, f))
            in_bad = False
            for b in bf:
                if b in p:
                    in_bad = True
                    break
            if in_bad:
                continue
            file_name = p.replace(src, dist)
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            if os.path.exists(file_name):
                os.remove(file_name)
            shutil.copy(p, file_name)

def copy_to_gitstaging():
    copy_to_directory(VOTV, GIT_STAGING, test_bad_folders)

BACKUPS = os.path.join(VOTV, 'Saved', 'backups')
def backups_count_file(filename:str) -> int:
    count = 0
    for f in os.listdir(BACKUPS):
        if f[:-2] == filename:
            count += 1

    return count


def delete_oldest_backup():
    def key(v:str):
        return os.path.getmtime(v)

    files = [os.path.join(BACKUPS, f) for f in os.listdir(BACKUPS)]
    files.sort(reverse=True, key=key)
    os.remove(files[0])
    
        


def copy_to_savefolder():
    os.makedirs(BACKUPS,exist_ok=True)
    saves = os.path.join(VOTV, 'Saved', 'SaveGames')
    for s in os.listdir(saves):
        if os.path.isdir(os.path.join(saves, s)):
            continue

        c = backups_count_file(s)
        #if c > 5:
            #delete_oldest_backup()

        f_name = f'{s}-{c}'
        f_path = os.path.join(BACKUPS, f_name)
        shutil.copy2(os.path.join(saves, s), f_path)

    copy_to_directory(GIT_STAGING, VOTV, test_bad_folders)

        

test_bad_folders = """Saved/BugIt
Saved/Config
Saved/Logs
Saved/backups
Saved/webcache
saved.zip
.git
"""
#zip_save(test_bad_folders)

class DiscordAPI(discord.Client):
    @staticmethod
    def create():
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guild_messages = True
        return DiscordAPI(intents=intents)

    def init_constants(self):
        self.PERM_DATA_ID = 1337210423996579893
        self.VOTV_ID = 1401218978084425738

    async def init_data(self):
        self.perm_data:discord.ForumChannel = self.guild.get_channel(self.PERM_DATA_ID)
        self.votv:discord.TextChannel = self.guild.get_channel(self.VOTV_ID)

    async def on_ready(self):
        try:
            self.guild = self.guilds[0]
            await self.init_data()
            if hasattr(self, 'download'):
                await self.download_save()
                await self.close()
            if hasattr(self, 'upload'):
                await self.upload_save()
                await self.close()
        except Exception as e:
            await self.close()
            raise e
            

    async def get_perm_data_latest_str(self, key:str) -> str:
        all_threads = self.perm_data.threads + [t async for t in self.perm_data.archived_threads()]
        for t in all_threads:
            if t.name == key:
                return (await t.fetch_message(t.last_message_id)).content



    async def download_save(self):
        pass
    async def upload_save(self):
        #save_path = get_local_savefile_path(await self.get_savename())
        await self.votv.send(self.text, file=file)
        

    async def get_savename(self):
        return await self.get_perm_data_latest_str('votv_savefile') + '.sav'


    async def on_message(self, message:discord.Message):
        print(message.content)

    def run_client(self):
        self.init_constants()
        self.run(DISCORD_TOKEN)
        

repo:git.Repo

def file_in_repo(filePath):
    for f in repo.index.entries:
        if f[0].replace('/', '\\') in filePath:
            return True
    return False

def resolve_repo():
    global repo
    os.makedirs(GIT_STAGING, exist_ok=True)
    import git.cmd
    os.system(f'{GIT_PATH} config --global http.schannelCheckRevoke false')
    os.system(f'{GIT_PATH} config --global http.sslBackend "openssl')
    os.system(f'{GIT_PATH} config --global http.sslCAInfo {os.path.join(os.getcwd(), 'git_fuckery', 'cacert-2025-07-15.pem')}')
    try:
        if len(os.listdir(GIT_STAGING)) == 0:
            #repo = git.Repo.init('git_staging')
            #repo.create_remote('origin', REPO_URL)
            #repo.config_writer().set_value('http', 'schannelCheckRevoke', 'false')
            repo = git.Repo.clone_from(REPO_URL, os.path.join(os.getcwd(), 'git_staging'))
            repo.remote().pull()
        else:
            repo = git.Repo(GIT_STAGING)
            repo.remote().pull()
    except Exception as e:
        with open('giterrors.txt', 'w') as f:
            f.write(str(e))
            raise e

def download_save_source_direct():
    source = 'https://github.com/AlexFerras/votv_saves/archive/refs/heads/main.zip'
    filename = 'src.zip'
    urllib.request.urlretrieve(source, filename)
    with zipfile.ZipFile(filename) as f:
        for fi in f.infolist():
            fi.filename = fi.filename.removeprefix('votv_saves-main/')
            if fi.filename.endswith('/') : continue
            
            if fi.filename:
                f.extract(fi, GIT_STAGING)
                


    os.remove(filename)


def download_save():
    global repo
    #api = DiscordAPI.create()
    #api.download = True
    #api.run_client()
    set_w_subtext('error downloading save')
    try:
        resolve_repo()
        raise "why"
    except:
        download_save_source_direct()
    copy_to_savefolder()
    set_w_subtext('downloaded save')

def upload_save(text:str):
    global repo
    set_w_subtext("error uploading save")
    resolve_repo()
    copy_to_gitstaging()
    files_added = False
    for t in repo.untracked_files:
        repo.index.add(t)
        files_added = True



    changedFiles = repo.head.commit.diff(None)
    for f in changedFiles:
        repo.index.add(f.a_path)
        files_added = True

    if not files_added:
        set_w_subtext('no changes in savefiles')
        return

    repo.index.commit(text)
    repo.remote().push()
    set_w_subtext('save uploaded')
#upload_save('test commit')
#download_save()


# ui
from PySide6 import QtCore, QtWidgets, QtGui
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.download_button = QtWidgets.QPushButton("Download save")
        self.upload_button = QtWidgets.QPushButton("Upload save")
        self.text = QtWidgets.QLabel("",
                                     alignment=QtCore.Qt.AlignCenter)

        self.subtext = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.upload_button)
        self.layout.addWidget(self.subtext)

        self.download_button.clicked.connect(self.download)
        self.upload_button.clicked.connect(self.upload_popup)

    @QtCore.Slot()
    def download(self):
        download_save()

    @QtCore.Slot()
    def upload_popup(self):
        popup = QtWidgets.QInputDialog(self, QtCore.Qt.WindowType.FramelessWindowHint)
        popup.setModal(True)
        popup.setLabelText("message")
        popup.show()
        popup.accepted.connect(self.upload)
        self.popup = popup
    
    @QtCore.Slot()
    def upload(self):
        final_message = HOSTNAME + ": " + self.popup.textValue()
        upload_save(final_message)


app = QtWidgets.QApplication([])
widget = MyWidget()
widget.resize(300, 200)
widget.show()

main_text_format = \
"""
Game started: {GameStarted}
Save Time: {SaveTime}
Current Game Time: {GameTime}
Shift Time remaining: {TimeRemaining}
"""
import math
import time
class GameData:
    def __init__(self):
        self.gametime:float = 0.0
        self.savetime:float = 0.0
        self.shift_end:float = self.savetime + 60 * 75 *2
        self.game_started:bool = False
        self.text_format = main_text_format

    def update_gametime(self, in_time:float):
        self.gametime = in_time


    def dhms_tuple(self, seconds:float) -> tuple:
        secs = int(seconds)
        if secs == 0:
            return (0, 0, 0, 0)

        s = math.floor(secs)
        m = math.floor(secs / 60)
        h = math.floor(m / 60)
        d = math.floor(h / 24)
        return (
            d,
            h % 24,
            m % 60,
            s % (m * 60)
        )

    def dhms_str(self, seconds:float) -> str:
        return time.strftime('%H:%M', time.gmtime(seconds))

        try:
            t = self.dhms_tuple(seconds)
            d = 'D: ' + str(t[0]) if t[0] else ''
            h = 'H: ' + str(t[1]) if t[1] else ''
            m = 'M: ' + str(t[2]) if t[2] else ''
            s = 'S: ' + str(t[3]) if t[3] else ''
        except Exception as e:
            print(e)

        return ', '.join([i for i in [d, h, m, s] if len(i)])

    def get_formatted_text(self) -> str:

        form_dict = {}
        form_dict["GameStarted"] = self.game_started
        form_dict["SaveTime"] = 0#self.dhms_str(self.savetime)
        form_dict["GameTime"] = self.dhms_str(self.gametime)
        form_dict["TimeRemaining"] = self.dhms_str(self.shift_end - self.gametime)
        return self.text_format.format(**form_dict)

gamedata = GameData()
        

def main_loop():
    pid = Mem.GetProcIdFromName('VotV-Win64-Shipping')
    if pid:
        try:
            Mem.OpenProcess(pid)
            time = Mem.ReadFloat(secondsAddress)
            gamedata.update_gametime(time)
            widget.text.setText(gamedata.get_formatted_text())
        except:
            pass
           # app.exit()

timer = QtCore.QTimer(widget, interval=1000)
timer.timeout.connect(main_loop)
timer.start()
sys.exit(app.exec())



import asyncio



import time
while True:
    pid = Mem.GetProcIdFromName('VotV-Win64-Shipping')
    if pid:
        Mem.OpenProcess(pid)
        print('time seconds: ', Mem.ReadFloat(secondsAddress))
    else:
        break
    time.sleep(1)

#print(tr.GetTime())