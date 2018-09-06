# plot a scatterplots

import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

from util import get_data, plot_data


def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.ix[0, :] = 0 # set row 0 to 0
    return daily_returns



def test_run():
    # SPY vs XOM and SPY vs 

    # read data
    dates = pd.date_range('2009-01-01', '2012-12-31')
    symbols = ['SPY', 'XOM', 'GLD']
    df = get_data(symbols, dates)

    # compute daily returns
    daily_returns = compute_daily_returns(df)

    # scatterplot SPY vs XOM
    daily_returns.plot(kind='scatter', x='SPY', y='XOM')
    beta_XOM, alpha_XOM = np.polyfit(daily_returns['SPY'], daily_returns['XOM'],1)
    plt.plot(daily_returns['SPY'], beta_XOM*daily_returns['SPY'] + alpha_XOM, '-', color='r')
    print 'beta_XOM: ', beta_XOM
    print 'alpha_XOM: ', alpha_XOM 
    plt.show()




    # scatterplot SPY vs GLD
    daily_returns.plot(kind='scatter', x='SPY', y='GLD')
    beta_XOM, alpha_XOM = np.polyfit(daily_returns['SPY'], daily_returns['GLD'],1)
    plt.plot(daily_returns['SPY'], beta_XOM*daily_returns['SPY'] + alpha_XOM, '-', color='r')
    print 'beta_XOM: ', beta_XOM
    print 'alpha_XOM: ', alpha_XOM
    plt.show()

    # calculate correlation coeff
    print daily_returns.corr(method='pearson')



if __name__ == "__main__":
    test_run()