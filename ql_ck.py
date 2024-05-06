import base64
import os
import stat
import time
import shutil
from Crypto.Cipher import DES
from json import dumps

import requests
from git import Repo

REPO_URL = "git@gitee.com:xsi640/bed.git"
REPO_BRANCH = "master"
LOCAL_PATH = "F:\\temp\\bed"
QL_CLIENT_ID = "e2qUfk_CKh8e"
QL_CLIENT_SECRET = "iPpmtfmgaeAbmp-3MpTfIya2"
QL_URL = "http://10.10.1.1:5700"
QL_ENV = "test"
INVOKE_INTERVAL = 5
FILE = "ck.txt"
DES_KEY = b'asd213sa'
DES = DES.new(DES_KEY, DES.MODE_ECB)


def readonly_handler(func, path, exc_info):
    os.chmod(path, stat.S_IWUSR)
    func(path)


def init():
    if os.path.exists(LOCAL_PATH):
        shutil.rmtree(LOCAL_PATH, onerror=readonly_handler)
    else:
        os.makedirs(LOCAL_PATH)


def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text


def update_env(content):
    url = f"{QL_URL}/open/auth/token?client_id={QL_CLIENT_ID}&client_secret={QL_CLIENT_SECRET}"
    auth = ""
    try:
        rjson = requests.get(url).json()
        if rjson['code'] == 200:
            auth = f"{rjson['data']['token_type']} {rjson['data']['token']}"
            url = f"{QL_URL}/open/envs?searchValue={QL_ENV}"
            headers = {"Authorization": auth, "content-type": "application/json"}
            rjson = requests.get(url, headers=headers).json()
            if rjson['code'] == 200:
                print(f"获取环境变量成功")
                env_id = rjson['data'][0]['id']
                headers = {"Authorization": auth, "content-type": "application/json"}
                rjson = requests.put(f"{QL_URL}/open/envs", headers=headers,
                                     data=dumps({"id": env_id,
                                                 "name": QL_ENV,
                                                 "value": DES.decrypt(base64.b64decode(content)).decode("utf-8").rstrip(' ')
                                                 })).json()
                if rjson['code'] == 200:
                    print(f"更新环境变量成功")
                else:
                    print(f"更新环境变量失败：{rjson}")
                return True
            else:
                print(f"获取环境变量失败：{rjson}")
                return False
        else:
            print(f"登录失败：{rjson}")
    except Exception as e:
        print(f"登录失败：{str(e)}")


def check():
    repo = Repo.clone_from(url=REPO_URL, to_path=LOCAL_PATH)
    remote = repo.remote()
    remote.fetch()
    remote.pull()
    file = LOCAL_PATH + "\\" + FILE
    if not os.path.exists(file):
        print("no found file %s", file)
    file_size = os.path.getsize(file)
    file_time = os.path.getmtime(file)
    while True:
        remote.fetch()
        remote.pull()
        if os.path.getsize(file) != file_size or os.path.getmtime(file) != file_time:
            with open(file, 'r') as f:
                update_env(f.read())
            file_size = os.path.getsize(file)
            file_time = os.path.getmtime(file)
        time.sleep(INVOKE_INTERVAL)


if __name__ == '__main__':
    init()
    check()
    # padded_text = pad("ttttt\r\nfffff")
    # print(base64.b64encode(DES.encrypt(padded_text.encode('utf-8'))))
