# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from dateutil.relativedelta import relativedelta
from supportResistanceStrategy import supportResistanceStrategy


intervals = {
# "1_Year": relativedelta(years=+1),
"1_Month": relativedelta(months=+1), 
# "1_Week": relativedelta(days=+7), 
# "1_Day": relativedelta(days=+1), 
# "1_Hour": relativedelta(hours=+1)
}

class supportResistanceEngine(object):
    def __init__(self):
        self.supportResistanceStrategies = {}
        for intervalName in intervals:
            self.supportResistanceStrategies[intervalName] = supportResistanceStrategy(intervals[intervalName])
        self.performance = 1000
        self.initialised = False

    def timeframeInitialiser(self, time, priceOpen, priceHigh, priceLow, priceClose):
        for strategy in self.supportResistanceStrategies:
            self.supportResistanceStrategies[strategy].OHLCFeeder(time, priceOpen, priceHigh, priceLow, priceClose)
    
    def OHLCFeeder(self, time, priceOpen, priceHigh, priceLow, priceClose):
        if self.initialised == False:
            self.timeframeInitialiser(time, priceOpen, priceHigh, priceLow, priceClose)
            self.initialised = True
        else:
            for strategy in self.supportResistanceStrategies:
                # print('perf', self.supportResistanceStrategies[strategy].OHLCFeeder(time, priceOpen, priceHigh, priceLow, priceClose))
                self.performance *= self.supportResistanceStrategies[strategy].OHLCFeeder(time, priceOpen, priceHigh, priceLow, priceClose)
            # input("next? ")


