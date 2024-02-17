import os, time, datetime, logging, hashlib, json, requests

MID = 43447
ORDER_WAY = 0
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjEzNjkxMjYyODUzIiwiUm9sZUlkcyI6IiIsInJvbGUiOiIiLCJSZWFsTmFtZSI6IuiLj-aJrCIsIlVzZXJJZCI6IjM0MDQ3IiwiRGVwdElkIjoiMCIsIkRlcHRDb2RlIjoiIiwiRGVwdE5hbWUiOiIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDI0LzgvMSAxOjA0OjEzIiwibmJmIjoxNjkwOTM4MjUzLCJleHAiOjE3MjI0NzQyNTMsImlhdCI6MTY5MDkzODI1MywiaXNzIjoiaG9uZ3hpbiIsImF1ZCI6Imhvbmd4aW4ifQ.tQzxkVJkbVJ3GD95XSqDQO9RESIlcnVd_UAiWlP9uyY"
URL = "https://tsg.fscac.org:5134/api/FW_Module/AddOrder"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
START_TIME = "2024-02-17 12:00:00"


def sign(map: dict) -> str:
    keys = sorted(set(map.keys()))
    sortKeys = []
    for key in keys:
        if map[key] is not None:
            sortKeys.append(key)
    urlParams = ""
    for index, value in enumerate(sortKeys):
        if index == len(sortKeys) - 1:
            urlParams += f"{value}={map[value]}"
        else:
            urlParams += f"{value}={map[value]}&"
    return hashlib.md5(urlParams.encode("utf-8")).hexdigest()


def run():
    timestamp = int(time.time() * 1000)
    data = {
        "Mid": MID,
        "OrderWay": ORDER_WAY,
    }
    newData = {
        "Mid": MID,
        "OrderWay": ORDER_WAY,
        "token": TOKEN,
        "timestamps": timestamp
    }
    headers = {
        'Content-Type': 'application/json',
        'Sign': sign(newData),
        'Timestamps': timestamp,
        'User-Agent': USER_AGENT,
        'Authorization': f"Bearer {TOKEN}"
    }
    body = json.dumps(data)
    response = requests.post(URL, headers=headers, data=body).json()
    logging.log(logging.INFO, response)


while True:
    dt = datetime.datetime.strptime(START_TIME, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(minutes=1)
    if datetime.datetime.now() > dt:
        logging.log(logging.INFO, "开始...")
        run()
        break
    time.sleep(60)
    logging.log(logging.INFO, f"时间未到...{time.time()}")
