import logging, os
from io import BufferedWriter
from time import sleep

import smbclient
from smbclient import listdir, mkdir, register_session, rmdir, scandir
from smbclient.path import isdir, isfile
from smbprotocol.file_info import FileAttributes
from tqdm import tqdm

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)

SMB_SERVER_IP = "192.168.1.2"
SMB_USERNAME = os.environ.get("SMB_ARIA2_USERNAME")
SMB_PASSWORD = os.environ.get("SMB_ARIA2_PASSWORD")
SMB_PATH = "downloads"
SAVE_DIRECTORY = "G:\\private\\"
SAVE_FILE_SIZE = 100 * 1024 * 1024
SAVE_FILE_EXTNAME = [".mp4", ".mkv"]

logging.info(f"SMB_SERVER_IP: {SMB_SERVER_IP}")
logging.info(f"SMB_USERNAME: {SMB_USERNAME}")
logging.info(f"SMB_PASSWORD: {SMB_PASSWORD}")
logging.info(f"SAVE_DIRECTORY: {SAVE_DIRECTORY}")
logging.info(f"SAVE_FILE_SIZE: {SAVE_FILE_SIZE}")
logging.info(f"SAVE_FILE_EXTNAME: {SAVE_FILE_EXTNAME}")

register_session(SMB_SERVER_IP, username=SMB_USERNAME, password=SMB_PASSWORD)
base_path = r"\\" + SMB_SERVER_IP + r"\\" + SMB_PATH

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

def delete_remote_dir(path: str):
    entries = listdir(path)
    for name in entries:
        full_path = f"{path}\\{name}"
        if isdir(full_path):
            delete_remote_dir(full_path)  # 递归删除子目录
        else:
            smbclient.remove(full_path)  # 删除文件
    smbclient.rmdir(path)  # 删除空目录本身
    logging.warning(f"✅ 删除目录：{path}")

files = listdir(base_path)
for dir in files:
    if isdir(f"{base_path}\\{dir}") and not any(entry == f"{dir}.aria2" for entry in files):
        logging.warning(f"Download directory {dir} finished.")
        flag = False
        for f in listdir(f"{base_path}\\{dir}\\"):
            file_path = f"{base_path}\\{dir}\\{f}"
            if not isfile(file_path):
                continue
            stat = smbclient.stat(file_path)
            file_size = stat.st_size
            if (f.endswith(extName) for extName in SAVE_FILE_EXTNAME) and file_size >= SAVE_FILE_SIZE:
                flag = True
                if os.path.exists(SAVE_DIRECTORY + f) and os.path.getsize(SAVE_DIRECTORY + f) == file_size:
                    logging.warning(f"Skip download file /{dir}/{f} ...")
                    continue
                logging.warning(f"Download file /{dir}/{f} ...")
                local_file_path = SAVE_DIRECTORY + f

                with smbclient.open_file(file_path, mode="rb") as remote_file, \
                        open(SAVE_DIRECTORY + f, "wb") as local_file, \
                        tqdm(total=file_size, unit="B", unit_scale=True, desc=f) as pbar:
                    with BufferedWriter(local_file, buffer_size=16 * 1024 * 1024) as bf:

                        while True:
                            chunk = remote_file.read(16 * 1024 * 1024)
                            if not chunk:
                                break
                            bf.write(chunk)
                            pbar.update(len(chunk))
                logging.warning("Downloaded.")
        logging.warning(f"clean directory ...{dir}")
        if flag:
            sleep(1)
            delete_remote_dir(f"{base_path}\\{dir}")