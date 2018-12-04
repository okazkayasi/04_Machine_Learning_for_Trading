 #!/usr/bin/env python -W ignore::DeprecationWarning
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




class ms:


    @staticmethod
    def test_policy(symbol, sd, ed, sv):


        end_date = ed
        start_date = sd
        stocks = symbol

        start_date = start_date - dt.timedelta(365)


        adj_close = get_data(stocks, pd.date_range(start_date, end_date))
        adj_close.fillna(method='ffill', inplace=True)
        adj_close.fillna(method='bfill', inplace=True)


        rm_jpm = pd.rolling_mean(adj_close["IBM"], window=20)
        rm_150_jpm = pd.rolling_mean(adj_close["IBM"], window=150)
        JP = adj_close[['IBM']]
        JP['150-SMA'] = rm_150_jpm
        JP['20-SMA'] = rm_jpm

        JP_2008 = JP[start_date +dt.timedelta(365):]
        JP_2008 = JP_2008/JP_2008.IBM[0]


        strategy = pd.DataFrame(index=JP_2008.index)
        strategy['moving_average'] = JP_2008['20-SMA'] - JP_2008['150-SMA']


        high = pd.rolling_max(adj_close["IBM"], window=14)
        low = pd.rolling_min(adj_close["IBM"], window=14)
        K = (adj_close["IBM"] - low)/ (high - low) * 100
        slow_stoch = pd.rolling_mean(K, window=3)

        slow_2008 = slow_stoch[start_date +dt.timedelta(365):]
        strategy['slow_stoch'] = slow_2008




        #### MACD
        e = 12
        rm_jpm_1 = pd.rolling_mean(adj_close["IBM"], window=e)
        ema_12 = np.zeros(len(rm_jpm_1.index))
        multiplier = 2./(e+1)
        ema_12[e-1] = rm_jpm_1[e-1]
        for i in range(e, len(adj_close.index)):
            close = adj_close["IBM"].values[i]
            em = ema_12[i-1]
            ema_12[i] = (close - em) * multiplier + em


        e = 26
        rm_jpm_1 = pd.rolling_mean(adj_close["IBM"], window=e)
        ema_26 = np.zeros(len(rm_jpm_1.index))
        multiplier = 2./(e+1)
        ema_26[e-1] = rm_jpm_1[e-1]
        for i in range(e, len(adj_close.index)):
            close = adj_close["IBM"].values[i]
            em = ema_26[i-1]
            ema_26[i] = (close - em) * multiplier + em

        df_macd = pd.DataFrame(rm_jpm_1)
        df_macd['ema_12'] = ema_12
        df_macd['ema_26'] = ema_26
        df_macd['MACD'] = df_macd['ema_12'] - df_macd['ema_26']
        MACD = ema_12 - ema_26
        MACD[:25] = 0

        # signal_line
        e = 9
        rm_macd = pd.rolling_mean(MACD, window=e)
        sig = np.zeros(len(MACD))
        multiplier = 2./(e+1)
        sig[e-1] = rm_macd[e-1]
        for i in range(e, len(MACD)):
            close = MACD[i]
            em = sig[i-1]
            sig[i] = (close - em) * multiplier + em


        df_macd['signal'] = sig
        df_macd['hist'] = df_macd['MACD'] - df_macd['signal']


        strategy['MACD'] = df_macd[start_date +dt.timedelta(365):]['hist']


        strategy['guess'] = 0
        # q1 = strategy.query('moving_average > -0.1 & slow < 30 & MACD > -0.1').index
        # strategy['guess'].iloc[q1] = 1
        strategy.guess.loc[(strategy['moving_average'] > -0.1) & (strategy['slow_stoch'] < 30) & (strategy['MACD'] > -0.1)] = 1

        strategy.guess.loc[(strategy['moving_average'] < 0.1) & (strategy['slow_stoch'] > 30) & (strategy['MACD'] < 0.1)] = -1

        jp = adj_close[['IBM']]
        jp['Date'] = adj_close.index
        jp['Symbol'] = symbol[0]
        jp['Order'] = '-'
        jp['Share'] = None
        jp = jp[start_date + dt.timedelta(365):]
        jp.Order[strategy['guess'] == -1] = "SELL"
        jp.Share[strategy['guess'] == -1] = -1000

        jp.Order[strategy['guess'] == 1] = "BUY"
        jp.Share[strategy['guess'] == 1] = 1000

        jp.Share.fillna(method='ffill', inplace=True)
        jp.Share.fillna(0, inplace=True)
        jp
        jp['Shares'] = jp['Share'] - jp['Share'].shift(1)
        jp['Shares'][0] = jp['Share'][0]

        jp = jp[["Date", "Symbol", "Order", "Shares"]]
        order_book = jp[jp.Shares != 0.0]

        manual = ms.trade(order_book,sv, ed, sd)
        # print manual
        daily_opt = ms.compute_daily_returns(manual)

        daily_opt = daily_opt.replace(0, np.NaN)
        # print daily_opt.mean()
        # print 'manual daily return', daily_opt.mean()[0]
        # print 'manual daily std', daily_opt.std()[0]

        opt_norm = manual/manual.values[0][0]


        bench = order_book.iloc[:1].copy()
        bench['Date'].iloc[0] = sd
        bench['Order'].iloc[0] = "BUY"
        bench['Shares'].iloc[0] = 1000.0
        benchmark = ms.trade(bench, sv, ed, sd)
        # print benchmark
        daily_opt = ms.compute_daily_returns(benchmark)
        daily_opt = daily_opt.replace(0, np.NaN)
        # print 'bench daily return', daily_opt.mean()[0]
        # print 'bench daily std', daily_opt.std()[0]

        bench_norm = benchmark/benchmark.values[0][0]


        fig, ax1 = plt.subplots(figsize=(12,8))
        ax1.set_ylabel('Normalized value', fontsize=14)
        ax1.set_xlabel('Date', fontsize=14)

        ax1.plot(opt_norm, color='black')
        ax1.plot(bench_norm, color='blue')
        plt.title("Manual vs Benchmark out-sample", fontsize=14)
        # plt.show()
        plt.savefig("Manual vs Benchmark in sample.png", dpi=100)


    @staticmethod
    def trade(orders_df, sv, ed, sd):
        orders_df.sort_index(inplace=True)
        # if sv == 0:
        #     print orders_df

        # set dates and required stocks
        end_date = ed
        start_date = sd


        # get data using util
        stocks = list(orders_df.Symbol.drop_duplicates().values)
        adj_close = get_data(stocks, pd.date_range(start_date, end_date))
        adj_close = adj_close.fillna(method='ffill')
        adj_close = adj_close.fillna(method='bfill')

        # date formatting
        # date formatting
        date_list = adj_close.index
        date_list = list(date_list)
        ret_df = pd.DataFrame(columns=["Portfolio Value"], index=date_list)
        emp = np.zeros(len(date_list))
        adj_ind = 0
        order_ind = 0
        order_len = len(orders_df.index)
        my_port = Portfolio(cash=sv, comm=9.95, imp=0.005, stocks=["IBM"], lenn=len(adj_close.index))

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


ms.test_policy(['IBM'], dt.datetime(2010,1,1), dt.datetime(2011,12,31), sv=100000)
