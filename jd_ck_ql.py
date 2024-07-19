#!/usr/bin/env python3
# coding: utf-8

import base64
import glob
import os
import re
import stat
import shutil
from Crypto.Cipher import DES
import tempfile
import json
import sendNotify

import requests
from git import Repo

REPO_URL = "git@gitee.com:xsi640/bed.git"
REPO_BRANCH = "master"
QL_URL = "http://127.0.0.1:5700"
QL_ENV = "JD_COOKIE"
FILE = "ck_*"
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


def decrypt(content):
    return DES.decrypt(base64.b64decode(content)).decode("utf-8").rstrip(' ')


def encrypt(content):
    while len(content) % 8 != 0:
        content += ' '
    return base64.b64encode(DES.encrypt(content.encode('utf-8'))).decode("utf-8")


def get_token():
    token_path = '/ql/data/config/auth.json'
    if not os.path.exists(token_path):
        token_path = '/ql/config/auth.json'
    with open(token_path, 'r') as f:
        data = json.loads(f.read())
        return data['token']


def update_env(content):
    content = '&'.join(str(x) for x in content)
    print(f"update: {content}")
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
        status = rjson['data'][0]['status']
        print(f'id: {env_id} name:{QL_ENV} value:{content}')
        env_data = {"id": env_id, "name": QL_ENV, "value": content}
        rjson = requests.put(f"{QL_URL}/api/envs", headers={
            "Content-Type": "application/json",
            "authorization": f"Bearer {token}"
        }, data=json.dumps(env_data)).json()
        print(rjson)
        if rjson['code'] == 200:
            print(f"更新环境变量成功")
        else:
            print(f"更新环境变量失败: {rjson['message']}")
        if status == 1:
            rjson = requests.put(f"{QL_URL}/api/envs/enable", headers={
                "Content-Type": "application/json",
                "authorization": f"Bearer {token}"
            }, data=json.dumps([env_id])).json()
            print(rjson)


def check_ck(content):
    rjson = requests.get(url='https://me-api.jd.com/user_new/info/GetJDUserInfoUnion', headers={
        'Host': "me-api.jd.com",
        'Accept': "*/*",
        'Connection': "keep-alive",
        'Cookie': content,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
        "Accept-Language": "zh-cn",
        "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
        "Accept-Encoding": "gzip, deflate, br"
    }).json()
    if rjson['retcode'] == '1001':
        return False
    if rjson['retcode'] == '0':
        return True
    rjson = requests.get(url='https://plogin.m.jd.com/cgi-bin/ml/islogin', headers={
        "Cookie": content,
        "referer": "https://h5.m.jd.com/",
        "User-Agent": "jdapp;iPhone;10.1.2;15.0;network/wifi;Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1"
    }).json()
    if rjson['islogin'] == "1":
        return True
    return False


def check():
    repo = Repo.clone_from(url=REPO_URL, to_path=temp_dir)
    remote = repo.remote()
    remote.fetch()
    remote.pull()
    file = temp_dir + '/' + FILE
    content = set()
    fail_account = set()
    for file in glob.glob(file):
        print(f"发现文件: {file}")
        with open(file, 'r') as f:
            s = f.read()
            print(f"内容: {s}")
            if len(s) > 0:
                s = decrypt(s)
                print(f"解密后: {s}")
                if check_ck(s) == True:
                    content.add(s)
                else:
                    print(f'cookie验证失败...{file}')
                    fail_account.add(re.findall(r"pt_pin=([^; ]+)(?=;?)", s)[0])
    if len(fail_account) > 0:
        try:
            sendNotify.send('cookie验证失败', "账号：" + ",".join(fail_account))
        finally:
            pass
    if len(content) > 0:
        update_env(content)


if __name__ == '__main__':
    init()
    check()
