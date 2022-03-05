from Engine import Engine
import sys
from Double_Top_Double_Bottom import double_top_double_bottom


# e = Engine()

"""Take a string corresponding to the name of a strategy and create an
instance of the engine with the strategy loaded"""

def main(argv):
    e = Engine()
    if sys.argv[1] == '1': # double top double bottom
        e.add_strategy(double_top_double_bottom(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])) )
    e.timeframe = 1
    e.backtest("../Data/Datasets/Binance_BTCUSDT_1h.csv")
    # print(e.performance)


if __name__ == "__main__":
    print(sys.argv) # print the command line arguments
    main(sys.argv[1:])


"""What do we want to log?
Basically all that is needed to recreate the test
Name, Strategy, Parameters, Dataset, Performance"""