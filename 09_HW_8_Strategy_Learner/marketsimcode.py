"""MC2-P1: Market simulator.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Mehmet Oguz Kazkayasi (replace with your name)
GT User ID: mkazkayasi3 (replace with your User ID)
GT ID: 903369796 (replace with your GT ID)
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


class Portfolio:

    def __init__(self, cash=0, comm=0, imp=0, stocks=[], lenn=0):
        self.stocks = stocks
        self.commission = comm
        self.impact = imp
        self.arr = np.zeros((lenn+1, len(stocks)+2))
        self.arr[0, -2] = cash
        self.arr[0, -1] = cash



    def buy_stock(self, stock_name, price, number_of_shares, indexx):


        cash_ind = -2
        port_ind = -1

        stock_ind = self.stocks.index(stock_name)


        self.arr[indexx, stock_ind] = self.arr[0, stock_ind]
        self.arr[indexx, stock_ind] += number_of_shares
        self.arr[0, stock_ind] = self.arr[indexx, stock_ind]


        self.arr[indexx, cash_ind] = self.arr[0, cash_ind]
        self.arr[indexx, cash_ind] -= price * number_of_shares
        self.arr[0, cash_ind] = self.arr[indexx, cash_ind]


        self.arr[indexx, cash_ind] -= self.commission
        self.arr[indexx, cash_ind] -= self.impact * number_of_shares * price
        self.arr[0, cash_ind] = self.arr[indexx, cash_ind]


    def sell_stock(self, stock_name, price, number_of_shares, indexx):
        # if I already have it

        cash_ind = -2
        port_ind = -1

        stock_ind = self.stocks.index(stock_name)


        self.arr[indexx, stock_ind] = self.arr[0, stock_ind]
        self.arr[indexx, stock_ind] -= number_of_shares
        self.arr[0, stock_ind] = self.arr[indexx, stock_ind]

        self.arr[indexx, cash_ind] = self.arr[0, cash_ind]
        self.arr[indexx, cash_ind] += price * number_of_shares
        self.arr[0, cash_ind] = self.arr[indexx, cash_ind]



        self.arr[indexx, cash_ind] -= self.commission
        self.arr[indexx, cash_ind] -= self.impact * number_of_shares * price
        self.arr[0, cash_ind] = self.arr[indexx, cash_ind]


    def port_value(self, adj_close, indexx):

        val = self.arr[0, -2]
        self.arr[indexx, :] = self.arr[0, :]

        for stock in self.stocks:
            price = adj_close[stock]
            stock_ind = self.stocks.index(stock)
            num = self.arr[indexx, stock_ind]

            val += num * price

        self.arr[indexx, -1] = val
        return val










def compute_portvals(orders_df, start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # read the ordering data and format date
    # orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    orders_df.sort_index(inplace=True)


    # set dates and required stocks
    end_date = orders_df.index.max()
    start_date = orders_df.index.min()


    # get data using util
    stocks = list(orders_df.Symbol.drop_duplicates().values)
    adj_close = get_data(stocks, pd.date_range(start_date, end_date))
    adj_close = adj_close.fillna(method='ffill')
    adj_close = adj_close.fillna(method='bfill')

    # date formatting
    date_list = adj_close.index
    date_list = list(date_list)





    # WHERE MAGIC HAPPENS

    # create one col df
    ret_df = pd.DataFrame(columns=["Portfolio Value"], index=date_list)
    emp = np.zeros(len(date_list))
    adj_ind = 0
    order_ind = 0
    order_len = len(orders_df.index)

    # Portfolio create
    my_port = Portfolio(start_val, commission, impact, stocks, len(date_list))
    while adj_ind < len(date_list):

        while order_ind < order_len and orders_df.index[order_ind] == adj_close.index[adj_ind]:

            sym = orders_df.Symbol.iloc[order_ind]
            dat = date_list[adj_ind]
            price = adj_close[sym].loc[dat]
            buy = orders_df.Order.iloc[order_ind]
            num = orders_df.Shares.iloc[order_ind]
            # print sym, dat, price, buy, num
            if buy == "BUY":
                my_port.buy_stock(sym, price, num, adj_ind+1)
            else:
                my_port.sell_stock(sym, price, num, adj_ind+1)

            order_ind += 1

        emp[adj_ind] = my_port.port_value(adj_close.iloc[adj_ind], adj_ind+1)
        adj_ind += 1

    ret_df["Portfolio Value"] = emp


    return ret_df

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./workspace/ex4.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])


def author():
    return "mkazkayasi3"

if __name__ == "__main__":
    test_code()
