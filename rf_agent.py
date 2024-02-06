from collections import defaultdict
from State import State
from SnakeGame import SnakeGame
import random
import json
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.exceptions import NotFittedError
import numpy as np
from Direction import Direction
import pickle



class RandomForestAgent:
    def __init__(self, alpha, epsilon, discount):
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount
        self.rf_model = RandomForestRegressor(100)

    def get_values(self, state: State):
        try:
            return self.rf_model.predict([state.state])[0]
        except NotFittedError:
            return [0]*4
    
    def get_value_for_action(self, state: State, action: Direction):
        return self.get_values(state)[action.value]
    
    def get_value(self, state: State):
        return max(self.get_values(state))
    
    def set_value(self, state: State, action: Direction, new_val):
        y = self.get_values(state)
        y[action.value] = new_val
        self.rf_model = self.rf_model.fit([state.state], [y])

    def update(self, state: State, action, reward, next_state):
        gamma = self.discount
        learning_rate = self.alpha

        # if state.state == (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0):
        #     print(self.get_values(state))
        #     print(state)
        #     print(action)
    
        new_val = (1 - learning_rate) * self.get_value_for_action(state, action) + learning_rate*(reward+gamma*self.get_value(next_state))
        # if reward > 0:
        #     print('\n\n', '='*50)
        #     print("Before:", self.get_values(state))
        self.set_value(state, action, new_val)
        # if reward > 0:
        #     print("Action:", action.value)
        #     print("Reward:", reward)
        #     print("Map\n", state)
        #     print("State:", state.state)
        #     print("After:", self.get_values(state))

    def get_best_action(self, state: State):
        possible_actions = state.get_possible_actions()

        if len(possible_actions) == 0:
            return None

        best_actions = []
        best_value = float('-inf')
        for action in possible_actions:
            val = self.get_value_for_action(state, action)
            
            if val > best_value:
                best_actions = []
                best_value = val
                best_actions.append(action)
            elif val == best_value:
                best_actions.append(action)

        print(self.get_values(state))

        return random.choice(best_actions)

    def get_action(self, state: State):
        possible_actions = state.get_possible_actions()

        if len(possible_actions) == 0:
            return None

        epsilon = self.epsilon
        r = random.random()

        if r < epsilon:
            return random.choice(possible_actions)
        

        return self.get_best_action(state)

    def turn_off_learning(self):
        self.epsilon = 0
        self.alpha = 0
    
    def save_model(self):
        with open('random_forest_model.pkl', 'wb') as model_file:
            pickle.dump(self.rf_model, model_file)
    
    def load_model(self):
        with open('random_forest_model.pkl', 'rb') as model_file:
            self.rf_model = pickle.load(model_file)


def play_and_train(env: SnakeGame, agent: RandomForestAgent, train):
    total_reward = 0.0
    done = False
    env.reset()
    state = env.get_state()

    moves_without_reward = 0
    
    while not done:
        action = agent.get_action(state)
        env.step(action)

        next_state = env.get_state()
        reward = next_state.get_value() - state.get_value()
        done = next_state.is_terminal

        if done:
            if not next_state.is_win:
                reward = -10

        if not train:
            env.display()
        else:
            if reward == 0:
                moves_without_reward += 1
            if moves_without_reward > abs(state.get_value() + 1):
                reward = -5
                done = True

            agent.update(state, action, reward, next_state)
            

        state = next_state
        total_reward += reward
        if done:
            break

    return total_reward



if __name__ == '__main__':
    train = False

    if train:
        env = SnakeGame(simulation_mode=True)
        agent = RandomForestAgent(alpha=0.5, epsilon=0.30, discount=0.99)
        episodes = 1000000
    else:
        env = SnakeGame(simulation_mode=False)
        agent = RandomForestAgent(alpha=0.5, epsilon=0, discount=0.99)
        episodes = 1

    agent.load_model()

    max_score = float('-inf')
    for i in range(1, episodes+1):
        total_reward = play_and_train(env, agent, train)

        if total_reward > max_score:
            print("New high score:", total_reward)
            max_score = total_reward

        if i % 100 == 0:
            print(f"Episode: {i} saving model...")
            agent.save_model()

         
