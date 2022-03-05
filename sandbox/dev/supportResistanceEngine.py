# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from timeframe import timeframe
from supportResistanceStrategy import supportResistanceStrategy



periods = {
# "1_Year": relativedelta(years = 1),
# "1_Month": relativedelta(months = 1), 
# "1_Week": relativedelta(weeks = 1), 
# "1_Day": relativedelta(days = 1), 
"1_Hour": relativedelta(hours = 1)
} # periods contain datetimes and instructions on when they start

# When initialising objects, make sure they are aligned to their interval
# Take the current datetime, subtract the 

class supportResistanceEngine(object):
    def __init__(self):
        self.supportResistanceStrategies = {}
        for key, val in periods:
            print(key, val)
            self.supportResistanceStrategies[key] = supportResistanceStrategy()
        self.performance = 1

    def feed(self, time, open, high, low, close):
        for strategy in self.supportResistanceStrategies:
            strategy.feedData(time, open, high, low, close)

if __name__ == "__main__":
    print('ban')
    e = supportResistanceEngine()
    e.backtest("../Data/Datasets/Binance_BTCUSDT_1h.csv")



#all it recieves is timestamped ohlc data
#thats all it needs
#from this it creates and feeds the supportResistanceStrategies
#and runs backtests as well as live 
#logs activity to a log file