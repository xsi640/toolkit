#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Huaisha2049"

import asyncio
from random import random
from socket import timeout
from time import sleep
import pyperclip
import os
import pyppeteer

# 1. download chrome-win.zip from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1181217/
# 2. unzip it to ~/AppData/Local/pyppeteer/pyppeteer/local-chromium/1181205.( Because 1181205 is written in the code, in order not to change the original library code, so here 1181205 is used as the directory name. )
# 3. finally, it seem like this ~/AppData/Local/pyppeteer/pyppeteer/local-chromium/1181205/chrome-win/chrome.exe


def find_cookie(cookies):
    """提取pt_key和pt_pin
    """
    for item in cookies.split('; '):
        if 'pt_pin' in item:
            pt_pin = item
        if 'pt_key' in item:
            pt_key = item
    jd_cookie = pt_pin + ';' + pt_key + ';'
    pyperclip.copy(jd_cookie)  # 拷贝JDcookie到剪切板
    print("Cookie:", jd_cookie)
    print("已拷贝Cookie到剪切板、直接黏贴即可。")
    # return jd_cookie
    os.system('pause')  # 按任意键继续


async def main():
    """使用pyppeteer库来登录京东、并获取cookie
    """
    browser = await pyppeteer.launch(headless=False, dumpio=True, autoClose=False,
                           args=['--no-sandbox', '--window-size=1000,800', '--disable-infobars',
                                 '--proxy-server=http://127.0.0.1:7898'])  # 进入有头模式
    context = await browser.createIncognitoBrowserContext()  # 隐身模式

    # 关闭默认打开的第一个标签页
    pages = await browser.pages()
    if pages:
        await pages[0].close()

    page = await context.newPage()  # 打开新的标签页
    await page.setViewport({'width': 1000, 'height': 800})  # 页面大小一致
    await page.goto('https://home.m.jd.com/myJd/home.action',
                    {'timeout': 1000 * 60})  # 访问主页、增加超时解决Navigation Timeout Exceeded: 30000 ms exceeded报错

    await page.waitFor(1000)
    elm = await page.waitForXPath('//*[@id="myHeader"]', timeout=0)  # 通过判断用户头像是否存在来确定登录状态
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
