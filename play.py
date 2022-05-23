# OM NAMO NARAYANA

import tic_tac_toe.Game as Game
import tic_tac_toe.Agent as Agent

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import copy


def printResult(done):
    if(done > 0):
        if(done == 3):
            print(f'Match draw!')
        else:
            print(f'Player {done} wins!')

        if(done==2):
            num_wins+=1
        num_draws += (done==3)
        print('\n\n\n')


if __name__ == "__main__":
    done = 0
    
    m = 3
    n = 3

    alpha = 0.1
    gamma = 1.0
    eps = 1.0

    

    game = Game.Game(m, n)

        
    numGames = 50000
    num_wins = [0, 0, 0]
    totalRewards = np.zeros(numGames)
    wins = []

    agent_bot = Agent.Agent(alpha, gamma, eps, 0.01, m, n)


    for game_no in tqdm(range(numGames)):
        turn = 2
        done = 0
        epRewards = 0
        state = copy.deepcopy(game.reset())

        while(done==0):
            turn = turn % 2 + 1
            validActions = game.randomSelection()
            # game.render(validActions)
            
            if(turn % 2 == 1):
                # action = int( input("Select index of valid square: ") )
                action = game.actionSpaceSample(validActions)
                state, reward, done, _ = game.step([int(action/n), action%n], turn, validActions)
                state = copy.deepcopy(state)
                if(done > 0):
                    num_wins[done-1] += 1

            else:
                action = agent_bot.getAction(state, validActions)
            
                new_state, reward, done, info = game.step([int(action/n), action%n], turn, validActions)
                new_state = copy.deepcopy(new_state)
                epRewards += reward

                agent_bot.update(state, new_state, action, reward)
                state = copy.deepcopy(new_state)


                if(done > 0):
                    num_wins[done-1] += 1
                
        if(game_no % 500 == 0):
            wins.append(num_wins[1])

        totalRewards[game_no] = epRewards
print(wins)
plt.plot(range(len(wins)), wins)
plt.show()

plt.scatter(range(len(totalRewards)), totalRewards)
plt.show()