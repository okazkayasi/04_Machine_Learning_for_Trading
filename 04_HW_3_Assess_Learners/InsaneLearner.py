"""
import InsaneLearner as it
learner = it.InsaneLearner(verbose = False) # constructor
learner.addEvidence(Xtrain, Ytrain) # training step
Y = learner.query(Xtest) # query
"""

import BagLearner as bl
import LinRegLearner as lrl
import numpy as np 
class InsaneLearner:
    ins_bags = []

    def __init__(self, verbose=False):
        self.ins_bags = []
    
    def addEvidence(self, Xtrain, Ytrain):
        for i in range(20):
            self.ins_bags.append(bl.BagLearner(learner = lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False))
            self.ins_bags[i].addEvidence(Xtrain, Ytrain)     
    
    def query(self, Xtest):
        hold = np.zeros((20, Xtest.shape[0]))
        for i in range(20):
            hold[i] = self.ins_bags[i].query(Xtest)
        return np.mean(hold, axis=0)


    def author(self):
        return 'mkazkayasi3'