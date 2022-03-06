# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022
from supportResistanceLevels import supportResistanceLevels
from timeframe import timeframe


class supportResistanceStrategy(object):
    def __init__(self, period):
        self.supportResistanceLevelsObjects = supportResistanceLevels()
        self.period = period
        self.timeframe = None

    def levelsOHLCFeeder(self, time, open, high, low, close):
        if low < self.timeframe.low:
            self.timeframe.low = low
        if high > self.timeframe.high:
            self.timeframe.high = high
        if time >= self.timeframe.endTime: # interval concluded, calc levels, create next
            self.timeframe.close = close
            if self.timeframe.startTime + self.timeframe.intervalLength: # Check that it was a full interval
                self.supportResistanceLevels.addTimeframe(self.timeframe)
            self.timeframe = timeframe(time, self.period, close) 


