import threading

import requests
import time
import re
import json
from flask import Flask, send_file

def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


class jdthor:
    def qrcode(self):  # 保存二维码
        url = "https://qr.m.jd.com/show?appid=133&size=147"
        req = requests.get(url)
        with open("wc.png", mode="wb") as f1:
            f1.write(req.content)
        # print(req.headers)
        self.state(req.cookies.get_dict())

    def state(self, h):  # 查看扫码情况
        while True:
            smdl = h.get('wlfstk_smdl')
            codekey = h.get('QRCodeKey')
            headers = {
                "Referer": "https://union.jd.com/index",
                "Cookie": f"QRCodeKey={codekey}; wlfstk_smdl={smdl}"
            }
            url = f'https://qr.m.jd.com/check?appid=133&token={smdl}&callback=jsonp'
            req = requests.get(url, headers=headers)
            data = loads_jsonp(req.text)
            if data.get('code') == 201:
                print('\t还没扫描呢亲~')  # 未扫描
            elif data.get('code') == 202:
                print('\t\t请确认登陆')  # 请再手机端确认登陆
            elif data.get('code') == 205:
                print('\t\t\t干嘛取消登陆了')
                break  # 取消登陆
            elif data.get('code') == 203:
                print('已经过期了')
                break
            elif data.get('code') == 200:
                self.get(data.get('ticket'), smdl)
                break
            else:
                print(data)
                break
            time.sleep(1)

    def get(self, ticket, smdl):  # 获取Ck
        url = f'https://passport.jd.com/uc/qrCodeTicketValidation?t={ticket}&ReturnUrl=https://union.jd.com/index&callback=jsonp'
        headers = {
            "Referer": "https://union.jd.com/index",
            "Cookie": f"wlfstk_smdl={smdl}"
        }
        req = requests.get(url, headers=headers)
        ckdict = req.cookies.get_dict()
        print(ckdict)

app = Flask(__name__)

@app.route("/")
def display_html():
    html_content = """
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>White Background Image</title>
        <style>
            body {
                background-color: white; /* Set the background color of the webpage to white */
                margin: 0;
                padding: 0;
            }
            .image-container {
                text-align: center;
            }
            .image {
                max-width: 100%;
                height: auto;
                margin: 20px;
            }
        </style>
    </head>
    <body>
        <div class="image-container">
            <img src="/image" alt="qr code" class="image">
        </div>
    </body>
    </html>"""
    return html_content

@app.route('/image')
def display_image():
    return send_file("wc.png", mimetype="image/png")

def jdcookie():
    jd = jdthor()
    jd.qrcode()

if __name__ == '__main__':
    thread = threading.Thread(target=jdcookie)
    thread.start()
    app.run()

{'DeviceSeq': '3faf2392b95945f185e9ef645f0a2711',
 'TrackID': '1wOSppxp4jU9aOQFz81_du7M4jVYhNufIQdLgJbC940p8RTHBBlhbfECCsUBl_Ftys0v5Pg7pfIh1F1c0fxrsjQ',
 'thor': '3E40D81A0A64A53AD4A2C784C68B6A4613CB433F80A652C66865AA75173B7DA5F2D0E8BE7F63C601442D300A9E49B4D0EA063EC95063A7660DC4D69E69221862B2AD82087AE3038347A2BE0A6DC33BD66A4803A816268B56185BAE1617C706A5BCDF9D13EC489B367BDD279411A25639EFE95B73B5019F90F4E35D79030F5B51',
 'flash': '2_5XA1cHs_D5i48ACyJ6C-mRulbW4GI1VnSCkXyW1-OPnv6vyZ01k1b26AJhKd8p0R6FKLclzWaCFWUQOejw4tWEFmNqz6UOZT1tZA-NpwHoUp2-XXnorn27_FNtTx73oU',
 'pinId': 'wExJDvOMp4I', 'pin': 'xsi640', 'unick': 'jdxsi64123', 'ceshi3.com': '203', '_tp': 't5FlCqHStHx%2Bp0u92JCRxQ%3D%3D', 'logining': '1', '_pst': 'xsi640'}