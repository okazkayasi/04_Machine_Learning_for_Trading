import os
import pandas as pd
import matplotlib.pyplot as plt

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
    # read the data
    dates = pd.date_range('2010-01-01', '2012-12-31')
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    df = get_data(symbols, dates)
    # plot_data(df)

    # compute global statistics for each stock
    print df.mean()
    print df.median()
    print df.std()

    # rolling statistics
    # take 20 days rolling mean
    symbols = ['SPY']
    df = get_data(symbols, dates)

    # plot SPY data, retain matplotlib axis object
    ax = df['SPY'].plot(title="SPY rolling mean", label='SPY')

    # compute rolling mean using a 20-day window
    # rm_SPY = pd.rolling_mean(df['SPY'], window=20)
    rm_SPY = pd.rolling_mean(df['SPY'], window=20)

    # add rolling mean to the plot above
    rm_SPY.plot(label='Rolling mean', ax=ax)

    # add axis labels and legend
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    plt.show()


if __name__ == "__main__":
    test_run()
