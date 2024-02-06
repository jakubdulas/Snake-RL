from constants import GRID_SIZE, RED
from Snake import Snake
import random


class Apple:
    def __init__(self, snake, initial_position=None):
        self.color = RED
        if initial_position is not None:
            self.position = initial_position
        else:
            possible_positions = []
            occupied_positions = snake.body
            for i in range(GRID_SIZE[0]):
                for j in range(GRID_SIZE[1]):
                    if (i, j) not in occupied_positions:
                        possible_positions.append((i, j))

            if len(possible_positions) > 0:
                self.position = random.choice(possible_positions)
            else:
                self.position = (-1, -1)