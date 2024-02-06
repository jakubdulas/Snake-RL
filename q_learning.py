from collections import defaultdict
from State import State
from SnakeGame import SnakeGame
import random
import json
import os


class QLearningAgent:
    def __init__(self, alpha, epsilon, discount):
        self._qvalues = defaultdict(lambda: defaultdict(lambda: 0))
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount

    def get_qvalue(self, state: State, action):
        if str(state.state) not in self._qvalues:
            self._qvalues[str(state.state)] = {str(action.value): 0}
            return 0
        elif str(action.value) not in self._qvalues[str(state.state)]:
            self._qvalues[str(state.state)][str(action.value)] = 0
            return 0
        return self._qvalues[str(state.state)][str(action.value)]
    
    def set_qvalue(self, state: State, action, value):
        self._qvalues[str(state.state)][str(action.value)] = value

    def get_value(self, state: State):
        possible_actions = state.get_possible_actions()

        if len(possible_actions) == 0:
            return 0.0

        max_value = float('-inf')
        for action in possible_actions:
            val = self.get_qvalue(state, action)
            if val > max_value:
                max_value = val

        return max_value

    def update(self, state: State, action, reward, next_state: State):
        gamma = self.discount
        learning_rate = self.alpha

        new_val = (1 - learning_rate) * self.get_qvalue(state, action) + learning_rate*(reward+gamma*self.get_value(next_state))

        self.set_qvalue(state, action, new_val)

    def get_best_action(self, state):
        possible_actions = state.get_possible_actions()

        if len(possible_actions) == 0:
            return None

        best_actions = []
        best_value = float('-inf')
        for action in possible_actions:
            try:
                val = self.get_qvalue(state, action)
            except:
                return random.choice(possible_actions)
            
            if val > best_value:
                best_actions = []
                best_value = val
                best_actions.append(action)
            elif val == best_value:
                best_actions.append(action)

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

    def save_qtable(self):
        with open('q_table.json', 'w+') as f:
            json.dump({str(k): v for k, v in self._qvalues.items()}, f)

    def load_qtable(self):
        if os.path.exists('q_table.json'):
            with open('q_table.json', 'r') as f:
                obj = json.load(f)
            self._qvalues = obj


def play_and_train(env: SnakeGame, agent: QLearningAgent, train):
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
        agent = QLearningAgent(alpha=0.5, epsilon=0.30, discount=0.99)
        episodes = 1000000
    else:
        env = SnakeGame(simulation_mode=False)
        agent = QLearningAgent(alpha=0.5, epsilon=0, discount=0.99)
        episodes = 1
    agent.load_qtable()

    for i in range(1, episodes+1):
        total_reward = play_and_train(env, agent, train)
        if i % 1000 == 0:
            print(f"Episode: {i}, total reward: {total_reward}, states: {len(agent._qvalues)}")
            agent.save_qtable()
