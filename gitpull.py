import os
import stat
import time
import shutil
from git import Repo

REPO_URL = "git@gitee.com:xsi640/bed.git"
REPO_BRANCH = "master"
LOCAL_PATH = "F:\\temp\\bed"
INVOKE_INTERVAL = 60


def readonly_handler(func, path, exc_info):
    os.chmod(path, stat.S_IWUSR)
    func(path)


if os.path.exists(LOCAL_PATH):
    shutil.rmtree(LOCAL_PATH, onerror=readonly_handler)
else:
    os.makedirs(LOCAL_PATH)

repo = Repo.clone_from(url=REPO_URL, to_path=LOCAL_PATH)
remote = repo.remote()
while True:
    remote.fetch()
    remote.pull()
    time.sleep(INVOKE_INTERVAL)
