def pct_change(X1, X2):
    return (X2 - X1)/X1

class sltp(object):
    """The Classic Trade object
    This one implements an entry price and two exit prices
    One of the exit prices is to take profit and the other is to 
    avoid losses
    When handling these order types the entry order would have to be managed
    The exits also have to be managed, these can have options"""
    def __init__(self, prediction, entry, sl, tp):
        self.prediction = prediction
        self.correctness = None
        self.entry = entry # entry price
        self.sl = sl # stop loss price
        self.tp = tp # take profit price

    def check(self, open, high, low, close):
        """checks for stop loss hits before take profits which does not take into account which one was actually hit first
        Errs on the side of loss in order to not overestimate profits in backtests"""
        if self.prediction == "up":
            if low < self.sl:
                self.correctness = False # unsuccessful prediction
                return pct_change(self.entry, self.sl)
            if high > self.tp:
                self.correctness = True # successful prediction
                return pct_change(self.entry, self.tp)

        if self.prediction == "down":
            if high > self.sl:
                self.correctness = False # unsuccessful prediction
                return -pct_change(self.entry, self.sl)
            if low < self.tp:
                self.correctness = True # successful prediction
                return -pct_change(self.entry, self.tp)

