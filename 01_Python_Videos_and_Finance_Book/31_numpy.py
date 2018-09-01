
# numpy is a wrapper for numerical libraries
# pandas is a wrapper for numpy

import numpy as np


def test_run():
    # list to 1D array
    print np.array([(2,3,4), (5,6,7)])

    print np.empty(5)
    print np.empty((5,4))

    # this creates float 1's if no dtype
    print np.ones((5,4), dtype=np.int)


    # random func
    print np.random.random((5,4)) # tuple
    print np.random.rand(5,4) # no tuple

    print np.random.normal(50,10, size=(2,3)) #std normal 



if __name__ == "__main__":
    test_run()