from pyalgotrade import strategy
from pyalgotrade import technical
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns
import tushare as ts

class DiffEventWindow(technical.EventWindow):
    def __init__(self, period):
        assert(period > 0)
        super(DiffEventWindow, self).__init__(period)
        self.__value = None

    def onNewValue(self, dateTime, value):
        super(DiffEventWindow, self).onNewValue(dateTime, value)
        if self.windowFull():
            lastValue = self.getValues()[0]
            nowValue = self.getValues()[1]
            self.__value = (nowValue - lastValue) / lastValue

    def getValue(self):
        return self.__value

class Diff(technical.EventBasedFilter):
    def __init__(self, dataSeries, period, maxLen=None):
        super(Diff, self).__init__(dataSeries, DiffEventWindow(period), maxLen)

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, diffPeriod=2):
        super(MyStrategy, self).__init__(feed, 1000000)
        self.__instrument = instrument
        self.__position = None
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__diff = Diff(self.__prices, diffPeriod)
        self.__break = 0.05
        self.__withdown = -0.05

    def getDiff(self):
        return self.__diff

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        account = self.getBroker().getCash()
        bar = bars[self.__instrument]
        if self.__position is None:
            one = bar.getPrice() * 500
            oneUnit = account // one
            if oneUnit > 0 :
                self.__position = self.enterLong(self.__instrument, oneUnit * 500, True)
        elif self.__diff[-1] < self.__withdown and not self.__position.exitActive():
            self.__position.exitMarket()

def runStrategy():
    # 下载数据
    jdf = ts.get_k_data("600519",start='2018-07-01',end='2020-07-01')

    # 新建Adj Close字段
    jdf["Adj Close"] =jdf.close

    # 将tushare下的数据的字段保存为pyalgotrade所要求的数据格式
    jdf.columns = ["Date", "Open", "Close", "High", "Low", "Volume", "code", "Adj Close"]

    # 将数据保存成本地csv文件
    jdf.to_csv("jdf.csv", index=False)

    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("jdf", "jdf.csv")

    myStrategy = MyStrategy(feed, "jdf")

    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    plt = plotter.StrategyPlotter(myStrategy)
    plt.getInstrumentSubplot("jdf")
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    myStrategy.run()
    print("Final portfolio value: $%.2f" % myStrategy.getResult())
    plt.plot()

runStrategy()

