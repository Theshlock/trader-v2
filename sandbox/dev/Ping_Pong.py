def pct_change(X1, X2):
    return (X2 - X1)/X1
    
class pp(object):
    """Ping Pong orders are ones which either place all of the
    funds in a long or all of the funds in a short
    The utility of using them is that any strategy that is unprofitable
    can be switched into a profitable one by simple reversing the longs 
    to shorts and vice versa.
    This does not account for fees however."""
    def __init__(self, prediction, entry):
        self.prediction = prediction
        self.entry = entry

    def position_delta(self, current_price):
        return pct_change(current_price) # finish this off