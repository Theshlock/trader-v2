# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022
from supportResistanceLevels import supportResistanceLevels
from timeframe import timeframe


class supportResistanceStrategy(object):
    def __init__(self, period):
        self.supportResistanceLevelsObjects = supportResistanceLevels()
        self.period = period
        self.timeframe = None

    def timeframeIntialiser(self, time, priceOpen, priceHigh, priceLow, priceClose):
        print('initialised')
        self.timeframe = timeframe(time, self.period, priceOpen, priceHigh, priceLow, priceClose)
        print(self.timeframe.__dict__)

    def levelsOHLCFeeder(self, time, priceOpen, priceHigh, priceLow, priceClose):
        if self.timeframe == None:
            self.timeframeIntialiser(time, priceOpen, priceHigh, priceLow, priceClose)
        else:
            if priceLow < self.timeframe.priceLow:
                self.timeframe.priceLow = priceLow
            if priceHigh > self.timeframe.priceHigh:
                self.timeframe.priceHigh = priceHigh
            if time >= self.timeframe.endTime: # interval concluded, calc levels, create next
                self.timeframe.priceClose = priceClose
                if self.timeframe.startTime + self.timeframe.intervalLength: # Check that it was a full interval
                    self.supportResistanceLevelsObjects.levelFeeder(self.timeframe)
                self.timeframe = timeframe(time, self.period, priceClose, priceClose, priceClose, None) 


