import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tushare as ts
#画图时显示中文，使用微软雅黑字体，画图时显示负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
# %matplotlib inline

#%%
sh=ts.get_k_data(code='000001',start='2002-01-01',end='2018-07-01',
             ktype='D',autype='qfq')
sh.index=pd.to_datetime(sh.date)  #将数据列表中第0列‘date'设置为索引
#画出上证指数收盘价的走势
sh['close'].plot(figsize=(12,6))
plt.title('上证指数2002-2018年走势图')
plt.xlabel('日期')
plt.show()

#构建一个计算股票收益率和标准差的函数
#默认起始时间为'2002-01-01'
def return_risk(stocks,startdate='2002-01-01'):
    close=pd.DataFrame()
    for stock in stocks.values():
        close[stock]=ts.get_k_data(stock,ktype='D',
     autype='qfq', start=startdate,end='2018-07-01')['close']
    tech_rets = close.pct_change()[1:]
    rets = tech_rets.dropna()
    ret_mean=rets.mean()*100
    ret_std=rets.std()*100
    return ret_mean,ret_std

#画图函数
def plot_return_risk(stocks):
    ret,vol=return_risk(stocks)
    color=np.array([ 0.18, 0.96, 0.75, 0.3, 0.9,0.5])
    plt.scatter(ret, vol, marker = 'o',
    c=color,s = 500,cmap=plt.get_cmap('Spectral'))
    plt.xlabel("日收益率均值%")
    plt.ylabel("标准差%")
    for label,x,y in zip(stocks.keys(),ret,vol):
        plt.annotate(label,xy = (x,y),xytext = (20,20),
            textcoords = "offset points",
             ha = "right",va = "bottom",
            bbox = dict(boxstyle = 'round,pad=0.5',
            fc = 'yellow', alpha = 0.5),
                arrowprops = dict(arrowstyle = "->",
                    connectionstyle = "arc3,rad=0"))
stocks={'上证指数':'sh','深证指数':'sz','沪深300':'hs300',
        '上证50':'sz50','中小板指数':'zxb','创业板指数':'cyb'}
plot_return_risk(stocks)
plt.title("不同股票指数的收益-风险情况")
plt.show()

#%%
stocks1={'中国平安':'601318','格力电器':'000651',
        '招商银行':'600036','恒生电子':'600570',
        '中信证券':'600030','贵州茅台':'600519'}
# startdate='2018-01-01'
plot_return_risk(stocks1)
plt.title("不同股票的收益-风险情况")
plt.show()

#%%
sh["日收益率"] = sh["close"].pct_change()
sh["日收益率"].loc['2002-01-01':].plot(figsize=(12,4))
plt.xlabel('日期')
plt.ylabel('收益率')
plt.title('2002-2018年贵州茅台日收益率')
plt.show()

###这里我们改变一下线条的类型
#(linestyle)以及加一些标记(marker)
sh["日收益率"].loc['2002-01-01':].plot(figsize=
(12,4),linestyle="--",marker="o",color="g")
plt.title('2002-2018年日收益率图')
plt.xlabel('日期')
plt.show()