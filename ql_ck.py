#!/usr/bin/env python3
# coding: utf-8

import base64
import os
import stat
import shutil
from Crypto.Cipher import DES
import tempfile
import json

import requests
from git import Repo

REPO_URL = "git@gitee.com:xsi640/bed.git"
REPO_BRANCH = "master"
QL_URL = "http://127.0.0.1:5700"
QL_ENV = "JD_COOKIE"
FILE = "ck.txt"
DES_KEY = b'asd213sa'
DES = DES.new(DES_KEY, DES.MODE_ECB)

temp_dir = tempfile.gettempdir() + '/ck_temp'


def readonly_handler(func, path, exc_info):
    os.chmod(path, stat.S_IWUSR)
    func(path)


def init():
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, onerror=readonly_handler)
    else:
        os.makedirs(temp_dir)


def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text


def get_token():
    token_path = '/ql/data/config/auth.json'
    if not os.path.exists(token_path):
        token_path = '/ql/config/auth.json'
    with open(token_path, 'r') as f:
        data = json.loads(f.read())
        return data['token']


def update_env(content):
    token = get_token()
    if not token:
        print(f"获取token失败")
        return

    url = f"{QL_URL}/api/envs?searchValue={QL_ENV}"
    rjson = requests.get(url=url, headers={
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}"
    }).json()
    if rjson['code'] == 200:
        print(f"获取环境变量成功, {rjson}")
        env_id = rjson['data'][0]['id']
        value = DES.decrypt(base64.b64decode(content)).decode("utf-8").rstrip(' ').strip('&')
        print(f'id: {env_id} name:{QL_ENV} value:{value}')
        env_data = {"id": env_id, "name": QL_ENV, "value": value}
        rjson = requests.put(f"{QL_URL}/api/envs", headers={
            "Content-Type": "application/json",
            "authorization": f"Bearer {token}"
        }, data=json.dumps(env_data)).json()
        print(rjson)
        if rjson['code'] == 200:
            print(f"更新环境变量成功")
        else:
            print(f"更新环境变量失败: {rjson['message']}")


def check():
    repo = Repo.clone_from(url=REPO_URL, to_path=temp_dir)
    remote = repo.remote()
    remote.fetch()
    remote.pull()
    file = temp_dir + '/' + FILE
    with open(file, 'r') as f:
        update_env(f.read())


if __name__ == '__main__':
    # init()
    # check()
    padded_text = pad("1111")
    print(base64.b64encode(DES.encrypt(padded_text.encode('utf-8'))))
