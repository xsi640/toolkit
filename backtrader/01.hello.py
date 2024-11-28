import backtrader as bt
import pandas as pd
import numpy as np
import datetime
from copy import deepcopy

# 实例化 cerebro
cerebro = bt.Cerebro()
# 打印初始资金
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
# 启动回测
cerebro.run()
# 打印回测完成后的资金
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

print("=============================")

daily_price = pd.read_csv("./data/daily_price.csv", parse_dates=['datetime'])
print(daily_price)

print("=============================")
result = daily_price.query("sec_code=='600466.SH'")
print(result)

print("=============================")