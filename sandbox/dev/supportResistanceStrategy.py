# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022
from supportResistanceLevels import supportResistanceLevels
from timeframe import timeframe

def pct_change(X1, X2):
    return (X2 - X1)/X1

class supportResistanceStrategy(object):
    def __init__(self, period):
        self.supportResistanceLevels = {} # holds timeframe objects
        self.priceBuffer = [None] * 3 # holds and checks prices for reversals
        self.period = period
        self.timeframe = None

    def OHLCFeeder(self, time, priceOpen, priceHigh, priceLow, priceClose):
        perf = 1
        if self.timeframe == None:
            self.timeframeIntialiser(time, priceOpen, priceHigh, priceLow, priceClose)
        else:
            if time >= self.timeframe.endTime: # interval concluded
                perf = self.theMechanism(priceOpen, priceHigh, priceLow, priceClose) # call theMechanism before the switcher
                self.intervalSwitcher(time, priceClose) # call intervalSwitcher after the mechanism but before the return
            self.priceWatcher(priceHigh, priceLow)
        return perf

    def timeframeIntialiser(self, time, priceOpen, priceHigh, priceLow, priceClose):
        print('initialised')
        self.timeframe = timeframe(time, self.period, priceOpen, priceHigh, priceLow, priceClose)
        print(self.timeframe.__dict__)

    def priceWatcher(self, priceHigh, priceLow):
        if priceLow < self.timeframe.priceLow:
            self.timeframe.priceLow = priceLow
        if priceHigh > self.timeframe.priceHigh:
            self.timeframe.priceHigh = priceHigh

    def intervalSwitcher(self, time, priceClose):
        self.timeframe.priceClose = priceClose
        if self.timeframe.startTime + self.timeframe.intervalLength: # Check that it was a full interval
            self.levelCreator(self.timeframe)
        self.timeframe = timeframe(time, self.period, priceClose, priceClose, priceClose, None)

    def levelCreator(self, timeframe):
        self.priceBuffer.insert(0, timeframe.priceClose) # add item to price buffer
        self.priceBuffer.pop(-1) # remove last item
        if self.priceBuffer[-1] != None: # check that the buffer is full
            if (self.priceBuffer[0] > self.priceBuffer[1] and self.priceBuffer[1] < self.priceBuffer[2]) or (self.priceBuffer[0] < self.priceBuffer[1] and self.priceBuffer[1] > self.priceBuffer[2]): # if the timeframe before last is an inflection point 
                self.supportResistanceLevels[str(timeframe.endTime)] = timeframe # store it as a Support/Resistance Level

    def theMechanism(self, priceOpen, priceHigh, priceLow, priceClose):
        combinedOutput = 1
        for levelName, level in self.supportResistanceLevels.items(): #
            # from below
            if priceOpen > level.priceClose and priceLow < level.priceClose:
                print(pct_change(level.priceClose, priceClose), level.priceClose, priceClose)
                combinedOutput += pct_change(level.priceClose, priceClose) #somethings wrong when flipping
            # from above
            if priceOpen < level.priceClose and priceHigh > level.priceClose:
                print(-pct_change(level.priceClose, priceClose), level.priceClose, priceClose)
                combinedOutput -= pct_change(level.priceClose, priceClose) #the polarity of these lines doesn't invert the performance
        return combinedOutput
