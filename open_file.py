import os
import random

DIRECTORY = ['E:\\temp\\aria2']
EXTENDS = ['.mp4']

filelist = []

for directory in DIRECTORY:
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in EXTENDS:
                filelist.append(os.path.join(root, file))

print(f'file count{len(filelist)}')
while True:
    index = random.randint(0, len(filelist))
    f = filelist[index]
    print(f)
    os.startfile(f)
    filelist.remove(f)
    command = input(f"count: {len(filelist)}, 按回车继续...")
    if command == 'q':
        break
    if len(filelist) == 0:
        break
