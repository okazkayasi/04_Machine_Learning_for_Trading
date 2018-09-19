import pytest
import util

import os
import sys
import traceback as tb

import numpy as np
import pandas as pd
from collections import namedtuple

import math

import string

import time

import random
from DTLearner import DTLearner
from RTLearner import RTLearner
from BagLearner import BagLearner


def get_learner_data_file(basefilename):
    return open(os.path.join(os.environ.get("LEARNER_DATA_DIR",'04_HW_3_Assess_Learners/Data/'),basefilename),'r')




LearningTestCase = namedtuple('LearningTestCase', ['description', 'group', 'datafile', 'seed', 'outputs'])
learning_test_cases = [
    ########################
    # DTLearner test cases #
    ########################
    LearningTestCase(
        description="Test Case 01: Deterministic Tree",
        group='DTLearner',
        datafile='Istanbul.csv',
        seed=1481090001,
        outputs=dict(
            insample_corr_min=0.95,
            outsample_corr_min=0.15,
            insample_corr_max=0.95
            )
        )]

datafile ='Istanbul.csv'
seed = 1481090001

with get_learner_data_file(datafile) as f:
    alldata = np.genfromtxt(f,delimiter=',')
    if datafile == 'Istanbul.csv':
        alldata = alldata[1:,1:]
    datasize = alldata.shape[0]
    # cutoff = int(datasize*0.6)
    # permutation = np.random.permutation(alldata.shape[0])
    # col_permutation = np.random.permutation(alldata.shape[1]-1)
    # train_data = alldata[permutation[:cutoff],:]
    # trainX = train_data[:,:-1]
    train_data = alldata
    trainX = train_data[:,:-1]
    trainY = train_data[:,-1]
    # testX = test_data[:,:-1]
    testX = trainX
    testY = testX


tmp_numpy_seed = np.random.seed
tmp_random_seed = random.seed
clss_name = DTLearner
np.random.seed(seed)
random.seed(seed)
learner = clss_name(leaf_size=1,verbose=False)
learner.add_evidence(trainX,trainY)
insample = learner.query(trainX)
outsample = learner.query(testX)
np.random.seed = tmp_numpy_seed
random.seed = tmp_random_seed


def fake_seed(*args):
    pass
def fake_rseed(*args):
    pass