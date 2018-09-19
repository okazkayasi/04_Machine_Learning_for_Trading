"""
import BagLearner as bl
learner = bl.BagLearner(learner = al.ArbitraryLearner, kwargs = {"argument1":1, "argument2":2},\
                        bags = 20, boost = False, verbose = False)
learner.addEvidence(Xtrain, Ytrain)
Y = learner.query(Xtest)
"""
import numpy as np
from RTLearner import RTLearner


class BagLearner:
    
    learner = RTLearner
    kwargs = {}
    bags = 10
    boost = False
    verbose = False
    bag = []
    
    def __init__(self, learner, kwargs, bags, boost=False, verbose=False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose

    def addEvidence(self, Xtrain, Ytrain):

        # get with random replacement
        for i in range(self.bags):
            permed = np.random.randint(0, high=Xtrain.shape[0], size=(Xtrain.shape[0]))
            x = Xtrain[permed, :]
            y = Ytrain[permed]
            learn = self.learner(**self.kwargs)
            self.bag.append(learn)
            self.bag[i].addEvidence(x, y)

    def query(self, Xtest):
        # hold results in 2D array
        hold = np.zeros((self.bags, Xtest.shape[0]))
        for i in range(self.bags):
            pred = self.bag[i].query(Xtest)
            hold[i] = pred

        Ypredict = np.mean(hold, axis=0)
        return Ypredict


    def author(self):
        return 'mkazkayasi3'