import random
from SnakeGame import SnakeGame
import numpy as np
import random
import time
from State import State
from Direction import Direction
from copy import deepcopy


class MCTSAgent:
    class Node:
        def __init__(self, state, action=None, parent=None):
            self.state: State = state
            self.action: Direction = action
            self.parent = parent
            self.children: list[MCTSAgent.Node] = []
            self.visits: int = 0
            self.score: int = 0

    def __init__(self, iterations=1000, exploration_weight=2):
        self.iterations = iterations
        self.exploration_weight = exploration_weight

    def backpropagate(self, node: Node, score):
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    def rollout(self, state):
        game = SnakeGame(deepcopy(state), True)
        # prev_state = None
        # if not state.is_terminal:
        #     print("="*10, "Rollout", "="*10)
        while True:
            # if state.is_terminal:
            #     if state.is_win:
            #         return 1
            #     return 0
            # elif prev_state is not None and prev_state.apple.position != state.apple.position:
            #     return 0.1
            if state.is_terminal:
                return state.get_value()
            
            action = random.choice(state.get_possible_actions())
            # print(action)
            # print(state)
            # prev_state = deepcopy(state)
            game.step(action)
            state = game.get_state()

    def expand(self, node: Node):
        actions = node.state.get_possible_actions()
        for action in actions:
            game = SnakeGame(deepcopy(node.state), True)
            game.step(action)
            node.children.append(MCTSAgent.Node(game.get_state(), action, node))

    def ucb1(self, node, exploration_weight=None):
        if exploration_weight is None:
            exploration_weight = self.exploration_weight
        return node.score / node.visits + exploration_weight * np.sqrt(np.log(node.parent.visits) / node.visits) if node.visits != 0 else float('inf')

    def select(self, node: Node):
        return max(node.children, key=lambda c: self.ucb1(c))
    
    def take_best_action(self, children):
        max_visits = children[0].visits
        best_action = children[0].action
        for child in children[1:]:
            if child.visits > max_visits:
                max_visits = child.visits
                best_action = child.action
        return best_action

    def mcts(self, state: State, iterations: int):
        root_node = MCTSAgent.Node(state)

        for _ in range(iterations):
            current_node = root_node

            # Selection
            while len(current_node.children) != 0:
                current_node = self.select(current_node)

            # Expansion
            # if current_node.visits != 0:
            self.expand(current_node)
            current_node = self.select(current_node)

            # Simulation
            score = self.rollout(current_node.state)

            # Backpropagation
            self.backpropagate(current_node, score)

        best_node = max(root_node.children, key=lambda c: self.ucb1(c, 0))
        print(self.ucb1(best_node, 0))
        return best_node.action
        # return self.take_best_action(root_node.children)
    
    def choose_action(self, state):
        return self.mcts(state, self.iterations)


if __name__ == '__main__':
    playing = True
    game = SnakeGame()
    game.disable_events()
    agent = MCTSAgent(1000, exploration_weight=2)

    while not game.is_end:
        action = agent.choose_action(game.get_state())
        print(action)
        print(game.get_state())
        game.step(action)
        game.display()
        # time.sleep(0.)
    