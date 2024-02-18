import os
import shutil

DOWNLOAD_PATH = 'E:\\Downloads'
TARGET_PATH = 'E:\\temp\\aria2'
COPY_FILE_EXT = [".mp4", ".mkv"]
COPY_FILE_SIZE = 100 * 1024 * 1024

for dir in os.listdir(DOWNLOAD_PATH):
    if (os.path.isdir(os.path.join(DOWNLOAD_PATH, dir)) and
            not os.path.exists(os.path.join(DOWNLOAD_PATH, dir) + ".aria2")):
        for file in os.listdir(os.path.join(DOWNLOAD_PATH, dir)):
            if (os.path.splitext(file)[1] in COPY_FILE_EXT and
                    os.path.getsize(os.path.join(DOWNLOAD_PATH, dir, file)) > COPY_FILE_SIZE):
                source_file = os.path.join(DOWNLOAD_PATH, dir, file)
                dest_file = os.path.join(TARGET_PATH, file)
                shutil.move(source_file, dest_file)
                print(f"copy file: {source_file} -> {dest_file}")
        shutil.rmtree(os.path.join(DOWNLOAD_PATH, dir))
        print(f"remove dir: {dir}")
