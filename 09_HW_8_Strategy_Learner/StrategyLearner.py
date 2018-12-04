"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch

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

import datetime as dt
import pandas as pd
import util as ut
import numpy as np
import random
import QLearner
import warnings
import sys
from marketsimcode import *
import matplotlib.pyplot as plt

 #!/usr/bin/env python -W ignore::DeprecationWarning
if not sys.warnoptions:
    warnings.simplefilter("ignore")

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.q_learner = QLearner.QLearner(num_states=1000, num_actions=3, alpha=0.01, \
                                      gamma=0.95, rar=0.7, radr=0.999995, dyna=0, verbose=False)



    def getIndicators(self, symbol = "IBM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), sv = 10000):


        # go to 1 year back for learning
        sd = sd - dt.timedelta(365)

        symbols = [symbol]

        # get the data using util
        adj_close = ut.get_data(symbols, pd.date_range(sd, ed))
        adj_close.fillna(method='ffill', inplace=True)
        adj_close.fillna(method='bfill', inplace=True)

        # rolling mean
        rol_mean_20 = pd.rolling_mean(adj_close[symbol], window=20)
        rol_mean_150 = pd.rolling_mean(adj_close[symbol], window=150)
        df = adj_close[symbols]
        df['150-SMA'] = rol_mean_150
        df['20-SMA'] = rol_mean_20

        df_back_to_future = df[sd + dt.timedelta(365) : ]
        df_back_to_future = df_back_to_future / df_back_to_future[symbol][0]


        strategy = pd.DataFrame(index=df_back_to_future.index)
        strategy['moving_average'] = df_back_to_future['20-SMA'] - df_back_to_future['150-SMA']


        ## SLOW STOCHASTIC
        high = pd.rolling_max(adj_close[symbol], window=14)
        low = pd.rolling_min(adj_close[symbol], window=14)
        K = (adj_close[symbol] - low) / (high-low) * 100
        slow_stoch = pd.rolling_mean(K, window=3)
        # print slow_stoch
        slow_future = slow_stoch[sd+dt.timedelta(365):]
        strategy['slow_stoch'] = slow_future

        ### MACD
        e = 12
        rol_mean_e = pd.rolling_mean(adj_close[symbol], window=e)
        ema_12 = np.zeros(len(rol_mean_e.index))
        multiplier = 2./(e+1)
        ema_12[e-1] = rol_mean_e[e-1]
        for i in range(e, len(adj_close.index)):
            close = adj_close[symbol].values[i]
            em = ema_12[i-1]
            ema_12[i] = (close-em) * multiplier + em

        e = 26
        rol_mean_e = pd.rolling_mean(adj_close[symbol], window=e)
        ema_26 = np.zeros(len(rol_mean_e.index))
        multiplier = 2./(e+1)
        ema_26[e-1] = rol_mean_e[e-1]
        for i in range(e, len(adj_close.index)):
            close = adj_close[symbol].values[i]
            em = ema_26[i-1]
            ema_26[i] = (close-em) * multiplier + em

        df_macd = pd.DataFrame(rol_mean_e)
        df_macd['ema_12'] = ema_12
        df_macd['ema_26'] = ema_26
        df_macd['MACD'] = df_macd['ema_12'] - df_macd['ema_26']
        MACD = ema_12 - ema_26
        MACD[:25] = 0

        ## SIGNAL line
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

        strategy['MACD'] = df_macd[sd + dt.timedelta(365):]['hist']
        return strategy



    # def compute_n_day_daily_returns(self, df, n, threshold):
    #     # return DataFrame that have the same number of rows
    #     ibm = df.copy()
    #     ibm[:-n] = np.divide(1, ibm[:-n] / ibm[n:].values)
    #     threshold = self.impact
    #     if threshold < 0.0001:
    #         threshold = 0.001
    #
    #     ibm[-n:] = 1
    #     q = ibm.copy()
    #     q[ibm > 1 + threshold] = 1
    #     q[ibm <= 1 + threshold] = 0
    #     q[ibm < 1 - threshold] = -1
    # #     ibm[ibm.values>]
    #     return q.values




    def compute_n_day_daily_returns(self, df, n, threshold):

        # return DataFrame that have the same number of rows
        ibm = df.copy()
        ibm[1:] = (df[1:] / df[:-1].values)
        q = ibm.copy()
        q[ibm > 1 + threshold] = 1
        q[ibm <= 1 + threshold] = 0
        q[ibm < 1 - threshold] = -1
    #     ibm[ibm.values>]
        return q.values

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):

        # add your code to do learning here
        indicators = self.getIndicators(symbol, sd, ed, sv=100000)


        # get discrete states number
        a = (indicators[indicators.columns[0]].values)
        b = (indicators[indicators.columns[1]].values)
        c = (indicators[indicators.columns[2]].values)

        mov_av = pd.qcut(a, 10, labels=False)
        slow_st = pd.qcut(b, 10, labels=False, duplicates='drop')
        macd = pd.qcut(c, 10, labels=False)
        disc = mov_av*100+slow_st*10+macd

        # where we get the reward
        n = 3
        adj_close = ut.get_data([symbol], pd.date_range(sd, ed))
        adj_close = adj_close[adj_close.columns[1]]
        rewards = self.compute_n_day_daily_returns(adj_close, n, self.impact)


        ## use QLearner

        qqq = 0
        actions = np.zeros(len(rewards))

        a = self.q_learner.querysetstate(disc[0])
        actions[0] = a
        while qqq < 3000000:
            i = 0

            while i < len(rewards)-1:
                i += 1
                qqq += 1
                if a == 0:
                    r = rewards[i]
                elif a == 1:
                    r = 0
                elif a == 2:
                    r = -rewards[i]

                a = self.q_learner.query(disc[i], r)
                actions[i] = a

        df = pd.DataFrame(adj_close)
        df['Date'] = df.index
        df['Symbol'] = symbol
        df['Orders'] = actions
        df['Order1'] = (df['Orders'] - df.Orders.shift(1))

        df.Order1[0] = df.Orders[0] - 1

        df['Order'] = '-'
        df.Order[df['Order1'] > 0] = 'SELL'
        df.Order[df['Order1'] < 0] = 'BUY'
        df['Shares'] = '-'
        df.Shares = abs(df['Order1'] * 1000)


        df = df.loc[df['Order'] != '-']
        order_book = df[["Date", "Symbol", "Order", "Shares"]]


        port_vals = compute_portvals(order_book, start_val=100000, commission=0, impact=self.impact)

        # port_vals.plot()
        # print port_vals.values[-1]/port_vals.values[0]

        fig, ax = plt.subplots(figsize=(10,8))
        ax.set_title(symbol)
        ax.set_ylabel('Total Worth')
        ax.set_xlabel('Date')
        ax.plot(port_vals.index, port_vals.values, label='QLearning')
        if symbol in ["ML4T-220", "SINE_FAST_NOISE"]:
            ax.plot(port_vals.index, np.ones(len(port_vals.values))*2*port_vals.values[0], label='Benchmark')
        else:
            o_book = order_book[:2]
            o_book.index = [dt.datetime(2008,2,1), dt.datetime(2009,12,31)]
            o_book.Date = [dt.datetime(2008,2,1), dt.datetime(2009,12,31)]
            o_book.Order = ["BUY", "SELL"]
            o_book.Shares = [1000., 1000.]
            port_vals1 = compute_portvals(o_book, start_val=100000, commission=0, impact=self.impact)
            ax.plot(port_vals1.index, port_vals1.values, label='Benchmark')
        ax.legend()
        for i in range(len(order_book)):
            if order_book.Order[i] == "BUY":
                plt.axvline(order_book.Date[i], color='green', linewidth = 0.3)
            else:
                plt.axvline(order_book.Date[i], color='red',  linewidth = 0.3)
        plt.savefig(symbol + '.png', dpi=100)
        plt.gcf()


    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):


        indicators = self.getIndicators(symbol, sd, ed, sv)
        a = (indicators[indicators.columns[0]].values)
        b = (indicators[indicators.columns[1]].values)
        c = (indicators[indicators.columns[2]].values)
        mov_av = pd.qcut(a, 10, labels=False)
        slow_st = pd.qcut(b, 10, labels=False, duplicates='drop')
        macd = pd.qcut(c, 10, labels=False)
        disc = mov_av*100+slow_st*10+macd

        n = 5
        adj_close = ut.get_data([symbol], pd.date_range(sd, ed))
        adj_close = adj_close[adj_close.columns[1]]
        rewards = self.compute_n_day_daily_returns(adj_close, n, 0.0)

        actions = np.zeros(len(rewards))
        rewards_1 = np.zeros(len(rewards))
        x = disc[0]
        a = self.q_learner.querysetstate(x)
        i = 0
        actions[0] = a
        while i < len(rewards)-1:
            i += 1
            if a == 0:
                r = rewards[i]
            elif a == 1:
                r = 0
            elif a == 2:
                r = -rewards[i]

            a = self.q_learner.querysetstate(disc[i])

            actions[i] = a

        df = pd.DataFrame(adj_close)
        df['Date'] = df.index
        df['Symbol'] = symbol
        df['Orders'] = actions
        df['Order1'] = (df['Orders'] - df.Orders.shift(1))

        df.Order1[0] = df.Orders[0] - 1

        df['Order'] = '-'
        df.Order[df['Order1'] > 0] = 'SELL'
        df.Order[df['Order1'] < 0] = 'BUY'
        df['Shares'] = '-'
        df.Shares = abs(df['Order1'] * 1000)


        df = df.loc[df['Order'] != '-']
        order_book = df[["Date", "Symbol", "Order", "Shares"]]

        port_vals = compute_portvals(order_book, start_val=100000, commission=0, impact=0)
        # print port_vals.values[-1]/port_vals.values[0]
        order_book.Shares[order_book['Order']=="SELL"] *= -1


        return pd.DataFrame(order_book.Shares)

if __name__=="__main__":
    print "One does not simply think up a strategy"
