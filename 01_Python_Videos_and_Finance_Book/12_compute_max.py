import pandas as pd
def get_max_close(symbol):
    #Return the max closing value for stock indicated by symbol

    df = pd.read_csv("data/{}.csv".format(symbol)) # read in data
    return df['Close'].max()

def test_run():
    
    for symbol in ['AAPL', 'IBM']:
        print "Max close"
        print symbol, get_max_close(symbol)

if __name__ == "__main__":
    test_run()