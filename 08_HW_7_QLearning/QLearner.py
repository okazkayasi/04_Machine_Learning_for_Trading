"""
Template for implementing QLearner  (c) 2015 Tucker Balch

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
import random as rand
from copy import deepcopy

class QLearner(object):

    def author(self):
        return 'mkazkayasi3' # replace tb34 with your Georgia Tech username.

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.s = 0
        self.a = 0
        self.qtable = np.zeros(shape=(num_states, num_actions), dtype='float')
        self.alpha = alpha
        self.gamma = gamma
        self.rand_rate = rar
        self.rand_decay = radr
        self.dyna = dyna
        self.verbose = verbose

        self.Tc = 0.00001 * np.ones(shape=(num_states, num_actions, num_states), dtype='float')

        self.T = np.zeros(shape=(num_states, num_actions, num_states), dtype='float')
        self.R = np.zeros(shape=(num_states, num_actions))

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """

        # choose random if below
        if np.random.rand() < self.rand_rate:
                action = rand.randint(0, self.num_actions-1)
        # exploit if above
        else:
            action = np.argmax(self.qtable[s, :])    
        
        self.s = s
        self.a = action
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The new state
        @returns: The selected action
        """
        old = self.s
        new = s_prime
        old_action = self.a
        # update Q(s,a)
        self.qtable[self.s, self.a] = (1-self.alpha) * self.qtable[self.s,self.a] + self.alpha * (r + self.gamma * self.qtable[s_prime, self.qtable[s_prime, :].argmax()])

        action = self.querysetstate(s_prime)
 
        self.rand_rate *= self.rand_decay
 
        if self.dyna > 0:
            self.Tc[old][old_action][new] = self.Tc[old][old_action][new] + 1


            total = 0
            for i in range(self.num_states):
                total += self.Tc[old][old_action][i] 
            for i in range(self.num_states):
                self.T[old][old_action][i] = self.Tc[old][old_action][i] / total

            # self.T[:, :, -1] = np.sum(self.Tc, axis=2)
            # self.T[:, :, :-1] = self.Tc /  self.T[:, :, -1]

            self.R[old][old_action] = (1 - self.alpha) * self.R[old][old_action] + self.alpha * r
    
            for i in range(self.dyna):

                rand_s = np.random.randint(0, self.num_states)
                rand_a = np.random.randint(0, self.num_actions)

                s1 = np.argmax(self.T[rand_s, rand_a, :])
                r1 = self.R[rand_s, rand_a]

                self.qtable[rand_s, rand_a] = (1-self.alpha) * self.qtable[rand_s, rand_a] + self.alpha * (r1 + self.gamma * self.qtable[s1, self.qtable[s1,:].argmax()])



        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"