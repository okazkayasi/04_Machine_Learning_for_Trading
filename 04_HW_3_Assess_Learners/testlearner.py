"""
Test a learner.  (c) 2015 Tucker Balch
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
"""

"""
Student Name: Mehmet Oguz Kazkayasi (replace with your name)
GT User ID: mkazkayasi3 (replace with your User ID)
GT ID: 903369796 (replace with your GT ID)
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import LinRegLearner as lrl
import DTLearner as dl
import RTLearner as rl
import BagLearner as bl
import InsaneLearner as il

import sys
import os




def rmse(trainX, trainY, testX, testY, learner):
    # create a learner and train it
    # learner = dl.DTLearner(leaf_size=leaf_size, verbose=False)
    # learner = rl.RTLearner(leaf_size=leaf_size, verbose=False)

    learner.addEvidence(trainX, trainY) # train it
    # print learner.author()

    # evaluate in sample
    predY = learner.query(trainX) # get the predictions
    rmse_in_sample = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    # print
    # print "In sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(predY, y=trainY)
    # print "corr: ", c[0,1]

    # evaluate out of sample
    predY = learner.query(testX) # get the predictions
    rmse_out_sample = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    # print
    # print "Out of sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(predY, y=testY)
    # print "corr: ", c[0,1]

    return rmse_in_sample, rmse_out_sample


if __name__=="__main__":
    if len(sys.argv) == 2:
        # print "Usage: python testlearner.py #<filename>"
        # sys.exit(1)
        filename = sys.argv[1]
    else:
        filename = "Istanbul.csv"

    inf = open(os.path.join("./04_HW_3_Assess_Learners/Data/", filename))

    # if it is Istanbul dataset we have tochange the method to read
    data = np.genfromtxt(inf, delimiter=',')
    if filename == 'Istanbul.csv':
        data = data[1:,1:]
        # print "ISTANBUL - ISTANBULLLL!!!!"
    # print filename

    # data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    # compute how much of the data is training and testing
    cutoff = int(data.shape[0]*0.6)  		   	  			    		  		  		    	 		 		   		 		  
    permutation = np.random.permutation(data.shape[0])  	

    train_data = data[permutation[:cutoff],:]	    	 		 		   		 		  
    test_data = data[permutation[cutoff:],:]  	

     
    # separate out training and testing data
    trainX = train_data[:, :-1] 		   	  			    		  		  		    	 		 		   		 		  
    trainY = train_data[:,-1]  	
    testX = test_data[:, :-1]
    testY = test_data[:, -1]

    # print testX.shape
    # print testY.shape
    hold_it = np.zeros((2, trainX.shape[0]-1))



    ## FOR DT Learner Leaf size 1 to all
    for leaf in range(1,trainX.shape[0]):
        learner = dl.DTLearner(leaf_size=leaf, verbose=False)
        in_sample, out_sample = rmse(trainX, trainY, testX, testY, learner)
        hold_it[0, leaf-1] = in_sample
        hold_it[1, leaf-1] = out_sample

    q = np.argmin(hold_it[1, :])
    print 'out sample minimum value: ', np.argmin(hold_it[1, :]), np.min(hold_it[1,:])
    print 'in sample value at min value of out sample: ', hold_it[0, q]

    plt.rcParams["figure.figsize"] = (10,8)    
    fig, ax = plt.subplots()
    ax.plot(range(1, trainX.shape[0]), hold_it[0], label='in-sample')
    ax.plot(range(1, trainX.shape[0]), hold_it[1], label='out-sample')
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.title('Overfitting Comparison Depending on Leaf Size (TD Learning)')
    maks = np.max(hold_it) * 1.1 
    plt.axis([1, trainX.shape[0], 0, maks])
    plt.legend()  
    # plt.show()
    plt.savefig('Overfitting_Comparison_Depending_on_Leaf_Size_Size_All.png')

    # plt.close()


    fig, ax = plt.subplots()
    ax.plot(range(1, 20), hold_it[0, :19], label='in-sample')
    ax.plot(range(1, 20), hold_it[1, :19], label='out-sample')
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.title('Overfitting Comparison Depending on Leaf Size (TD Learning)')
    maks = np.max(hold_it[:, :19]) * 1.1 
    plt.axis([1, 20, 0, maks])
    plt.legend()  
    # plt.rcParams["figure.figsize"] = (10,8)
    plt.savefig('Overfitting_Comparison_Depending_on_Leaf_Size_Size_20.png')



    bags = 90
    diff = 3
    hold_it = np.zeros((2, bags/diff))

    for no_bag in range(1,bags, diff):
        # learner = dl.DTLearner(leaf_size=leaf, verbose=False)

        bag = bl.BagLearner(dl.DTLearner, kwargs = {"leaf_size": 9, "verbose": False}, bags = no_bag, boost=False, verbose=False)
        in_sample, out_sample = rmse(trainX, trainY, testX, testY, bag)
        hold_it[0, ((no_bag/diff))] = in_sample
        hold_it[1, ((no_bag/diff))] = out_sample

    print 'leaf_size 9'
    print hold_it[1, 0]
    print np.mean(hold_it[1, 20:])

    fig, ax = plt.subplots()
    ax.plot(range(1,bags,diff), hold_it[0], label='in-sample')
    ax.plot(range(1,bags,diff), hold_it[1], label='out-sample')
    plt.ylabel('RMSE')
    plt.xlabel('Number of Bags')
    plt.title('Overfitting Comparison Depending on Number of Bags (Leaf_size=9)')
    maks = np.max(hold_it) * 1.1 
    plt.axis([1, bags, 0, maks])
    plt.legend()   
    # plt.show()
    plt.savefig('Overfitting_Comparison_Depending_on_Number_of_Bags_Leaf_Size_9.png')



    # LEAF SIZE 2 bags 30
    bags = 90
    diff = 3
    hold_it = np.zeros((2, bags/diff))

    for no_bag in range(1,bags, diff):
        # learner = dl.DTLearner(leaf_size=leaf, verbose=False)

        bag = bl.BagLearner(dl.DTLearner, kwargs = {"leaf_size": 2, "verbose": False}, bags = no_bag, boost=False, verbose=False)
        in_sample, out_sample = rmse(trainX, trainY, testX, testY, bag)
        hold_it[0, ((no_bag/diff))] = in_sample
        hold_it[1, ((no_bag/diff))] = out_sample

    print 'leaf_size 2'
    print hold_it[1, 0]
    print np.mean(hold_it[1, 20:])


    fig, ax = plt.subplots()
    ax.plot(range(1,bags,diff), hold_it[0], label='in-sample')
    ax.plot(range(1,bags,diff), hold_it[1], label='out-sample')
    plt.ylabel('RMSE')
    plt.xlabel('Number of Bags')
    plt.title('Overfitting Comparison Depending on Number of Bags (Leaf_size=2)')
    maks = np.max(hold_it) * 1.1 
    plt.axis([1, bags, 0, maks])
    plt.legend()  
    # plt.show()
    plt.savefig('Overfitting_Comparison_Depending_on_Number_of_Bags_Leaf_Size_2.png')





    hold_it = np.zeros((2, 50))


    # ## FOR DT Learner Leaf size 1 to all
    for leaf in range(1,51):
        bag = bl.BagLearner(dl.DTLearner, kwargs = {"leaf_size": leaf, "verbose": False}, bags = 20, boost=False, verbose=False)
        in_sample, out_sample = rmse(trainX, trainY, testX, testY, bag)
        hold_it[0, leaf-1] = in_sample
        hold_it[1, leaf-1] = out_sample

    print 'leaf_size 9'
    print hold_it[1, 0]
    print np.mean(hold_it[1, 20:])


    plt.rcParams["figure.figsize"] = (10,8)    

    fig, ax = plt.subplots()

    ax.plot(range(1, 51), hold_it[0, :], label='in-sample')
    ax.plot(range(1, 51), hold_it[1, :], label='out-sample')
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.title('Overfitting Comparison Depending on Leaf Size (TD Learning with Bagging Size 20)')
    maks = np.max(hold_it) * 1.1 
    plt.axis([1, 50, 0, maks])
    plt.legend()  
    # plt.rcParams["figure.figsize"] = (10,8)
    plt.savefig('Bagging_Overfitting_Comparison_Depending_on_Leaf_Size_Size_20.png')









    ### RLLEARNER COMPARISON

    hold_it = np.zeros((2, trainX.shape[0]-1))
    a = np.zeros((2,30))
    for i in range(30):
        for leaf in range(1,trainX.shape[0]):
            learner = rl.RTLearner(leaf_size=leaf, verbose=False)
            in_sample, out_sample = rmse(trainX, trainY, testX, testY, learner)
            hold_it[0, leaf-1] = in_sample
            hold_it[1, leaf-1] = out_sample

        q = np.argmin(hold_it[1, :])
        # print 'random out sample minimum value: ', np.argmin(hold_it[1, :]), np.min(hold_it[1,:])
        # print 'in sample value at min value of out sample: ', hold_it[0, q]
        a[0, i] = q
        a[1, i] = np.min(hold_it[1,:])  
    # print a



    nold_it = np.zeros((2, trainX.shape[0]-1))
    a = np.zeros((2,10))
    for i in range(10):
        for leaf in range(1,trainX.shape[0]):
            learner = rl.RTLearner(leaf_size=12, verbose=False)
            in_sample, out_sample = rmse(trainX, trainY, testX, testY, learner)
            nold_it[0, leaf-1] = in_sample
            nold_it[1, leaf-1] = out_sample

        q = np.argmin(nold_it[1, :])
        # print 'random out sample minimum value: ', np.argmin(hold_it[1, :]), np.ma(hold_it[1,:])
        # print 'in sample value at min value of out sample: ', hold_it[0, q]
        a[0, i] = q
        a[1, i] = np.mean(nold_it[1,:])     
    # print a



    plt.rcParams["figure.figsize"] = (10,8)    
    fig, ax = plt.subplots()
    ax.plot(range(1, trainX.shape[0]), hold_it[0], label='in-sample')
    ax.plot(range(1, trainX.shape[0]), hold_it[1], label='out-sample')
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.title('Overfitting Comparison Depending on Leaf Size (RT Learning)')
    maks = np.max(hold_it) * 1.1 
    plt.axis([1, trainX.shape[0], 0, maks])
    plt.legend()  
    # plt.show()
    plt.savefig('Random_Overfitting_Comparison_Depending_on_Leaf_Size_Size_All.png')

    # plt.close()


    fig, ax = plt.subplots()
    ax.plot(range(1, 20), hold_it[0, :19], label='in-sample')
    ax.plot(range(1, 20), hold_it[1, :19], label='out-sample')
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.title('Overfitting Comparison Depending on Leaf Size (RT Learning)')
    maks = np.max(hold_it[:, :19]) * 1.1 
    plt.axis([1, 20, 0, maks])
    plt.legend()  
    # plt.rcParams["figure.figsize"] = (10,8)
    plt.savefig('Random_Overfitting_Comparison_Depending_on_Leaf_Size_Size_20.png')
    




    ### RANDOM TREE BAGGING

    bags = 90
    diff = 3
    hold_it = np.zeros((2, bags/diff))

    for no_bag in range(1,bags, diff):
        # learner = dl.DTLearner(leaf_size=leaf, verbose=False)

        bag = bl.BagLearner(rl.RTLearner, kwargs = {"leaf_size": 12, "verbose": False}, bags = no_bag, boost=False, verbose=False)
        in_sample, out_sample = rmse(trainX, trainY, testX, testY, bag)
        hold_it[0, ((no_bag/diff))] = in_sample
        hold_it[1, ((no_bag/diff))] = out_sample

    print 'leaf_size 12, best leaf'
    print hold_it[1, 0]
    print np.mean(hold_it[1, 20:])

    fig, ax = plt.subplots()
    ax.plot(range(1,bags,diff), hold_it[0], label='in-sample')
    ax.plot(range(1,bags,diff), hold_it[1], label='out-sample')
    plt.ylabel('RMSE')
    plt.xlabel('Number of Bags')
    plt.title('Random Overfitting Comparison Depending on Number of Bags (Leaf_size=9)')
    maks = np.max(hold_it) * 1.1 
    plt.axis([1, bags, 0, maks])
    plt.legend()  
    # plt.show()
    plt.savefig('Random Overfitting_Comparison_Depending_on_Number_of_Bags_Leaf_Size_9.png')



    # LEAF SIZE 2 bags 30
    bags = 90
    diff = 3
    hold_it = np.zeros((2, bags/diff))

    for no_bag in range(1,bags, diff):
        # learner = dl.DTLearner(leaf_size=leaf, verbose=False)

        bag = bl.BagLearner(rl.RTLearner, kwargs = {"leaf_size": 2, "verbose": False}, bags = no_bag, boost=False, verbose=False)
        in_sample, out_sample = rmse(trainX, trainY, testX, testY, bag)
        hold_it[0, ((no_bag/diff))] = in_sample
        hold_it[1, ((no_bag/diff))] = out_sample

    print 'leaf_size 2'
    print hold_it[1, 0]
    print np.mean(hold_it[1, 20:])


    fig, ax = plt.subplots()
    ax.plot(range(1,bags,diff), hold_it[0], label='in-sample')
    ax.plot(range(1,bags,diff), hold_it[1], label='out-sample')
    plt.ylabel('RMSE')
    plt.xlabel('Number of Bags')
    plt.title('Random Overfitting Comparison Depending on Number of Bags (Leaf_size=2)')
    maks = np.max(hold_it) * 1.1 
    plt.axis([1, bags, 0, maks])
    plt.legend()  
    # plt.show()
    plt.savefig('Random Overfitting_Comparison_Depending_on_Number_of_Bags_Leaf_Size_2.png')


def author(self):
    return 'mkazkayasi3'