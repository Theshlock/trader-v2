# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from supportResistanceStrategy import supportResistanceStrategy



intervals = {
"1_Year": relativedelta(years=+1),
"1_Month": relativedelta(months=+1), 
"1_Week": relativedelta(days=+7), 
"1_Day": relativedelta(days=+1), 
"1_Hour": relativedelta(hours=+1)
}

class supportResistanceEngine(object):
    def __init__(self):
        self.supportResistanceStrategies = {}
        for intervalName in intervals:
            print(intervalName)
            self.supportResistanceStrategies[intervalName] = supportResistanceStrategy(intervals[intervalName])
        self.performance = 1
    
    def strategiesOHLCFeeder(self, time, open, high, low, close):
        for strategy in self.supportResistanceStrategies:
            strategy.levelsOHLCFeeder(time, open, high, low, close)

if __name__ == "__main__":
    e = supportResistanceEngine()
    # e.backtest("../Data/Datasets/Binance_BTCUSDT_1h.csv")



#all it recieves is timestamped ohlc data
#thats all it needs
#from this it creates and feeds the supportResistanceStrategies
#and runs backtests as well as live 
#logs activity to a log file