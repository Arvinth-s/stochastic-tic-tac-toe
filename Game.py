# OM NAMO NARAYANA

import numpy as np
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

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
    
    def isDraw(self):
        for row in self.board:
            for ele in row:
                if(ele == 0):
                    return False
        return True
    
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
        
        reward = -1 if not self.isTerminalState() else 0

        return self.board, reward, self.isTerminalState(), None
    
    def rollDice(self):
        return random.randint(1, 7)

    def randomSelection(self):
        k = self.rollDice()
        # print(f'dice output: {k}')
        validSquares = self.freeKquares(k)
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
    

def hashState(grid, hashkey = 10**5):
    m, n = grid.shape
    idx = 0
    for i in range(m):
        for j in range(n):
            idx = ( idx * 4 + grid[i][j]) % hashkey
    return idx


def maxAction(Q, grid, possibleActions, m, n, player = 2):
    max_action = possibleActions[0]
    for action in possibleActions:

        x = int (action // n)
        y = int (action % n)
        buf = grid[x][y]
        if(grid[x][y] != 0):
            raise Exception(f"Invalid square {x}, {y}")
        grid[x][y] = player
        state_ = hashState(grid)
        grid[x][y] = buf
        if(Q[state_, action] > Q[state_, max_action]):
            max_action = action
    return  max_action


if __name__ == "__main__":
    done = 0
    
    m = 3
    n = 3

    ALPHA = 0.1
    GAMMA = 1.0
    EPS = 1.0

    

    game = Game(m, n)

    Q = {}
    for state in range(game.stateSpaceSize):
        for action in range(game.actionSpaceSize):
            Q[state, action] = 0

    numGames = 50000
    num_wins = 0
    num_draws = 0
    totalRewards = np.zeros(numGames)
    wins = []
    for game_no in tqdm(range(numGames)):
        turn = 2
        done = 0
        epRewards = 0
        state = game.reset()

        while(done==0):
            turn = turn % 2 + 1
            # print(f'Player {turn} turn')
            # choice = int(input("[1]: normal mode [2]: neutral mode \n"))
            choice = 1
            # while(choice not in [1, 2]):
            #     print("invalid choice")
            #     choice = int(input("[1]: normal mode [2]: neutral mode \n"))

            validSquares = game.randomSelection()
            # game.render(validSquares)
            if(choice == 2):
                index = int( input("Select index of valid square: ") )
                x = int(index / n)
                y = index%n
                state, reward, done, _ = game.step([x, y], turn, validSquares)
                # game.render(validSquares)
                if(done>0):
                    if(done==3):
                        print(f'Match draw!')
                    else:
                        print(f'Player {done} wins!')
            else:
                if(turn % 2 == 1):
                    # action = int( input("Select index of valid square: ") )
                    action = game.actionSpaceSample(validSquares)
                    state, reward, done, _ = game.step([int(action/n), action%n], turn, validSquares)
                    if(done > 0):
                        # game.render(validSquares)
                        if(done == 3):
                            # print(f'Match draw!')
                            None
                        else:
                            # print(f'Player {done} wins!')
                            None
                        if(done==2):
                            num_wins+=1
                        num_draws += (done==3)
                        # print('\n\n\n')
                else:
                    rand = np.random.random()
                    action = maxAction(Q, state, validSquares, m, n) if rand < (1-EPS) \
                                                            else game.actionSpaceSample(validSquares)
                    state_, reward, done, info = game.step([int(action/n), action%n], turn, validSquares)
                    epRewards += reward

                    try:
                        action_ = maxAction(Q, state_, validSquares, m, n)

                        state_hash = hashState(state)
                        state_hash_ = hashState(state_)
                        Q[state_hash,action] = Q[state_hash,action] + ALPHA*(reward + \
                                    GAMMA*Q[state_hash_, action_] - Q[state_hash, action])
                        state = state_
                    except:
                        state_hash = hashState(state)
                        Q[state_hash,action] = Q[state_hash, action] + ALPHA*(reward + \
                                    GAMMA*  0 - Q[state_hash, action])

                    if(done > 0):
                        # game.render(validSquares)
                        if(done == 3):
                            # print(f'Match draw!')
                            None
                        else:
                            # print(f'Player {done} wins!')
                            None
                        num_wins += (done==2)
                        num_draws += (done==3)
                        # print('\n\n\n')
        if(game_no % 500 == 0):
            wins.append(num_wins)
            # print(f'game number {game_no}  win rate {float(num_wins +1) // float(game_no + 1)} wins {num_wins} draws {num_draws}')

        if EPS - 2 / numGames > 0:
            EPS -= 2 / numGames
        else:
            EPS = 0
        totalRewards[game_no] = epRewards
print(wins)
plt.plot(range(len(wins)), wins)
plt.show()

plt.scatter(range(len(totalRewards)), totalRewards)
plt.show()
        
