
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import scipy.optimize as spo

def error(line, data):
    # compute error btwn given line model and observed data

    # PARAMETERS
    # -------------
    # line: tuple/list/array (C0, C1) where C0 is slope and
    # C1 is Y-intercept 
    # data: 2D array where each row is a point (x,y)

    # returns error as a single real value

    err = np.sum((data[:,1] - (line[0]*data[:,0] + line[1]))**2)
    return err

def test_run():
    # define original line
    l_orig = np.float32([4,2])
    print "Original line: C0 = {}, C1 = {}".format(l_orig[0], l_orig[1])
    Xorig = np.linspace(0,10,21)
    Yorig = l_orig[0] * Xorig + l_orig[1]
    plt.plot(Xorig, Yorig,'b--', linewidth=2.0, label='Original Line')

    # generate noisy data
    noise_sigma = 3.0
    noise = np.random.normal(0, noise_sigma, Yorig.shape)
    data = np.asarray([Xorig, Yorig + noise]).T
    plt.plot(data[:, 0], data[:, 1], 'go', label = 'Data points')
    
    # add a legend and show plot
    
    # plt.show()

    x = fit_line(data, error)
    print x
    
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









if __name__ == "__main__":
    test_run()