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

def get_rolling_mean(values, window):
    return pd.rolling_mean(values, window=window)

def get_rolling_std(values, window):
    return pd.rolling_std(values, window=window)

def get_bollinger_bands(rm, rstd):
    upper_band = rm + 2*rstd
    lower_band = rm - 2*rstd

    return upper_band, lower_band


def test_run():
    # read the data
    dates = pd.date_range('2012-01-01', '2012-12-31')
    symbols = ['SPY']
    df = get_data(symbols, dates)

    # Compute Bollinger Bands
    # 1. Compute rolling mean
    rm_SPY = get_rolling_mean(df['SPY'], window=20)

    # 2. Compute rollinf std dev
    rstd_SPY = get_rolling_std(df['SPY'], window=20)

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)

    # plot raw SPY values, rolling mean and Bollinger bands
    ax = df['SPY'].plot(title="Bollinger bands", label='SPY')
    rm_SPY.plot(label="Rolling mean", ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)
    plt.show()


if __name__ == "__main__":
    test_run()
