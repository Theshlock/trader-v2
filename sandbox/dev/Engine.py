# order types
from re import L
from Stop_Loss_Take_Profit import sltp
from Ping_Pong import pp
# strategies
from Double_Top_Double_Bottom import double_top_double_bottom
# utilites
import pandas as pd
import numpy as np
import time

dataframe_columns = ['performance', 'open','high','low','close','open_short','open_long','stop_loss','take_profit', 'close_short','close_long']

def pct_change(X1, X2):
    return (X2 - X1)/X1

class Engine(object):
    def __init__(self):
        # External Variables
        self.liveness = False # bool: default off
        self.logging = True # bool: default on
        self.strategy = None # string
        self.timeframe = 1 # int: default 1
        self.dataset = None # string
        self.graphics = True # bool

        # Internal Variables
        self.trade_type = None # trade object
        self.df = pd.DataFrame(columns=dataframe_columns) # Pandas.Dataframe
        self.open_trades = [] # holds trade objects
        self.performance = 1 # performance 

        print("\nEngine Instance Created\n")

    def add_strategy(self, strategy):
        self.strategy = strategy
        self.trade_type = strategy.trade_type

    def fill_fuel(self, dataset):
        self.dataset = dataset
        self.df = pd.read_csv(dataset)

    def feed_timeframe(self, open, high, low, close):
        """Takes ohlc values, checks trades, feeds_strategy, adds a row to the dataframe"""
        row = {"open": open, "high": high, "low": low, "close": close, "open_short": None, "open_long": None, "stop_loss": None, "take_profit": None, "close_short": None, "close_long": None}
        chk_rtn = self.tf_check_trades(open, high, low, close) # bug, swapping these lines affects the performance
        if chk_rtn:
            row["stop_loss"] = chk_rtn["stop_loss"]
            row["take_profit"] = chk_rtn["stop_loss"]
            row["stop_loss"] = chk_rtn["stop_loss"]
            
        fd_str_rtn = self.tf_feed_strategy(open, high, low, close)  # bug, swapping these lines affects the performance

        self.df = self.df.append([self.performance, row["open"], row["high"], row["low"], row["close"], row["open_short"], row["open_long"], row["stop_loss"], row["take_profit"], row["close_short"], row["close_long"]]) # put all the info into a row and add it to the online dataframe

    def tf_check_trades(self, open, high, low, close):
        """Checks for outputs from any of the stored trade objects"""
        row = {"long": None, "short": None, "stop_loss": None, "take_profit": None}
        for trade_object in self.open_trades[:]:
            force = trade_object.check(open, high, low, close)
            if force != None: # we have combustion
                print('force ', force)
                self.performance *= (1 + force) # multiply the performance by the force
                self.open_trades.remove(trade_object) # remove trade object
                row["stop_loss": trade_object.sl, "take_profit": trade_object.tp]
            

    def tf_feed_strategy(self, open, high, low, close):
        rtn = self.strategy.feed_candle(close)
        if isinstance(rtn, self.trade_type):
            self.open_trades.append(rtn) # store the trade type
            if self.graphics: # if graphics are activated, add the
                # required metrics for the specific trade type
                if isinstance(self.trade_type, sltp):
                    self.df["open_trade"]
                    self.df["stop_loss"]
                    self.df["take_profit"]
                if isinstance(self.trade_type, pp):
                    self.df["long"]
                    self.df["short"]

    def system_check(self):
        if self.strategy == None:
            print("Strategy not found")
            return "failed"
        if self.timeframe == None:
            print("Timeframe not specified")
            return "failed"
        return "ok"

    def stop(self, dataset):
        """Shutdown Procedure"""
        if self.logging == True:
            with open("log.csv", "a") as log_file:
                log_file.write(f"{time.time()},{{name: {type(self.strategy).__name__}, parameters: {self.strategy.parameters()}}},{dataset},{self.performance}\n")

    def backtest(self, dataset):
        if self.system_check() == "ok":
            """Needs to be set up for online use so it needs to build its own dataframe
            Build the template for a row instance in the dataframe
            Fill the row out as data becomes available"""
            for row in pd.read_csv(dataset).itertuples(index = True):
                self.feed_timeframe(row.open, row.high, row.low, row.close)
                print(self.performance)

            self.stop(dataset)


if __name__ == "__main__":
    e = Engine()
    e.add_strategy(double_top_double_bottom(0.001, 100, 200))
    e.timeframe = 1
    e.backtest("../Data/Datasets/Binance_BTCUSDT_1h.csv")
    print(e.performance)



"""
Steps to run backtest
Nominate Strategy
Nominate Dataset and load matrix
Add graphical output vectors to matrix
Add capital vector
Feed row vectors to Strategy
Keep track of 

Each order should have an interface,
call should look like feed_candle

Think about responsibilities
What should the resonsibility of the engine be?

What should the responsibility of the strategy be?

What should the responsibility of the trade_type be?
"""