# Samuel Lockton ~ lockton.sam@gmail.com ~ 2022
from dateutil.relativedelta import relativedelta
import datetime


class timeframe(object):
    def __init__(self, startTime, intervalLength, priceOpen, priceHigh, priceLow, priceClose):
        self.startTime = startTime
        self.intervalLength = intervalLength
        self.calibrateEndTime(startTime, intervalLength)
        self.priceOpen = priceOpen
        self.priceHigh = None
        self.priceLow = None
        self.priceClose = None
        if self.priceHigh == None:
            self.priceHigh = priceHigh
        if self.priceLow == None:
            self.priceLow = priceLow
        if self.priceClose == None:
            self.priceClose = priceClose # the actual Support/Resistance Level will always be at timeframe close

    def calibrateEndTime(self, startTime, intervalLength):
        if intervalLength == relativedelta(years=+1):# Add interval of time and strip out smaller units of time
            self.endTime = datetime.datetime.strptime((startTime+intervalLength).strftime("%Y"), "%Y")
        if intervalLength == relativedelta(months=+1):
            self.endTime = datetime.datetime.strptime((startTime+intervalLength).strftime("%Y %m"), "%Y %m")
        if intervalLength == relativedelta(days=+7): # weeks run independantly sunday = 0, saturday = 6
            self.endTime = datetime.datetime.strptime((startTime+relativedelta(days=+((7-int(startTime.strftime("%w")))%7)+1)).strftime("%Y %m %d"), "%Y %m %d")
        if intervalLength == relativedelta(days=+1):
            self.endTime = datetime.datetime.strptime((startTime+intervalLength).strftime("%Y %m %d"), "%Y %m %d")
        if intervalLength == relativedelta(hours=+1):
            self.endTime = datetime.datetime.strptime((startTime+intervalLength).strftime("%Y %m %d %H"), "%Y %m %d %H")