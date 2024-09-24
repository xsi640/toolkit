from datetime import datetime, timedelta

import requests

# 输入日期
start_date_str = input("请输入开始日期 (格式: YYYY-MM-DD): ")
end_date_str = input("请输入结束日期 (格式: YYYY-MM-DD): ")

# 将字符串转换为日期对象
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

# 打印中间的所有日期
dates = set()
current_date = start_date
while current_date <= end_date:
    dates.add(current_date.strftime("%Y-%m-%d"))
    current_date += timedelta(days=1)

months = set()
for date in dates:
    months.add(date[:7])


workdays = set()
for month in months:
    url = f"https://api.haoshenqi.top/holiday?date={month}"
    rjson = requests.get(url).json()
    for item in rjson:
        if item["status"] == 0 or item["status"] == 2: #工作日
            workdays.add(item["date"])

with open('output.txt', 'w') as file:
    for date in sorted(dates):
        if date in workdays:
            file.write(f"{date}\n")

print("写入完成。")