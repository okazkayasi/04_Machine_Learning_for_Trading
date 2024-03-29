"""
template for generating data to fool learners (c) 2016 Tucker Balch
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

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    
    # choose n columns randomly
    cols = np.random.randint(2, 11)

    # create X all integer 0 to 10
    X = np.multiply(np.random.rand(50,cols), np.random.randint(1, 10, size=(50,cols)))
    # Here's is an example of creating a Y from randomly generated
    # X with multiple columns
    # Y = X[:,0] + np.sin(X[:,1]) + X[:,2]**2 + X[:,3]**3

    # create weights -10 to 10
    weights = np.multiply(np.random.rand(X.shape[1]), np.random.randint(1, 10, size=(X.shape[1])))
    
    # add random negativity
    a = np.random.rand(weights.shape[0]) > 0.5
    b = np.ones(weights.shape[0])
    b[a==True] = -1
    weights = weights * b

    Y = np.dot(X, weights)
    Y = Y + np.random.normal(loc=0.0, scale=np.abs((np.mean(Y)/50)), size=Y.shape[0])
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed+100)
    
    # choose n columns randomly
    # cols = np.random.randint(2, 5)
    cols = 2

    # create X all integer 0 to 10
    X = np.multiply(np.random.rand(1000,cols), np.random.randint(1, 10, size=(1000,cols)))


    # create weights -10 to 10
    weights = np.multiply(np.random.rand(X.shape[1]), np.random.randint(1, 5, size=(X.shape[1])))
    
    # add random negativity
    a = np.random.rand(weights.shape[0]) > 0.5
    b = np.ones(weights.shape[0])
    b[a==True] = -1
    weights = weights * b

    # add squared weights 
    sq_weights = np.random.rand(X.shape[1]) / 2

    Y = np.dot(X**3, sq_weights)

    Y = Y + np.random.normal(loc=0.0, scale=np.abs((np.mean(Y)/50)), size=Y.shape[0])
    return X, Y

def author():
    return 'mkazkayasi3' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
