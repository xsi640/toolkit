import os
import random

FILE_EXT_NAMES = ["mp4", "mkv"]
FILE_FOLDER = [
    # "F:\\private",
    # "F:\\private\\其他",
    "F:\\private\\国产"
]
CHANGE = True

files = []

for folder in FILE_FOLDER:
    for f in [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]:
        if f.split(".")[-1] in FILE_EXT_NAMES:
            files.append(folder + "\\" + f)

print(f"files count: {len(files)}")
while True:
    file = random.choice(files)
    print(file)
    os.startfile(file)
    d = input("Press Enter to continue, 'd' to delete file...")
    if d == "d":
        files.remove(file)
        newFile = random.choice(files)
        print(newFile)
        os.startfile(newFile)
        os.remove(file)
    if CHANGE:
        files.remove(file)
