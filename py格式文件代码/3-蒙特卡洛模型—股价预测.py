# 导入相关模块
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)

# 获取数据
df = ts.get_k_data(code='600519',start='2018-07-01',end='2020-07-01')
# print(df.head(20))

# 处理数据
df.index = pd.to_datetime(df.date)
# df.drop("date", axis=1, inplace=True)

# 计算浮动比例
df["pchange"] = df.close.pct_change()
# 计算浮动点数
df["change"] = df.close.diff()

# 设定回撤值
withdraw = 0.05
# 设定突破值
breakthrough = 0.05
# 设定账户资金
account = 1000000
# 持有仓位手数
position = 0

def buy(bar):
    global account, position
    print("{}: buy {}".format(bar.date, bar.close))
    # 一手价格
    one = bar.close * 500
    position = account // one
    account = account - (position * one)

def sell(bar):
    global account, position
    # 一手价格
    print("{}: sell {}".format(bar.date, bar.close))
    one = bar.close * 500
    account += position * one
    position = 0

print("开始时间投资时间: ", df.iloc[0].date)
for date in df.index:
    bar = df.loc[date]
    if bar.pchange and bar.pchange > breakthrough and position == 0:
        buy(bar)
    elif bar.pchange and bar.pchange < withdraw and position > 0:
        sell(bar)

print("最终可有现金: ", account)
print("最终持有市值: ", position * df.iloc[-1].close * 100)