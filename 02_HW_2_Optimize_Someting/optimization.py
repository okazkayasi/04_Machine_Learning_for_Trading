"""MC1-P2: Optimize a portfolio.
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

Student Name: Tucker Balch (replace with your name)	 		   		 		  
GT User ID: tb34 (replace with your User ID)	 		   		 		  
GT ID: 900897987 (replace with your GT ID)	  		  		    	 		 		   		 		  
"""	   		 		  
		 		  

import pandas as pd		 		  
import matplotlib.pyplot as plt  	 		 		   		 		  
import numpy as np		   		 		  
import datetime as dt 		  
from util import get_data, plot_data	  		    	 		 		   		 		  


def sharpe_ratio(symbols, allocation):
    # compute the sharpe ratio of given portfolio

    # PARAMETERS
    # -------------
    # portfolio: list of stocks 
    # allocation: list of percentage of stocks

    # returns sharpe ratio of the portfolio


    # get mean daily return of each symbol

    err = np.sum((data[:,1] - (line[0]*data[:,0] + line[1]))**2)
    return err

def fit_line(data, error_func):
    # fit a line to given data, using a supplied error func

    # PARAMETERS
    # ---------------
    # data: 2D array where each row is a point (x, y)
    # error_func: function that computes the error between a line and observed data
    # returns the line that minimizes the error func

    # generate initial guess for line model
    l = np.float32([0, np.mean(data[:,1])]) # slope = 0, intercept = mean(y value)

    # plot initial guess
    x_ends = np.float32([-5,5])
    plt.plot(x_ends, l[0] * x_ends + l[1], 'm--', linewidth = 2.0, label="Initial guess")

    # call optimizer to minimize the error func
    result = spo.minimize(error_func, l, args=(data,), method='SLSQP', options={'disp': True})
    plt.show()
    return result.x


    # this returns the daily_returns
def compute_daily_returns(df):
    # return DataFrame that have the same number of rows
    daily_return = df.copy()
    daily_return[1:] = (df[1:] / df[:-1].values)
    daily_return.ix[0,:] = 0

#    return daily_return

    # pandas way
    daily_return = (df/ df.shift(1))-1
    return daily_return

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):		  

    # Read in adjusted closing prices for given symbols, date range 
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations

    # let's calculate average daily returns

    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats

    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        pass

    return allocs, cr, adr, sddr, sr
  
def test_code():  		 		  
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code
    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']
# Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)
    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr
if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()