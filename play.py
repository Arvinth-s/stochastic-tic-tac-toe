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

    alpha = 0.5
    gamma = 1.0
    eps = 0.3
    eps_decay = 0.0
    

    game = Game.Game(m, n)

        
    numGames = 2000
    num_wins = [0, 0, 0]
    totalRewards = np.zeros(numGames)
    wins = []
    steps = []

    agent_bot = Agent.Agent(alpha, gamma, eps, eps_decay, m, n)

    for game_no in tqdm(range(numGames)):
        turn = 2
        done = 0
        epRewards = 0
        state = copy.deepcopy(game.reset())
        step = 0
        while(done==0):
            step += 1
            turn = turn % 2 + 1
            validActions = game.randomSelection()
            # game.render(validActions)
            
            if(turn % 2 == 1):
                # '''action = int( input("Select index of valid square: ") )'''
                # action = game.actionSpaceSample(validActions)
                # state, reward, done, _ = game.step([int(action/n), action%n], turn, validActions)
                # state = copy.deepcopy(state)
                # if(done > 0): break
                None

            else:
                action = agent_bot.getAction(state, validActions)
            
                new_state, reward, done, info = game.step([int(action/n), action%n], turn, validActions)
                if(done > 0): break
                
                new_state = copy.deepcopy(new_state)
                epRewards += reward

                agent_bot.update(state, new_state, action, reward)
                state = copy.deepcopy(new_state)

        if(done == 1): 
            reward = -1 
            print(f'player 1 wins!')
        elif(done == 2): reward = 1
        agent_bot.update(state, None, action, reward)
        epRewards += reward
        num_wins[done-1] += 1
        if(game_no % 500 == 0): wins.append(num_wins[1])

        totalRewards[game_no] = epRewards
        steps.append(step)

print('\n\n\n\n\n Interactive playground:')

x = 'y'                         
while(x != 'n'):
    state = copy.deepcopy(game.reset())                    
    done = 0
    turn = 2
    while(done==0):
        step += 1
        validActions = game.randomSelection()
        game.render(validActions)
        

        action = int(input('select the required action (any of the numbers shown): '))
    
        new_state, reward, done, info = game.step([int(action/n), action%n], turn, validActions)
        if(done > 0): break
        
        new_state = copy.deepcopy(new_state)
        epRewards += reward

        agent_bot.update(state, new_state, action, reward)
        state = copy.deepcopy(new_state)

        print('************************   q value: ', agent_bot.Q[action, Agent.hashState(grid=state)])
    x = input('Want to continue? [y] yes [n] no')

print(f'unique states visited {len(agent_bot.unique_states)}')
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(range(len(wins)), wins)
axs[0, 0].set_title('Wins')
axs[0, 1].scatter(range(len(totalRewards)), totalRewards, s=0.1)
axs[0, 1].set_title('Rewards')
axs[1, 1].scatter(range(len(steps)), steps, s=0.1)
axs[1, 1].set_title('Steps')
# axs[1, 1].plot(x, -y, 'tab:red')
# axs[1, 1].set_title('Axis [1, 1]')

plt.show()