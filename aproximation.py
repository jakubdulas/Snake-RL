import random
from typing import Any
import numpy as np
from Direction import Direction
from State import State
from SnakeGame import SnakeGame
from constants import GRID_SIZE
import os
import json


class Agent:
    def __init__(self, features_in, features_out, lr=0, gamma=0, epsilon=0, weights_file="weights.json") -> None:
        self.weights_file = weights_file
        self.load_weights(features_in, features_out)
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.all_actions = list(Direction)

    def __call__(self, state: State):
        features = state.get_features()
        return np.dot(np.array(features), self.weights.T)
    
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum(axis=0, keepdims=True)
    
    def update(self, state: State, action: Direction, reward: float, next_state: State, is_terminal=False) -> None:
        if reward > 1:
            print('asdasd')

        if not is_terminal:
            delta = (reward+self.gamma*max(self(next_state))) - self(state)[action.value]
        else:
            delta = reward - self(state)[action.value]

        self.weights[action.value, :] += self.lr*delta*np.array(state.get_features())
    
    def get_action(self, state: State):
        possible_actions = state.get_possible_actions()
        r = random.random()
        if r < self.epsilon:
            return random.choice(possible_actions)
        return self.get_best_action(state)
    
    def get_best_action(self, state: State):
        possible_actions = state.get_possible_actions()
        values = self(state)
        action_value = [(action, values[action.value]) for action in possible_actions]
        action_value = sorted(action_value, reverse=True, key=lambda x: x[1])
        return action_value[0][0]

    def save_weights(self):
        with open(self.weights_file, 'w+') as f:
            json.dump({"w": self.weights.tolist()}, f)

    def load_weights(self, features_in, features_out):
        if os.path.exists(self.weights_file):
            print("loaded weights")
            with open(self.weights_file, 'r') as f:
                self.weights = np.array(json.load(f)["w"])
        else:
            self.weights = np.random.uniform(-0.1, 0.1, (features_out, features_in))


def play_and_train(env: SnakeGame, agent: Agent, train):
    total_reward = 0.0
    done = False
    env.reset()
    state = env.get_state()
    moves_without_reward = 0

    while not done:
        if train:
            action = agent.get_action(state)
        else:
            action = agent.get_best_action(state)
        env.step(action)

        next_state = env.get_state()
        reward = 0

        if next_state.get_value() - state.get_value() > 0:
            reward = 0.5
        # else:
        #     reward = -0.05
        
        done = next_state.is_terminal

        if done:
            if not next_state.is_win:
                reward = -1
            else:
                reward = 1
                print("Win!")

        if not train:
            env.display()
        else:
            if reward == 0:
                moves_without_reward += 1
            if moves_without_reward > abs(state.get_value() + 1):
                reward = -0.5
                done = True

            agent.update(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
        if done:
            break

    return total_reward



if __name__ == "__main__":
    train = False

    lr = 0.001
    gamma = 0.9
    num_features = 16
    # num_features = 12

    for epsilon in range(9 if train else 0, -1, -1):
        print("epsilon:", epsilon)
        epsilon /= 10
        if train:
            env = SnakeGame(simulation_mode=True)
            agent = Agent(num_features, len(list(Direction)), lr, gamma, epsilon)
            episodes = 25000
        else:
            env = SnakeGame(simulation_mode=False)
            agent = Agent(num_features, len(list(Direction)))
            episodes = 1

        total_rewards = 0
        # max_total_rewards = 2.4791499999999975
        max_total_rewards = float('-inf')
        # max_total_rewards = 2.5031000000000008

        for i in range(1, episodes+1):
            total_reward = play_and_train(env, agent, train)
            total_rewards += total_reward
            if i % 1000 == 0:
                print(f"Episode: {i}, average of total rewards: {total_rewards/1000}")
                if total_rewards/1000 > max_total_rewards:
                    max_total_rewards = total_rewards/1000
                    agent.save_weights()
                total_rewards = 0
