# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022

class supportResistanceLevels(object):
    """Contains an array of Support/Resistance Levels"""
    def __init__(self):
        self.supportResistanceLevels = {}
        self.priceBuffer = [None] * 3 # holds and checks prices for reversals

    def levelFeeder(self, timeframe):
        self.priceBuffer.insert(0, timeframe.priceClose) # add item to price buffer
        self.priceBuffer.pop(-1) # remove last item
        if self.priceBuffer[-1] != None: # check that the buffer is full
            if (self.priceBuffer[0] > self.priceBuffer[1] and self.priceBuffer[1] < self.priceBuffer[2]) or (self.priceBuffer[0] < self.priceBuffer[1] and self.priceBuffer[1] > self.priceBuffer[2]): # if the timeframe before last is an inflection point 
                self.supportResistanceLevels[str(timeframe.endTime)] = timeframe # store it as a Support/Resistance Level