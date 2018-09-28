# mainly working on istanbul.csv
# data includes the returns of multiple worldwide indexes
# Overall objective is to predict what the return for 
# the MSCI Emerging Markets (EM) index will be #
# on the basis of the other index returns. 

# the first column is date, which you should ignore
# auto-grader tests with 60% random train data and 40% test


# We define "best feature to split on" as the feature that has the highest absolute
# value correlation with Y

"""
import DTLearner as dt
learner = dt.DTLearner(leaf_size = 1, verbose = False) # constructor
learner.addEvidence(Xtrain, Ytrain) # training step
Y = learner.query(Xtest) # query
"""

"""
Student Name: Mehmet Oguz Kazkayasi (replace with your name)
GT User ID: mkazkayasi3 (replace with your User ID)
GT ID: 903369796 (replace with your GT ID)
"""
import numpy as np


class DTLearner:
    
    leaf_size = 1
    decision_tree = np.zeros((2,5), dtype=np.float)

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.decision_tree = np.zeros((2,5), dtype=np.float)

    def addEvidence(self, Xtrain, Ytrain):
        Xtrain = np.asarray(Xtrain, dtype=np.float)
        Ytrain = np.asarray(Ytrain, dtype=np.float)
        self.decision_tree = self.build_tree(Xtrain, Ytrain)

    def query(self, Xtest):
        Ypredict = np.zeros(Xtest.shape[0], dtype = np.float)
        node = 0
        for i in range(Xtest.shape[0]):
            # check root
            Ypredict[i] = self.checkTree(Xtest[i], node)

        return Ypredict


    def checkTree(self, xs, node):
        # if it is a leaf return the value
        LEAF = -1
        if self.decision_tree[node, 0] == LEAF:
            return self.decision_tree[node, 1]
        
        # if value is smaller than split val
        factor = int(self.decision_tree[node, 0])
        value = xs[factor]
        left_node = int(self.decision_tree[node, 2])
        right_node = int(self.decision_tree[node, 3])
        if value <= self.decision_tree[node, 1]:
            return self.checkTree(xs, left_node)
        
        # else
        return self.checkTree(xs, right_node) 

    def build_tree(self, Xtrain, Ytrain, node = 0):
        LEAF = -1
        NA = -2
        
        # if less than leaf size 
        if Xtrain.shape[0] <= self.leaf_size:
            return np.array([LEAF, sum(Ytrain)/float(len(Ytrain)), NA, NA])
        if np.unique(Ytrain).shape[0] == 1:
            return np.array([LEAF, Ytrain[0], NA, NA])
        
        # get best correlation
        split_ind = self.get_best_corr(Xtrain, Ytrain)
        if split_ind == None:
            print 'iiiiiiiii'

        # the split value
        split_val = np.median(Xtrain[:, split_ind])

        # left tree
        left_x = Xtrain[Xtrain[:, split_ind] <= split_val]
        left_y = Ytrain[Xtrain[:, split_ind] <= split_val]
        left_node = node + 1

        # if left tree is all the tree or none
        if left_x.shape[0] == Xtrain.shape[0] or left_x.shape[0] == 0:
            return np.array([LEAF, sum(Ytrain)/float(len(Ytrain)), NA, NA])


        left_tree = self.build_tree(left_x, left_y, left_node)

        # right tree
        right_x = Xtrain[Xtrain[:, split_ind] > split_val]
        right_y = Ytrain[Xtrain[:, split_ind] > split_val]
        right_node = 0
        if len(left_tree.shape) > 1:
            right_node = node + left_tree.shape[0] + 1
        else:
            right_node = node + 1 + 1
        right_tree = self.build_tree(right_x, right_y, right_node)

        # add root
        root = np.array([split_ind, split_val, left_node, right_node], dtype=np.float)
        
        # combine all
        tree = np.vstack((root, left_tree, right_tree))
        return tree 

    def get_best_corr(self, Xtrain, Ytrain):
        x = np.transpose(Xtrain)
        y = np.transpose(Ytrain)
        mat = np.corrcoef(x, y)
        mat = np.abs(mat[-1])

        a = np.isnan(mat[:-1])
        if a[a == False].shape[0] == 0:  
            return 0    
        return np.nanargmax(mat[:-1])

    def author(self):
        return 'mkazkayasi3'


