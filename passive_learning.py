from Direction import Direction
from SnakeGame import SnakeGame
from State import State
from constants import GRID_SIZE


class ValueIterationAgent:
    def __init__(self, gamma, theta):
        self.gamma = gamma
        self.theta = theta
        self.actions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]

    def get_all_states(self):
        states = []
        for i in range(GRID_SIZE[0]*GRID_SIZE[1]):
            for j in range(GRID_SIZE[0]*GRID_SIZE[1]):
                array = [0]*(GRID_SIZE[0]*GRID_SIZE[1])
                array[j] = 1 
                if i != j:
                    array[i] = 2 
                states.append(tuple(array))
        
        return states

    def get_next_state_and_reward(self, state, action):
        state = State.load_state_by_map(state)
        game = SnakeGame(state, simulation_mode=True, snake_alergic_to_apples=True)
        game.step(action)
        next_state = game.get_state()

        reward = 0
        if next_state.get_map().index(1) != state.get_map().index(1):
            reward = 1
        if next_state.is_terminal:
            reward = -10

        return next_state.get_map(), reward

    def get_policy(self):
        V = dict()
        policy = dict()
        all_states = self.get_all_states()

        for current_state in all_states:
            V[current_state] = 0
            policy[current_state] = self.actions[0]

        delta = float('inf')
        while delta > self.theta:
            delta = 0

            for state in all_states:
                prev_state_val = V[state]

                best_action = None
                best_action_val = float('-inf')

                for action in self.actions:
                    next_state, reward = self.get_next_state_and_reward(state, action)
                    x = 0.25*(reward+self.gamma*V[next_state])

                    if x > best_action_val:
                        best_action_val = x
                        best_action = action


                V[state] = best_action_val
                policy[state] = best_action
                
                delta = max(delta, abs(prev_state_val-V[state]))
        return policy


if __name__ == '__main__':
    env = SnakeGame(snake_alergic_to_apples=True)
    agent = ValueIterationAgent(0.9, 0.057)
    policy = agent.get_policy()

    env.disable_events()

    while not env.is_end:
        action = policy[env.get_state().get_map()]
        env.step(action)

        env.display()