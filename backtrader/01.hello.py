import backtrader as bt
import pandas as pd
import numpy as np
import datetime
from copy import deepcopy

# data部分
# 开盘价（ Open）、最高价（High）、最低价（Low）、收盘价（Close）、成交量（Volume）、持仓量（OpenInterest）

# 实例化 cerebro
cerebro = bt.Cerebro()

# 设置初始资金100000
cerebro.broker.setcash(100000.0)

# 打印初始资金
print('组合期初资金: %.2f' % cerebro.broker.getvalue())
# 启动回测
cerebro.run()
# 打印回测完成后的资金
print('组合期末资金: %.2f' % cerebro.broker.getvalue())