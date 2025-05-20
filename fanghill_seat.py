import os, time, datetime, logging, hashlib, json, requests, logging, threading
import random
from typing import List, Dict, Optional
import math

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


def get_seats(token: str) -> list:
    timestamp = int(time.time() * 1000)
    data = {
        "mid": MID,
        "token": token,
        "timestamps": timestamp
    }
    headers = {
        'Content-Type': 'application/json',
        'Sign': sign(data),
        'Timestamps': str(timestamp),
        'User-Agent': USER_AGENT,
        'Authorization': f"Bearer {token}"
    }
    url = f"{URL}/api/FW_UserCenter/GetUserSeatSettingByMid?mid={MID}"
    try:
        logging.log(logging.INFO, f"get {url}")
        response = requests.get(url, headers=headers).json()
        logging.log(logging.INFO, response)
        if response["result"] == 1:
            return response["data"]["SeatList"]
        return []
    except Exception as e:
        logging.log(logging.ERROR, e)
        return []


def find_best_seats(seats: List[Dict], count: int = 3) -> Optional[List[Dict]]:
    # 过滤可用座位，并按行号、列号排序
    available_seats = sorted(
        [s for s in seats if s["State"] == 1],
        key=lambda s: (s["RowNum"], s["ColNum"])
    )

    # 按行分组
    rows = {}
    for seat in available_seats:
        rows.setdefault(seat["RowNum"], []).append(seat)

    # 找到所有行中连续的 count 个座位
    candidate_seats = []
    for row, row_seats in rows.items():
        temp_list = []
        for seat in row_seats:
            if not temp_list or seat["ColNum"] == temp_list[-1]["ColNum"] + 1:
                temp_list.append(seat)
            else:
                if len(temp_list) >= count:
                    candidate_seats.append(temp_list[:count])
                temp_list = [seat]

        if len(temp_list) >= count:
            candidate_seats.append(temp_list[:count])

    if not candidate_seats:
        return None  # 没有符合条件的座位

    # 计算影院的中间行和中间列
    all_rows = [s["RowNum"] for s in seats]
    all_cols = [s["ColNum"] for s in seats]
    middle_row = (min(all_rows) + max(all_rows)) / 2
    middle_col = (min(all_cols) + max(all_cols)) / 2

    # 选择最接近 (middle_row, middle_col) 的座位组合
    best_choice = min(
        candidate_seats,
        key=lambda g: math.sqrt(
            (sum(s["RowNum"] for s in g) / len(g) - middle_row) ** 2 +
            (sum(s["ColNum"] for s in g) / len(g) - middle_col) ** 2
        ),
        default=None
    )
    return best_choice


def take_seat(rid, token):
    url = f"{URL}/api/FW_UserCenter/SetUserSeat?"
    timestamp = 1742525854547
    data = {
        "Mid": 46616,
        "token": token,
        "timestamps": timestamp
    }
    pass

data = {
    "Mid": 46616,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjEzNjkxMjYyODUzIiwiUm9sZUlkcyI6IiIsInJvbGUiOiIiLCJSZWFsTmFtZSI6IuiLj-aJrCIsIlVzZXJJZCI6IjM0MDQ3IiwiRGVwdElkIjoiMCIsIkRlcHRDb2RlIjoiIiwiRGVwdE5hbWUiOiIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDI2LzIvNyA2OjIwOjE2IiwibmJmIjoxNzM4OTA5MjE2LCJleHAiOjE3NzA0NDUyMTYsImlhdCI6MTczODkwOTIxNiwiaXNzIjoiaG9uZ3hpbiIsImF1ZCI6Imhvbmd4aW4ifQ.4kvNF5xMd4tL8SXIa4cCc7Cs-LFE2Pb1yc3QTUtac8Y",
    "timestamps": 1742525854547
}


# list = get_seats(TOKENS["suyang"])
# print(list)

# sign: 5ED58EF7F253A77603DFD0F9CA9E558A
# timestamps: 1745999148703
# {"Mid":46798,"list":[{"Mid":46798,"SeatId":210}]}

newData = {
    "Mid": 46798,
    "token": TOKENS["suyang"],
    "timestamps": 1745999148703,
    # "SeatId": 210
}

print(sign(newData))
print("5ED58EF7F253A77603DFD0F9CA9E558A")


# print("A80927A4F2AAA797948F41E3A4137AC3")
# print(sign(data))

# def run(name, token):
#     if not check_token(token):
#         logging.info(f"{name} token 验证失败。")
#         return
#     while True:
#         dt = datetime.datetime.strptime(START_TIME, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(minutes=1)
#         if datetime.datetime.now() > dt:
#             logging.log(logging.INFO, "开始..." + name)
#             if run_tick(token):
#                 break
#         time.sleep(5)
#         logging.log(logging.INFO,
#                     f"时间未到...{name}:{datetime.datetime.strptime(START_TIME, '%Y-%m-%d %H:%M:%S')}/{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#
# threads = []
# for key, value in TOKENS.items():
#     thread = threading.Thread(target=run, args=(key, value))
#     thread.start()
#     threads.append(thread)
#
# for t in threads:
#     t.join()
