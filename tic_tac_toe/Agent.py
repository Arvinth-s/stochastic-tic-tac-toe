# OM NAMO NARAYANA

import numpy as np
import random

def hashState(grid, hashkey = 10**5):
    m, n = grid.shape
    idx = 0
    for i in range(m):
        for j in range(n):
            idx = ( idx * 4 + grid[i][j]) % hashkey
    return idx

class Agent(object):
    def __init__(self, alpha, gamma, eps, eps_decay=0., m=3, n=3):
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay
        self.Q = {}
        self.hashkey = 10**5
        self.stateSpaceSize = self.hashkey 
        self.actionSpaceSize = m * n

        for i in range(self.actionSpaceSize):
            for j in range(self.stateSpaceSize):
                self.Q[i, j] = 0


        self.rewards = []

    def maxAction(self, Q, state, possibleActions, player = 2):
        m, n = state.shape
        max_action = possibleActions[0]
        for action in possibleActions:

            x = int (action // n)
            y = int (action % n)
            buf = state[x][y]
            if(state[x][y] != 0):
                raise Exception(f"Invalid square {x}, {y}")
            state[x][y] = player
            state_hash = hashState(state)
            state[x][y] = buf
            if(Q[action, state_hash] > Q[max_action, state_hash]):
                max_action = action
        return  max_action

    def randomAction(self, validActions):
        return random.choice(validActions)
    
    def getAction(self, state, validActions):
        rand = np.random.random()
        action = self.maxAction(self.Q, state, validActions) if rand < (1-self.eps) \
                                                else self.randomAction(validActions)
        return action
        
    def update(self, state, new_state, action, reward):
        m, n = state.shape
        state_hash = hashState(state)
        if new_state is not None:
            new_state_hash = hashState(new_state)
            possible_actions = []
            for i in range(m):
                for j in range(n):
                    if(new_state[i][j] == 0):
                        possible_actions.append(i*n+j)

            Q_options = [self.Q[a, new_state_hash] for a in possible_actions]

            self.Q[action, state_hash] += self.alpha*(reward + self.gamma*max(Q_options) - self.Q[action, state_hash])
        else:
            self.Q[action, state_hash] += self.alpha*(reward - self.Q[action, state_hash])

        self.rewards.append(reward)

        self.eps = max(0, self.eps - self.eps_decay / len(self.rewards) )

