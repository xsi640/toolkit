import os
import random
import subprocess
import platform

FILE_EXT_NAMES = ["mp4", "mkv"]
FILE_FOLDER = [
    # "F:\\private",
    # "/Volumes/private/private/其他",
    "G:\\private\\av\\"
]
CHANGE = True

files = []

for folder in FILE_FOLDER:
    for root, dirs, fs in os.walk(folder):
        for f in fs:
            if f.split(".")[-1] in FILE_EXT_NAMES and not f.startswith(".") and not f.startswith("."):
                full_path = os.path.join(root, f)
                files.append(full_path)

print(f"files count: {len(files)}")
while True:
    file = random.choice(files)
    print(file)
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', file))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(file)
    d = input("Press Enter to continue, 'd' to delete file...")
    if d == "d":
        files.remove(file)
        newFile = random.choice(files)
        print(newFile)
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', file))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(file)
        os.remove(file)
    if CHANGE:
        files.remove(file)
