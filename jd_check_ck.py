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
    for file in glob.glob(file):
        print(f"发现文件: {file}")
        with open(file, 'r') as f:
            s = f.read()
            print(f"内容: {s}")
            if len(s) > 0:
                s = decrypt(s)
                print(f"解密后: {s}")
                if check_ck(s) == True:
                    print(f'cookie验证成功...{file}')
                else:
                    print(f'cookie验证失败...{file}')


if __name__ == '__main__':
    init()
    check()
