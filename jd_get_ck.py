#!/usr/bin/env python
# -*- coding:utf-8 -*-
import asyncio
import base64
from idlelib.window import add_windows_to_menu

import pyperclip
import os
import tempfile
import pyppeteer
from Crypto.Cipher import DES
from git import Repo

REPO_URL = "git@gitee.com:xsi640/bed.git"
REPO_BRANCH = "master"
FILE_PREFIX = "ck_"
DES_KEY = b'asd213sa'
DES = DES.new(DES_KEY, DES.MODE_ECB)
temp_dir = tempfile.gettempdir() + '/ck_temp'

# 1. download chrome-win.zip from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1181217/
# 2. unzip it to ~/AppData/Local/pyppeteer/pyppeteer/local-chromium/1181205.( Because 1181205 is written in the code, in order not to change the original library code, so here 1181205 is used as the directory name. )
# 3. finally, it seem like this ~/AppData/Local/pyppeteer/pyppeteer/local-chromium/1181205/chrome-win/chrome.exe

if os.path.exists(temp_dir):
    os.system('rmdir /S /Q "{}"'.format(temp_dir))
os.makedirs(temp_dir)
repo = Repo.clone_from(url=REPO_URL, to_path=temp_dir)
remote = repo.remote()
remote.fetch()
remote.pull()


def decrypt(content):
    return DES.decrypt(base64.b64decode(content)).decode("utf-8").rstrip(' ')


def encrypt(content):
    while len(content) % 8 != 0:
        content += ' '
    return base64.b64encode(DES.encrypt(content.encode('utf-8'))).decode("utf-8")


def update(pt_key, pt_pin):
    file = temp_dir + '\\' + FILE_PREFIX + pt_pin + '.txt'
    if os.path.exists(file):
        os.remove(file)
    with open(file, 'w') as f:
        s = f"pt_key={pt_key};pt_pin={pt_pin}"
        f.write(encrypt(s))
    print(f"更新文件{file}, 内容: {encrypt(s)}")
    repo.git.add('--all')
    repo.git.commit('-m', 'update')
    remote.push()


def find_cookie(cookies):
    for item in cookies.split('; '):
        if 'pt_pin' in item:
            pt_pin = item
        if 'pt_key' in item:
            pt_key = item
    jd_cookie = pt_pin + ';' + pt_key + ';'
    pyperclip.copy(jd_cookie)  # 拷贝JDcookie到剪切板
    print("Cookie:", jd_cookie)
    print("已拷贝Cookie到剪切板、直接黏贴即可。")
    update(pt_key.split('=')[1], pt_pin.split('=')[1])


async def main():
    browser = await pyppeteer.launch(headless=False, dumpio=True, autoClose=False,
                                     args=['--no-sandbox', '--window-size=1000,800', '--disable-infobars'])  # 进入有头模式
    context = await browser.createIncognitoBrowserContext()  # 隐身模式
    pages = await browser.pages()
    if pages:
        await pages[0].close()
    page = await context.newPage()  # 打开新的标签页
    await page.setViewport({'width': 1000, 'height': 800})  # 页面大小一致
    await page.goto('https://home.m.jd.com/myJd/home.action',
                    {'timeout': 1000 * 60})  # 访问主页、增加超时解决Navigation Timeout Exceeded: 30000 ms exceeded报错
    # await page.waitForXPath('//*[@class="avatar"]', timeout=0)
    await page.waitFor(10000)
    elm = await page.waitForXPath('//*[@id="gotoUserInfo"]', timeout=0)  # 通过判断用户头像是否存在来确定登录状态
    if elm:
        cookie = await page.cookies()
        # print(cookie)
        # 格式化cookie
        cookies_temp = []
        for i in cookie:
            cookies_temp.append('{}={}'.format(i["name"], i["value"]))
        cookies = '; '.join(cookies_temp)
        find_cookie(cookies)
        # print("cookies:{}".format(await page.cookies()))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())  # 调用
