import os
import random
import subprocess
import platform

from typing_extensions import runtime

FILE_EXT_NAMES = ["mp4", "mkv"]
FILE_FOLDER = [
    # "F:\\private",
    # "F:\\private\\其他",
    "/Volumes/Storage1/private/"
]
CHANGE = True

files = []

for folder in FILE_FOLDER:
    for f in [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]:
        if f.split(".")[-1] in FILE_EXT_NAMES and not f.startswith(".") and not f.startswith("."):
            files.append(folder + "/" + f)

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
