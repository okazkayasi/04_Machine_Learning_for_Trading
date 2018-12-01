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

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.q_learner = QLearner.QLearner(num_states=1000, num_actions=3, alpha=0.2, gamma=0.95, rar=0.5, radr=0.99, dyna=0, verbose=False)


    @staticmethod
    def getIndicators(symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        symbols = list(symbol)
        # go to 1 year back for learning
        sd = sd - dt.timedelta(365)


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

        df_back_to_future = df[sd+dt.timedelta(365):]
        df_back_to_future = df_back_to_future / df_back_to_future.IBM[0]


        strategy = pd.DataFrame(index=df_back_to_future.index)
        strategy['moving_average'] = df_back_to_future['20-SMA'] - df_back_to_future['150-SMA']


        ## SLOW STOCHASTIC
        high = pd.rolling_max(adj_close[symbol], window=14)
        low = pd.rolling_min(adj_close[symbol], window=14)
        K = (adj_close[symbol] - low) / (high-low) * 100
        slow_stoch = pd.rolling_mean(K, window=3)

        slow_future = slow_stoch[sd + dt.timedelta(365):]
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



    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):



        # add your code to do learning here


        indicators = getIndicators(symbol, sd, ed, sv)




        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices

        # example use with new colname
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        if self.verbose: print volume

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        trades.values[:,:] = 0 # set them all to nothing
        trades.values[0,:] = 1000 # add a BUY at the start
        trades.values[40,:] = -1000 # add a SELL
        trades.values[41,:] = 1000 # add a BUY
        trades.values[60,:] = -2000 # go short from long
        trades.values[61,:] = 2000 # go long from short
        trades.values[-1,:] = -1000 #exit on the last day
        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"
