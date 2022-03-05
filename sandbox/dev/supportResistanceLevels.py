# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022
from supportResistanceLevel import supportResistanceLevel

class supportResistanceLevels(object):
    """Contains an array of supportResistanceLevels"""
    def __init__(self):
        self.supportResistanceLevels = {}
        self.priceBuffer = [None] * 3 # holds and checks prices for reversals

    def addTimeframe(self, timeframe):
        self.priceBuffer.insert(0, timeframe.close) # add item to price buffer
        self.priceBuffer.pop(-1) # remove last item
        if self.priceBuffer[-1] != None: # check that 3 timeframes have been fed
            if (self.priceBuffer[0] > self.priceBuffer[1] and self.priceBuffer[1] < self.priceBuffer[2]) or (self.priceBuffer[0] < self.priceBuffer[1] and self.priceBuffer[1] > self.priceBuffer[2]): # if the 
                self.supportResistanceLevels.append(supportResistanceLevel(timeframe.close, timeframe))