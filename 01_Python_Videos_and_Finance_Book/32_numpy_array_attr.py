import numpy as np

def get_max_index(a):
    # return the index of the maximum value in given 1D array
    return a.argmax()


def test_run():

    a = np.random.random((5,4)) # 5x4 random numbers
    print a.shape
    print a.shape[0] # rows
    print a.shape[1] # columns
    print len(a.shape) # dimensions
    print a.size # number of elements
    print a.dtype

    np.random.seed(693)
    a = np.random.randint(0,10,size=(5,4)) # 5x4 random integers
    print "Array:\n", a

    # sum of elements
    print "sum of the elements: ", a.sum()

    # sum of a dimension - called access
    print "sum of each column: ", a.sum(axis=0)
    print "sum of each row: ", a.sum(axis=1)

    # basic statistics: min, max, mean
    print "min of each column: ", a.min(axis=0)
    print "max of each row: ", a.max(axis=1)
    print "mean of all elements: ", a.mean() # no axis required


    a = np.array([9,6,2,3,12,14,7,10], dtype=np.int32)
    print "array: ", a
    # find the max and its index in array
    print 'max value: ', a.max()
    print 'index of max: ', get_max_index(a)



if __name__ == "__main__":
    test_run()