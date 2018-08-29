import pandas as pd


def get_mean_volume(symbol):
    # Note: data for a stock is stored in a file data/<symbol>.csv



    df = pd.read_csv("data/{}.csv".format(symbol)) # read in data
    
    # TODO: return the mean volume value for stock indicated by symbol

    return df['Volume'].mean()

def test_run():
    
    for symbol in ['AAPL', 'IBM']:
        print "Mean volume"
        print symbol, get_mean_volume(symbol)

if __name__ == "__main__":
    test_run()