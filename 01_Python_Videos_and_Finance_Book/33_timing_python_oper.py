# using time function

from time import time
import numpy as np

def how_long(func, *args):
    # execute function with given arguments, and measure execution time
    t0 = time()
    result = func(*args)
    t1 = time()
    return result, t1 - t0

def manual_mean(arr):
    # compute mean of all elements in 2D array

    sum = 0
    for i in xrange(0, arr.shape[0]):
        for j in xrange(0, arr.shape[1]):
            sum += arr[i,j]
    return sum / arr.size

def numpy_mean(arr):
    # compute mean using NumPy
    return arr.mean()



def test_run():

    t1 = time()
    print "ML4T"
    t2 = time()
    print "time of print is ", t2 - t1, " seconds"

    # check how fast is NumPy
    nd1 = np.random.random((1000,1000)) # large 2D array

    # time the two funcs
    res_manual, t_manual = how_long(manual_mean, nd1)
    res_numpy, t_numpy = how_long(numpy_mean, nd1)
    print "manual: {}, vs NumPy: {}".format(t_manual, t_numpy)

    # speedUp
    speedup = t_manual/t_numpy
    print "NumPy mean is, ", speedup, "times faster"




if __name__ == "__main__":
    test_run()