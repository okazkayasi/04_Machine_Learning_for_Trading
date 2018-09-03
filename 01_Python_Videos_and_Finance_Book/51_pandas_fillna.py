import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def symbol_to_path(symbol, base_dir="data"):
    # return CSV file path given ticker symbol
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    # read stock data (adj close) for given symbols from CSV files
    df = pd.DataFrame(index = dates)
    if 'SPY' not in symbols:
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        # read and join data for each symbol
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date', parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])

        # rename the col to prevent crash
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        
        
        df = df.join(df_temp) #use default how='left'

        if symbol == 'SPY': # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df

def plot_data(df, title="Stock prices"):
    # plot stock prices

    ax = df.plot(title=title, fontsize=11)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show() #must be called to show plots in some environments

def plot_selected(df, columns, start_index, end_index):
    # plot the desired columns over index values in the given range

    to_plot = df.ix[start_index : end_index, columns]
    plot_data(to_plot, title="Selected Stock Prices")

def test_run():
    symbollist = ['JAVA', 'FAKE1', 'FAKE2']
    start_date='2005-12-31'
    end_date='2014-12-07'

    # create adate range
    idx = pd.date_range(start_date, end_date)

    # get adjusted close of each
    df_data = get_data(symbollist, idx)
    df_data.fillna(method='ffill', inplace=True)
    df_data.fillna(method='bfill', inplace=True)
    plot_data(df_data)

if __name__ == "__main__":
    test_run()
