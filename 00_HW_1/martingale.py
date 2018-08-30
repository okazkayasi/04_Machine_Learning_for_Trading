"""Assess a betting strategy.

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

Student Name: Mehmet Oguz Kazkayasi (replace with your name)
GT User ID: mkazkayasi3 (replace with your User ID)
GT ID: 903369796 (replace with your GT ID)
""" 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def author():
    return 'mkazkayasi3' # replace tb34 with your Georgia Tech username.

def gtid():
    return 903369796 # replace with your GT ID number

def get_spin_result(win_prob):
    result = False
    if np.random.random() <= win_prob: 
        result = True
    return result
 
def test_code():
    win_prob = 18./38 # set appropriately to the probability of a win
    np.random.seed(gtid()) # do this only once
 
    exp1fig1(win_prob)
    res1 = exp1fig2(win_prob)
    exp1fig3(win_prob, res1)

    res2 = exp2fig1(win_prob)
    exp2fig2(win_prob, res2)

def exp1fig1(win_prob):
    results = np.zeros((10, 1001), dtype = int)

    for i in range(10):
        result = thousand_exp(win_prob)
        results[i][:] = result

    # fig, ax = plt.subplots (2, 5)
    # for i in range(1):
    #     for j in range(5):
    #         num = i*5 + j
    #         ax[i][j].plot(results(num))
    # plt.show()
    plt.figure(1)
    plt.figure(figsize=(8, 10))

    for i in range(2):
        for j in range(5):
            num = i*5 + j + 1
            plt.subplot(5, 2, num)
            plt.plot(results[num-1])
            plt.ylabel('episode_winning')
            plt.xlabel('number_of_episode')
            plt.axis([0, 300, -256, 100])
    plt.savefig("experiment1_figure1.png", dpi = 100)
    plt.cla()
    plt.clf()
    plt.figure(figsize=(10., 5.))
    # plt.close()


def exp1fig2(win_prob):
    results = np.zeros((1000, 1001), dtype = int)

    for i in range(1000):
        result = thousand_exp(win_prob)
        results[i][:] = result    

    mean = np.mean(results, axis=0)
    std = np.std(results, axis=0)
    mean_plus_std = mean + std
    mean_minus_std = mean - std
    
    plt.plot(mean)
    plt.plot(mean_minus_std)
    plt.plot(mean_plus_std)
    plt.legend(['mean', 'mean-std', 'mean+std'])
    plt.ylabel('mean_of_episode_winnings')
    plt.xlabel('number_of_episode')
    plt.axis([0, 300, -256, 100])
    plt.savefig("experiment1_figure2.png", dpi = 100)
    plt.cla()
    plt.clf()
    return results

def exp1fig3(win_prob, res1):
    results = res1
    # results = np.zeros((1000, 1001), dtype = int)

    # for i in range(1000):
    #     resures1
    #     results[i][:] = result    

    median = np.median(results, axis=0)
    std = np.std(results, axis=0)
    median_plus_std = median + std
    median_minus_std = median - std
    
    plt.plot(median)
    plt.plot(median_minus_std)
    plt.plot(median_plus_std)
    plt.legend(['median', 'median-std', 'median+std'])
    plt.ylabel('median_of_episode_winnings')
    plt.xlabel('number_of_episode')
    plt.axis([0, 300, -256, 100])
    plt.savefig("experiment1_figure3.png", dpi = 100)
    plt.cla()
    plt.clf()



def exp2fig1(win_prob):
    results = np.zeros((1000, 1001), dtype = int)

    for i in range(1000):
        result = thousand_exp(win_prob, money=256)
        results[i][:] = result    

    mean = np.mean(results, axis=0)
    std = np.std(results, axis=0)
    mean_plus_std = mean + std
    mean_minus_std = mean - std
    
    plt.plot(mean)
    plt.plot(mean_minus_std)
    plt.plot(mean_plus_std)
    plt.legend(['mean', 'mean-std', 'mean+std'])
    plt.ylabel('mean_of_episode_winnings')
    plt.xlabel('number_of_episode')
    plt.axis([0, 1000, -256, 100])

    plt.savefig("experiment2_figure1.png", dpi = 100)
    plt.cla()
    plt.clf()
    return results


def exp2fig2(win_prob, res2):
    
    results = res2
    # results = np.zeros((1000, 1001), dtype = int)

    # for i in range(1000):
    #     result = thousand_exp(win_prob, money=256)
    #     results[i][:] = result    

    median = np.median(results, axis=0)
    std = np.std(results, axis=0)
    median_plus_std = median + std
    median_minus_std = median - std
    
    plt.plot(median)
    plt.plot(median_minus_std)
    plt.plot(median_plus_std)
    plt.legend(['median', 'median-std', 'median+std'])
    plt.ylabel('median_of_episode_winnings')
    plt.xlabel('number_of_episode')
    plt.axis([0, 1000, -256, 100])
    plt.savefig("experiment2_figure2.png", dpi = 100)
    plt.cla()
    plt.clf()





def thousand_exp(win_prob, money=np.inf):

    episode_winning = 0
    winnings = np.zeros(1001, dtype=int)
    i = 0
    while i < 1000:
        bet_amount = 1
        won = False
        
        while not won:
            i += 1


            if money <= 0:
                winnings[i] = episode_winning
                won = True

            else:

                if money >= bet_amount:
                    bet_amount = bet_amount
                elif money < bet_amount and money > 0:
                    bet_amount = money

                if episode_winning >= 80:
                    winnings[i] = episode_winning
                    won = True
                else:
                    won = get_spin_result(win_prob) # test the roulette spin
                    if won:
                        episode_winning += bet_amount
                        money += bet_amount
                    else:
                        episode_winning -= bet_amount
                        money -= bet_amount
                        bet_amount *= 2
                winnings[i] = episode_winning
                if i == 1000:
                    won = True


    return winnings
    # add your code here to implement the experiment  



if __name__ == "__main__":
    test_code()
