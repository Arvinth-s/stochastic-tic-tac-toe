# OM NAMO NARAYANA

import numpy as np
import random

class Game(object):
    def __init__(self, m, n, params=None):
        self.board = np.zeros((m, n), dtype=np.int8)
        self.m = m
        self.n = n
        if(params and params.blocked):
            for cell in params.blocked:
                self.board[cell[0], cell[1]] = -1
        state_hash_key = 10**5 + 7
        self.stateSpaceSize = state_hash_key
        self.actionSpaceSize = self.m * self.n


    def isTerminalState(self):
        for i in range(self.m):
            row = self.board[i, :].tolist()
            if(row.count(1) + row.count(-1) == self.n ):
                return 1
            if(row.count(2) + row.count(-1) == self.n):
                return 2
        for j in range(self.n):
            col = self.board[:, j].tolist()
            if(col.count(1) + col.count(-1) == self.m):
                return 1 
            if(col.count(2) + col.count(-1) == self.m):
                return 2
        diagn = min(self.m, self.n)
        diag = [self.board[i][i] for i in range(diagn)]

        if(diag.count(1) + diag.count(-1) == diagn):
            return 1
        if(diag.count(2) + diag.count(-1) == diagn):
            return 2

        diag = [self.board[diagn-1-i][i] for i in range(diagn)]
        if(diag.count(1) + diag.count(-1) == diagn):
            return 1
        if(diag.count(2) + diag.count(-1) == diagn):
            return 2
    
        draw = True
        for row in self.board:
            for ele in row:
                if(ele == 0):
                    draw = False
                    break
        if(draw): return 3


        return 0
    
    
    def freeKquares(self, k=-1):
        indices = []
        if(k==-1):k = self.m * self.n
        for i in range(self.m):
            for j in range(self.n):
                if(self.board[i][j] == 0):
                    indices.append(i*self.n+j)
        random.shuffle(indices)
        return indices[:k]
            
    def setState(self, state, player=1):
        x = int (state // self.n )
        y = state % self.n

        assert(state < self.m * self.n and state >= 0)

        if(self.board[x][y] != 0):
            raise Exception("The box is already taken")
        
        self.board[x][y] = player
        return 
    
    def validSquare(self, action):
        if(action < 0 or action >= self.m * self.n):
            return False
        return True
    
    def step(self, action, player, validPositions):
        
        x = action[0]
        y = action[1] 

        if(x*self.n + y not in validPositions):
            raise Exception(f"Not a valid action {x, y} validPositions {validPositions}")

        self.setState(x*self.n + y, player)

        validPositions.remove(x*self.n + y)

        if(player > 3):
            raise Exception("Player can't be greater than 3.")

        if(player == 3):
            x = action[2]
            y = action[3]
            if(x*self.n + y not in validPositions):
                raise Exception("Not a valid action")

            self.setState(x*self.n + y, player)
        
        reward = -1 if not self.isTerminalState() else 1

        return self.board, reward, self.isTerminalState(), None
    
    def rollDice(self):
        return random.randint(1, 7)

    def randomSelection(self):
        k = self.rollDice()
        # print(f'dice output: {k}')
        validSquares = self.freeKquares()
        return validSquares

    def render(self, validSquares):
        print('------------------------------------------')
        items = ['-', 'X', 'O', 'T']
        for i in range(self.m):
            for j in range(self.n):
                ele = self.board[i][j]
                if(ele > 3):
                    raise Exception("Player index can't be greater than 3")
                if(i*self.m + j in validSquares):
                    print(f'{i*self.m+j}', end='\t')
                else:
                    print(items[ele], end='\t')
            print('\n')
        print('------------------------------------------')
        return

    def actionSpaceSample(self, validActions):
        action = random.choice(validActions)
        return action
    
    def reset(self):
        self.board = np.zeros((self.m, self.n), dtype=np.int8)
        return self.board
    






