import os
import shutil
import time
import urllib
import zipfile
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
        print("Update error: " + str(yo1))

Update()