if __name__ == "__main__":
    engine = supportResistanceEngine()

    #####DATASET SWITCHER#####
    """Binance_BTCUSDT_1h.csv"""
    # df = pd.read_csv("Binance_BTCUSDT_1h.csv", parse_dates=['timestamp'], index_col=['timestamp'])

    """bitstamp_hourly.csv"""
    # df = pd.read_csv('bitstamp_hourly.csv', index_col=['timestamp'])
    df = pd.read_csv('bitstamp_hourly.csv') # read csv
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s') # convert UNIX to dateTime
    df = df.set_index('timestamp') # set the index as timestamp
    
    #####END DATASET SWITCHER#####

    df["performance"] = engine.performance

    """Main loop"""
    active_trade = None
    for k, row in df.iterrows():
        engine.OHLCFeeder(k, row['open'], row['high'], row['low'], row['close'])
        df.loc[k, 'performance'] = engine.performance
        print(engine.performance)
        # input("next?")
 
    """Output section"""
    print(df)

    # print(df.index[-1:].to_pydatetime()[0])

    """Matplotlib config"""
    fig = plt.figure()
    gs = fig.add_gridspec(2, hspace=0) # 2 plots
    ax = gs.subplots(sharex=True)
    
    """Top plot, put the chart and resistance lines here"""
    ax[0].plot(df.index, df['high'], label = 'high')
    ax[0].plot(df.index, df['low'], label = 'low')
    ax[0].plot(df.index, df['close'], label = 'close')

    firstYearlyLevel = None
    firstMonthlyLevel = None
    firstWeeklyLevel = None
    firstDailyLevel = None
    firstHourlyLevel = None

    # plotIntervals = [firstYearlyLevel, firstMonthlyLevel, firstWeeklyLevel, firstDailyLevel, firstHourlyLevel]

    # for SRLevelName, SRLevel in engine.supportResistanceStrategies['1_Year'].supportResistanceLevels.items():
    #     # print(f"{SRLevel.startTime+(SRLevel.intervalLength*1)}, {df.index[-1:].to_pydatetime()[0]}, {min(SRLevel.startTime+(SRLevel.intervalLength*1), df.index[-1:].to_pydatetime()[0])}")
    #     ax[0].hlines(y=SRLevel.priceClose, xmin=SRLevel.endTime, xmax=SRLevel.startTime+(SRLevel.intervalLength*1), color='black')
    #     if not firstYearlyLevel:
    #         firstYearlyLevel = SRLevel.endTime

    for SRLevelName, SRLevel in engine.supportResistanceStrategies['1_Month'].supportResistanceLevels.items():
        # print(f"{SRLevel.startTime+(SRLevel.intervalLength*8)}, {df.index[-1:].to_pydatetime()[0]}, {min(SRLevel.startTime+(SRLevel.intervalLength*8), df.index[-1:].to_pydatetime()[0])}")
        ax[0].hlines(y=SRLevel.priceClose, xmin=SRLevel.endTime, xmax=min(SRLevel.startTime+(SRLevel.intervalLength*8),df.index[-1:].to_pydatetime()[0]), color='blue')
        if not firstMonthlyLevel:
            firstMonthlyLevel = SRLevel.endTime

    # for SRLevelName, SRLevel in engine.supportResistanceStrategies['1_Week'].supportResistanceLevels.items():
    #     # print(f"{SRLevel.startTime+(SRLevel.intervalLength*16)}, {df.index[-1:].to_pydatetime()[0]}, {min(SRLevel.startTime+(SRLevel.intervalLength*16), df.index[-1:].to_pydatetime()[0])}")
    #     ax[0].hlines(y=SRLevel.priceClose, xmin=SRLevel.endTime, xmax=min(SRLevel.startTime+(SRLevel.intervalLength*16),df.index[-1:].to_pydatetime()[0]), color='red')
    #     if not firstWeeklyLevel:
    #         firstWeeklyLevel = SRLevel.endTime

    # for SRLevelName, SRLevel in engine.supportResistanceStrategies['1_Day'].supportResistanceLevels.items():
    #     # print(f"{SRLevel.startTime+(SRLevel.intervalLength*64)}, {df.index[-1:].to_pydatetime()[0]}, {min(SRLevel.startTime+(SRLevel.intervalLength*64), df.index[-1:].to_pydatetime()[0])}")
    #     ax[0].hlines(y=SRLevel.priceClose, xmin=SRLevel.endTime, xmax=min(SRLevel.startTime+(SRLevel.intervalLength*64),df.index[-1:].to_pydatetime()[0]), color='orange')
    #     if not firstDailyLevel:
    #         firstDailyLevel = SRLevel.endTime

    # for SRLevelName, SRLevel in engine.supportResistanceStrategies['1_Hour'].supportResistanceLevels.items():
    #     # print(f"{SRLevel.startTime+(SRLevel.intervalLength*512)}, {df.index[-1:].to_pydatetime()[0]}, {min(SRLevel.startTime+(SRLevel.intervalLength*512), df.index[-1:].to_pydatetime()[0])}")
    #     ax[0].hlines(y=SRLevel.priceClose, xmin=SRLevel.endTime, xmax=min(SRLevel.startTime+(SRLevel.intervalLength*512),df.index[-1:].to_pydatetime()[0]), color='blue')
    #     if not firstHourlyLevel:
    #         firstHourlyLevel = SRLevel.endTime

    # while firstYearlyLevel < df.index[-1:].to_pydatetime()[0]:
    #     ax[0].axvline(x = firstYearlyLevel, alpha = 0.8)
    #     firstYearlyLevel += relativedelta(years=+1)

    while firstMonthlyLevel < df.index[-1:].to_pydatetime()[0]:
        ax[0].axvline(x = firstMonthlyLevel, alpha = 0.6)
        firstMonthlyLevel += relativedelta(months=+1)

    # while firstWeeklyLevel < df.index[-1:].to_pydatetime()[0]:
    #     ax[0].axvline(x = firstWeeklyLevel, alpha = 0.4)
    #     firstWeeklyLevel += relativedelta(weeks=+1)

    # while firstDailyLevel < df.index[-1:].to_pydatetime()[0]:
    #     ax[0].axvline(x = firstDailyLevel, alpha = 0.2)
    #     firstDailyLevel += relativedelta(days=+1)

    plt.xlabel("time")
    ax[0].legend()

    """Bottom plot, put performance and metadata here"""
    ax[1].plot(df.index, df['performance'])
    plt.yscale("log")

    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off

    plt.show()