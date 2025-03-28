import os, time, datetime, logging, hashlib, json, requests, logging, threading
import random

logging.basicConfig(level=logging.INFO)
console_handler = logging.StreamHandler()
logging.getLogger().addHandler(console_handler)

MID = 46616
ORDER_WAY = 0
TOKENS = {
    "suyang": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjEzNjkxMjYyODUzIiwiUm9sZUlkcyI6IiIsInJvbGUiOiIiLCJSZWFsTmFtZSI6IuiLj-aJrCIsIlVzZXJJZCI6IjM0MDQ3IiwiRGVwdElkIjoiMCIsIkRlcHRDb2RlIjoiIiwiRGVwdE5hbWUiOiIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDI2LzIvNyA2OjIwOjE2IiwibmJmIjoxNzM4OTA5MjE2LCJleHAiOjE3NzA0NDUyMTYsImlhdCI6MTczODkwOTIxNiwiaXNzIjoiaG9uZ3hpbiIsImF1ZCI6Imhvbmd4aW4ifQ.4kvNF5xMd4tL8SXIa4cCc7Cs-LFE2Pb1yc3QTUtac8Y",
    "wufang": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjE4NzAxMTE2ODQ2IiwiUm9sZUlkcyI6IiIsInJvbGUiOiIiLCJSZWFsTmFtZSI6IuWQtOiKsyIsIlVzZXJJZCI6IjUyODEyIiwiRGVwdElkIjoiMCIsIkRlcHRDb2RlIjoiIiwiRGVwdE5hbWUiOiIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDI1LzcvMTggMTozNTowMSIsIm5iZiI6MTcyMTI2NjUwMSwiZXhwIjoxNzUyODAyNTAxLCJpYXQiOjE3MjEyNjY1MDEsImlzcyI6Imhvbmd4aW4iLCJhdWQiOiJob25neGluIn0.UevQttiGIIF6TE_XRxP_tR1KTlLW2A538_ACEVvrdp8",
    "yyx": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjEzNDM5NDE1NDE5IiwiUm9sZUlkcyI6IiIsInJvbGUiOiIiLCJSZWFsTmFtZSI6IuadqOiJs-mcniIsIlVzZXJJZCI6IjMzMzYxIiwiRGVwdElkIjoiMCIsIkRlcHRDb2RlIjoiIiwiRGVwdE5hbWUiOiIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDI1LzgvMTUgOToxODozOCIsIm5iZiI6MTcyMzcxMzUxOCwiZXhwIjoxNzU1MjQ5NTE4LCJpYXQiOjE3MjM3MTM1MTgsImlzcyI6Imhvbmd4aW4iLCJhdWQiOiJob25neGluIn0.VRqFKLhJvZqSDUv6t8faI_Q32xGYg6M9D8YkzB95Qok"
}
URL = "https://tsg.fscac.org:5134"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
START_TIME = "2025-03-20 10:00:00"



def sign(keywords: dict) -> str:
    keys = sorted(set(keywords.keys()))
    sortKeys = []
    for key in keys:
        if keywords[key] is not None:
            sortKeys.append(key)
    urlParams = ""
    for index, v in enumerate(sortKeys):
        if index == len(sortKeys) - 1:
            urlParams += f"{v}={keywords[v]}"
        else:
            urlParams += f"{v}={keywords[v]}&"
    return hashlib.md5(urlParams.encode("utf-8")).hexdigest().upper()


def check_token(token: str) -> bool:
    timestamp = int(time.time() * 1000)
    newData = {
        "token": token,
        "timestamps": timestamp
    }
    headers = {
        'Content-Type': 'application/json',
        'Sign': sign(newData),
        'Timestamps': str(timestamp),
        'User-Agent': USER_AGENT,
        'Authorization': f"Bearer {token}"
    }
    try:
        logging.log(logging.INFO, f"get {URL}/api/FW_RegUser/GetUserInfo {headers}")
        response = requests.get(f"{URL}/api/FW_RegUser/GetUserInfo", headers=headers).json()
        logging.log(logging.INFO, response)
        if response["result"] == 1:
            return True
        return False
    except Exception as e:
        logging.log(logging.ERROR, e)
        return False


def post_server(token: str) -> bool:
    timestamp = int(time.time() * 1000)
    data = {
        "Mid": MID,
        "OrderWay": ORDER_WAY,
    }
    newData = {
        "Mid": MID,
        "OrderWay": ORDER_WAY,
        "token": token,
        "timestamps": timestamp
    }
    headers = {
        'Content-Type': 'application/json',
        'Sign': sign(newData),
        'Timestamps': str(timestamp),
        'User-Agent': USER_AGENT,
        'Authorization': f"Bearer {token}"
    }
    try:
        body = json.dumps(data)
        logging.log(logging.INFO, f"post {URL}/api/FW_Module/AddOrder {headers} {body}")
        response = requests.post(f"{URL}/api/FW_Module/AddOrder", headers=headers, data=body).json()
        logging.log(logging.INFO, response)
        if response["result"] == 1:
            return True
        if response["result"] == 0 and "已预约" in response["msg"]:
            return True
        return False
    except Exception as e:
        logging.log(logging.ERROR, e)
        return False


def run_tick(token: str) -> bool:
    while True:
        if post_server(token):
            break
        sleep_time = random.uniform(0.1, 0.02)
        time.sleep(sleep_time)
    return True


def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime(time_stamp / 1000)
    other_style_time = time.strftime(format_string, time_array)
    return other_style_time


def run(name, token):
    if not check_token(token):
        logging.info(f"{name} token 验证失败。")
        return
    while True:
        dt = datetime.datetime.strptime(START_TIME, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(minutes=1)
        if datetime.datetime.now() > dt:
            logging.log(logging.INFO, "开始..." + name)
            if run_tick(token):
                break
        time.sleep(5)
        logging.log(logging.INFO,
                    f"时间未到...{name}:{datetime.datetime.strptime(START_TIME, '%Y-%m-%d %H:%M:%S')}/{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

threads = []
for key, value in TOKENS.items():
    thread = threading.Thread(target=run, args=(key, value))
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()