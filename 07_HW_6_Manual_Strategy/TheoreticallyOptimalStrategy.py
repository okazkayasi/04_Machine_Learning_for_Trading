import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt
from marketsimcode import Portfolio
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


class tos:


    @staticmethod
    def test_policy(symbol, sd, ed, sv):


        end_date = ed
        start_date = sd
        stocks = symbol

        adj_close = get_data(stocks, pd.date_range(start_date, end_date))
        adj_close.fillna(method='ffill', inplace=True)
        adj_close.fillna(method='bfill', inplace=True)

        adj_close['diff'] = adj_close['JPM'] - adj_close['JPM'].shift(-1)
        adj_close['BUY'] = 0
        adj_close.BUY[adj_close['diff'] > 0] = 'SELL'
        adj_close.BUY[adj_close['diff'] < 0] = 'BUY'

        adj_close['Date'] = adj_close.index
        adj_close['Symbol'] = symbol[0]
        adj_close['Order'] = 'BUY'
        adj_close['Shares'] = 0

        adj_close.Shares[adj_close['BUY'] == 'SELL'] = -1000
        adj_close.Shares[adj_close['BUY'] == 'BUY'] = 1000

        adj_close['Share'] = adj_close['Shares'] - adj_close['Shares'].shift(1)
        adj_close['Share'][0] = adj_close['Shares'][0]

        adj_close.Order[adj_close['Shares'] < 0] = 'SELL'
        adj_close.Order[adj_close['Shares'] > 0] = 'BUY'
        adj_close.Share = abs(adj_close.Share)

        best = adj_close[['Date', 'Symbol', 'Order', 'Share']]
        best['Shares'] = best['Share']
        best = best[['Date', 'Symbol', 'Order', 'Shares']]
        orders_df = best

        optimal = tos.trade(orders_df,sv, ed, sd)
        # print optimal
        daily_opt = tos.compute_daily_returns(optimal)
        # print 'optimal daily return', daily_opt.mean()[0]
        # print 'optimal daily std', daily_opt.std()[0]

        opt_norm = optimal/optimal.values[0][0]

        bench = best.iloc[:1].copy()
        bench['Order'].iloc[0] = "BUY"
        bench['Shares'].iloc[0] = 1000.0
        benchmark = tos.trade(bench, sv, ed, sd)
        # print benchmark
        daily_opt = tos.compute_daily_returns(benchmark)
        # print 'bench daily return', daily_opt.mean()[0]
        # print 'bench daily std', daily_opt.std()[0]   

        bench_norm = benchmark/benchmark.values[0][0]

        fig, ax1 = plt.subplots(figsize=(12,8))
        ax1.set_ylabel('Normalized value', fontsize=14)
        ax1.set_xlabel('Date', fontsize=14)

        ax1.plot(opt_norm, color='black')
        ax1.plot(bench_norm, color='blue')
        plt.title("Optimum vs Benchmark in-sample", fontsize=14)

        # plt.show()
        plt.savefig("Optimum vs Benchmark.png", dpi=100)
        

    @staticmethod
    def trade(orders_df, sv, ed, sd):
        orders_df.sort_index(inplace=True)


        # set dates and required stocks
        end_date = ed
        start_date = sd


        # get data using util
        stocks = list(orders_df.Symbol.drop_duplicates().values)
        adj_close = get_data(stocks, pd.date_range(start_date, end_date))
        adj_close = adj_close.fillna(method='ffill')
        adj_close = adj_close.fillna(method='bfill')

        # date formatting
        date_list = adj_close.index
        date_list = list(date_list)
        ret_df = pd.DataFrame(columns=["Portfolio Value"], index=date_list)
        emp = np.zeros(len(date_list))
        adj_ind = 0
        order_ind = 0
        order_len = len(orders_df.index)

        my_port = Portfolio(cash=sv, comm=0, imp=0, stocks=["JPM"], lenn=len(adj_close.index))

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
    
    @staticmethod
    def compute_daily_returns(df):
        # return DataFrame that have the same number of rows
        daily_return = df.copy()
        daily_return[1:] = (df[1:] / df[:-1].values)
        daily_return.ix[0,:] = 0
        return daily_return[1:]

tos.test_policy(['JPM'], dt.datetime(2008,1,1), dt.datetime(2009,12,31), sv=100000)
