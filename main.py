from pywinauto import Application
from bs4 import BeautifulSoup
import requests
import configparser
import time
import datetime
import ctypes
import urllib.request
import zipfile
import os
import shutil
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="pywinauto.application")
version = "Version 1.8"
Updated = False

def Print(text): return print("[" + str(datetime.datetime.now().time().strftime("%H:%M:%S")) + "] " + text)

def download_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    print(f"Downloading: {percent}%", end='\r')
    if percent == 100:
        print()
try:
    shutil.rmtree(os.path.join(os.path.expanduser('~/TMVAuto'), 'DELETEME'))
except Exception as yo:
    time.sleep(0)

def Update():
    try:
        destination_folder = os.path.expanduser('~/TMVAuto')
        current_folder_path = os.path.join(destination_folder, 'main')

        try:
            os.makedirs(os.path.join(destination_folder, 'DELETEME'), exist_ok=True)
        except Exception as a:
            time.sleep(0)

        new_folder_path = os.path.join(destination_folder, 'DELETEME')

        os.rename(current_folder_path, new_folder_path)
        zip_url = 'https://github.com/rjwilder1/TMV-Keys/releases/download/idk/TMV.zip'
        
        config_file_path = os.path.join(new_folder_path, 'config.ini')
        config_exists = os.path.exists(config_file_path)
        os.makedirs(destination_folder, exist_ok=True)

        if config_exists:
            print("Current config exists")
            backup_folder = os.path.join(destination_folder, 'Backup')
            os.makedirs(backup_folder, exist_ok=True)
            backup_file_path = os.path.join(backup_folder, 'Config.ini')
            shutil.copy2(config_file_path, backup_file_path)
        else:
            print("No current config exists, please contact RJ")

        zip_filename, _ = urllib.request.urlretrieve(zip_url, reporthook=download_progress)

        with zipfile.ZipFile(zip_filename, 'a') as zip_ref:
            total_files = len(zip_ref.infolist())
            extracted_files = 0

            for i, file_info in enumerate(zip_ref.infolist(), start=1):
                zip_ref.extract(file_info, destination_folder)
                extracted_files += 1
                progress_percent = int(extracted_files * 100 / total_files)
                print(f"Extracting: {progress_percent}%", end='\r')
                if i == total_files:
                    print()

        if config_exists:
            restored_file_path = os.path.join(destination_folder + '\\main', 'config.ini')
            shutil.copy2(backup_file_path, restored_file_path)

        os.remove(zip_filename)
        try:
            shutil.rmtree(os.path.join(destination_folder, 'Backup'))
        except Exception as a:
            time.sleep(0)

        try:
            shutil.rmtree(os.path.join(destination_folder, 'DELETEME'))
        except Exception as yo:
            time.sleep(0)

        input("Update completed, please relaunch. Press enter to exit")
        exit()
    except Exception as yo1:
        Print("Update error: " + str(yo1))

def CheckVersion(): 
    global version
    content = requests.get("https://raw.githubusercontent.com/rjwilder1/TMV-Keys/main/README.md").text
    versionstring = content.splitlines()[0]
    if versionstring == version:
        return True
    else:
        return False

if not CheckVersion():
    input("There is an update available, press enter to update")
    Update()

def ValidateKeys(key):
    global Validated
    content = requests.get("https://raw.githubusercontent.com/rjwilder1/TMV-Keys/main/README.md").text
    keys = content.splitlines()
    for line in keys:
        if line == key:
            Validated = True
            break
    if Validated:
        Print("Key is valid")
        Print('Waiting for page')
    else:
        input("Key in invalid, press enter to exit")
        quit()

try:
    config= configparser.ConfigParser()
    config.read(r'config.ini')
    path = config['CONFIG']['path']
    URL = config['CONFIG']['smsurl'].split(", ")
    KEY = config['CONFIG']['key']
    AmountDone = 0
    Validated = False
except Exception as a:
    print("Error in CONFIG: " + str(a))

ValidateKeys(KEY)

def title(title):
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleTitleW(title)

title("TMV Auto Enter " + version)

def GetCode(PhoneNum):
    global URL
    FoundNumber = False
    for SMSURL in URL:
        response = requests.get(SMSURL)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find('table')
        if table:
            msgs = table.find_all('tr')
            if len(msgs) >= 1:
                td_elements = msgs[0].find_all('td')
                if len(td_elements) >= 3:
                    PhoneNumber = td_elements[0].get_text(strip=True)
                    Code1 = td_elements[2].get_text(strip=True) 
                    Code = Code1[:6]
                    if PhoneNumber in PhoneNum:
                        FoundNumber = True
                        return PhoneNumber, Code
        if FoundNumber:
            FoundNumber = False
            break

AppPath = Application(backend="win32").start(path)

def GetVers():
    Found = False
    for i in AppPath.windows():
        if Found:
            break
        istr = str(i)
        if 'WindowsForms10' in istr:
            txt = istr.index(',')
            Found = True
            return istr[txt + 1:].strip()

time.sleep(2)
#print(re.sub(r"(?<=\.Window)......", "XXXXXX", GetVers()).replace('WindowXXXXXX', 'STATIC'))

def GetWindow(title): 
    return AppPath.window(title_re=title)

def ChangeText(text, window): return window.child_window(class_name=re.sub(r"(?<=\.Window)......", "XXXXXX", GetVers()).replace('WindowXXXXXX', 'EDIT'), found_index=0).set_text(text)
def ClickButton(window, index): return window.child_window(class_name=re.sub(r"(?<=\.Window)......", "XXXXXX", GetVers()).replace('WindowXXXXXX', 'BUTTON'), found_index=index).click()
def GetLabelText(window, index): return window.child_window(class_name=re.sub(r"(?<=\.Window)......", "XXXXXX", GetVers()).replace('WindowXXXXXX', 'STATIC'), found_index=index).window_text()

while True:
    try:
        PhoneNumberLabel = GetLabelText(GetWindow(".*Enter Queue Code for"), 1)
        PhoneNumber = GetCode(PhoneNumberLabel)[0]
        if PhoneNumber in PhoneNumberLabel:
            AmountDone += 1
            Code = GetCode(PhoneNumberLabel)[1]
            ChangeText(Code, GetWindow(".*Enter Queue Code for"))
            ClickButton(GetWindow(".*Enter Queue Code for"), 2)
            Print("[" + str(AmountDone) + "] Finished " + PhoneNumber + " - Code: " + Code)
        else:
            Print("Not correct number, waiting for new message: Label Number: " + PhoneNumberLabel + " | SMSPhoneNumber: " + PhoneNumber)
    except Exception as x:
        time.sleep(0.5)
    time.sleep(1)