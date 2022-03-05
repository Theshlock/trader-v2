#Samuel Lockton 2021

"""The framework used to execute the Double Top Double Bottom Strategy"""

from Stop_Loss_Take_Profit import sltp

def pct_change(X1, X2):
    return (X2 - X1)/X1

class reversal(object):
    """Object containing instance of a reversal"""
    def __init__(self, point, point_type, close_sens):
        self.point = point # price value
        self.point_type = point_type # min or max
        self.close_sens = close_sens # percentage of retracement with which price needs to close within to open trade

class price_buffer(object):
    """Circular List of size 3 used to check points for minima and maxima"""
    def __init__(self):
        self.list = [None] * 3

    def add_item(self, price):
        self.list.insert(0,price)
        self.list.pop(-1)

    def check_for_reversal(self):
        if self.list[-1] == None: # wait til the buffer is full
            return None
        if self.list[1] > self.list[0] and self.list[1] > self.list[2]:
            return "max" # previous price is a maxima
        if self.list[1] < self.list[0] and self.list[1] < self.list[2]:
            return "min" # previous price is a minima
        else:
            return None

class double_top_double_bottom(object):
    """Object Representing Double Top, Double Bottom strategy. 
    Takes candles and:
    - Finds reversal points
    - Checks reversal points for trades
    """
    def __init__(self, close_sens, sl_val, tp_val):
        self.close_sens = close_sens # proximity to initial reversal to initiate trade
        self.sl_val = sl_val # stop loss at this percent of retracement
        self.tp_val = tp_val # take profit at this percent of retracement
        self.price_buffer = [None] * 3 # holds and checks prices for reversals
        self.reversals = []
        self.trade_type = sltp

    def parameters(self):
        """returns json string specifying defined parameters"""
        return f"{{close_sens: {self.close_sens}, sl_val: {self.sl_val}, tp_val: {self.tp_val}}}"

    def add_item_to_price_buffer(self, price):
        self.price_buffer.insert(0, price)
        self.price_buffer.pop(-1)

    def check_for_reversals(self, price):
        """Scan the candle buffer for minima and maxima"""
        if self.price_buffer[-1] == None:
            return
        if self.price_buffer[1] > self.price_buffer[0] and self.price_buffer[1] > self.price_buffer[2]: # . ' .
            self.reversals.append(reversal(price, "max", self.close_sens))
        if self.price_buffer[1] < self.price_buffer[0] and self.price_buffer[1] < self.price_buffer[2]: # ' . '
            self.reversals.append(reversal(price, "min", self.close_sens))

    def check_maxima_for_double_top(self, price, reversal):
        pcr = pct_change(reversal.point, price)
        if pcr > -self.close_sens and pcr < self.close_sens: # price closed close to reversal point
            return sltp("down", price, price + self.sl_val, price - self.tp_val)

    def check_minima_for_double_bottom(self, price, reversal):
        pcr = pct_change(reversal.point, price)
        if pcr > -self.close_sens and pcr < self.close_sens: # price closed close to reversal point
            return sltp("up", price, price - self.sl_val, price + self.tp_val)

    def check_reversals_for_trades(self, price):
        rtn = None # holds return variable of price check
        for reversal in list(self.reversals):
            if reversal.point_type == "min":
                rtn = self.check_minima_for_double_bottom(price, reversal)
            elif reversal.point_type == "max":
                rtn = self.check_maxima_for_double_top(price, reversal)

            if isinstance(rtn, sltp):
                return rtn

    def feed_candle(self, price):
        """Returns sltp object or none"""
        self.add_item_to_price_buffer(price)
        self.check_for_reversals(price)
        return self.check_reversals_for_trades(price)


if __name__ == "__main__":
    d = double_top_double_bottom(0.001, 100, 200)
    print(d.parameters())

    # print(type(d).__name__) # the name of the class

    # print(globals()['double_top_double_bottom'])
    # print(globals())
    # d = globals()['sltp']
    # print(d.__dict__)

    # constructor = globals()[sltp]
    # instance = constructor()


"""we want to save a class insstance and use it to create a fresh copy of the class"""
