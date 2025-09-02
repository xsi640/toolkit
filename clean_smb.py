import os
import logging
from time import sleep

from smb.SMBConnection import SMBConnection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

conn = SMBConnection(SMB_USERNAME, SMB_PASSWORD, 'client', SMB_SERVER_IP, use_ntlm_v2=True)
conn.connect(SMB_SERVER_IP, 445)

files = conn.listPath(SMB_PATH, '/')
for dir in files:
    if (dir.filename not in ['.', '..'] and dir.isDirectory and
            not any(entry.filename == f"{dir.filename}.aria2" for entry in files)):
        logging.info(f"Download directory {dir.filename} finished.")
        flag = False
        for f in conn.listPath(SMB_PATH, f"/{dir.filename}"):
            if (f.filename.endswith(extName) for extName in SAVE_FILE_EXTNAME) and f.file_size >= SAVE_FILE_SIZE:
                flag = True
                if os.path.exists(SAVE_DIRECTORY + f.filename) and os.path.getsize(
                        SAVE_DIRECTORY + f.filename) == f.file_size:
                    logging.info(f"Skip download file /{dir.filename}/{f.filename} ...")
                    continue
                logging.info(f"Download file /{dir.filename}/{f.filename} ...")
                local_file_path = SAVE_DIRECTORY + f.filename
                with open(local_file_path, 'wb') as local_file:
                    conn.retrieveFile(SMB_PATH, f"/{dir.filename}/{f.filename}", local_file, show_progress=True)
                logging.info("Downloaded.")
        logging.info(f"clean directory ...{dir.filename}")
        if flag:
            sleep(1)
            conn.deleteFiles(SMB_PATH, f"/{dir.filename}/*", delete_matching_folders=True)
            conn.deleteDirectory(SMB_PATH, f"/{dir.filename}")
conn.close()
