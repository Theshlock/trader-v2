# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
            self.supportResistanceStrategies[intervalName] = supportResistanceStrategy(intervals[intervalName])
        self.performance = 1
        self.initialised = False

    def timeframeInitialiser(self, time, priceOpen, priceHigh, priceLow, priceClose):
        for strategy in self.supportResistanceStrategies:
            self.supportResistanceStrategies[strategy].levelsOHLCFeeder(time, priceOpen, priceHigh, priceLow, priceClose)
    
    def strategiesOHLCFeeder(self, time, priceOpen, priceHigh, priceLow, priceClose):
        if self.initialised == False:
            self.timeframeInitialiser(time, priceOpen, priceHigh, priceLow, priceClose)
            self.initialised = True
        else:
            for strategy in self.supportResistanceStrategies:
                self.supportResistanceStrategies[strategy].levelsOHLCFeeder(time, priceOpen, priceHigh, priceLow, priceClose)


if __name__ == "__main__":
    engine = supportResistanceEngine()
    df = pd.read_csv("Binance_BTCUSDT_1h.csv")
    print(df.info)

    """Prepare the dataframe with indicators/outputs"""
    df["performance"] = engine.performance

    """Main loop"""
    active_trade = None
    capital = 1000
    for k, row in df.iterrows():
        print(k)
        engine.strategiesOHLCFeeder(datetime.fromtimestamp(row['open_time']), row['open'], row['high'], row['low'], row['close'])
        df.loc[k, 'performance'] = engine.performance
        # print(row)

    """Output section"""
    print(df)

    """Matplotlib section"""
    fig = plt.figure()
    gs = fig.add_gridspec(2, hspace=0)
    ax = gs.subplots(sharex=True)
    
    """Top plot, put the chart and resistance lines here"""
    ax[0].plot(df.index, df['close'], label = 'close')

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