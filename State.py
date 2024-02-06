from copy import deepcopy
from Snake import Snake
from constants import GRID_SIZE
from Apple import Apple


class State:
    def __init__(self, snake: Snake,  apple, is_terminal, is_win) -> None:
        self.snake = deepcopy(snake)
        self.apple = deepcopy(apple)
        self.is_terminal = is_terminal
        self.is_win = is_win

    @property
    def state(self):
        state = (
            self.snake.position[0] < self.apple.position[0],
            self.snake.position[1] < self.apple.position[1],
            self.snake.position[0] == self.apple.position[0],
            self.snake.position[1] == self.apple.position[1],
            bool(sum(el[0] < self.snake.position[0] for el in self.snake.body)),
            bool(sum(el[0] > self.snake.position[0] for el in self.snake.body)),
            bool(sum(el[1] < self.snake.position[1] for el in self.snake.body)),
            bool(sum(el[1] > self.snake.position[1] for el in self.snake.body)),
            self.snake.position[0] - 1 < 0 or self.snake.position[0] - 1 in [el[0] for el in self.snake.body[1:]],
            self.snake.position[0] + 1 >= GRID_SIZE[1] or self.snake.position[1] + 1 in [el[0] for el in self.snake.body[1:]],
            self.snake.position[1] - 1 < 0 or self.snake.position[1] - 1 in [el[1] for el in self.snake.body[1:]],
            self.snake.position[1] + 1 >= GRID_SIZE[0] or self.snake.position[1] + 1 in [el[1] for el in self.snake.body[1:]],
        )
        return tuple(int(e) for e in state)
    
    def get_features(self):
        state = (
            self.snake.position[0] < self.apple.position[0],
            self.snake.position[1] < self.apple.position[1],
            self.snake.position[0] == self.apple.position[0],
            self.snake.position[1] == self.apple.position[1],
            bool(sum(el[0] < self.snake.position[0] for el in self.snake.body)),
            bool(sum(el[0] > self.snake.position[0] for el in self.snake.body)),
            bool(sum(el[1] < self.snake.position[1] for el in self.snake.body)),
            bool(sum(el[1] > self.snake.position[1] for el in self.snake.body)),
            self.snake.position[0] - 1 < 0 or self.snake.position[0] - 1 in [el[0] for el in self.snake.body[1:]],
            self.snake.position[0] + 1 >= GRID_SIZE[1] or self.snake.position[1] + 1 in [el[0] for el in self.snake.body[1:]],
            self.snake.position[1] - 1 < 0 or self.snake.position[1] - 1 in [el[1] for el in self.snake.body[1:]],
            self.snake.position[1] + 1 >= GRID_SIZE[0] or self.snake.position[1] + 1 in [el[1] for el in self.snake.body[1:]],
            int(bool(sum([(el[0] == GRID_SIZE[0]-1 ) for el in self.snake.body]))),
            int(bool(sum([(el[0] == 0) for el in self.snake.body]))),
            int(bool(sum([(el[1] == GRID_SIZE[1]-1 ) for el in self.snake.body]))),
            int(bool(sum([(el[1] == 0) for el in self.snake.body]))),
        )
        return tuple(int(e) for e in state)
    
    @classmethod
    def load_state_by_map(cls, map: list):
        is_terminal = False
        try:
            x_snake = map.index(2) % GRID_SIZE[1]
            y_snake = map.index(2) // GRID_SIZE[0]
        except:
            x_snake = -1
            y_snake = -1
            is_terminal = True

        x_apple = map.index(1) % GRID_SIZE[1]
        y_apple = map.index(1) // GRID_SIZE[0]

        snake = Snake((x_snake, y_snake), alergic_to_apples=True)
        apple = Apple(snake, (x_apple, y_apple))
        return cls(snake, apple, is_terminal, False)
    
    def get_reward(self, next_state):
        return next_state.get_value() - self.get_value()
    
    def get_map(self):
        map = []
        for y in range(GRID_SIZE[0]):
            for x in range(GRID_SIZE[1]):
                pos = (x, y)
                if self.apple.position == pos:
                    map.append(1)
                elif pos in self.snake.body:
                    if pos == self.snake.position:
                        map.append(2)
                    else:
                        map.append(3)
                else:
                    map.append(0)
        return tuple(map)

    def get_possible_actions(self):
        return self.snake.get_possible_actions()
    
    def get_value(self):
        if self.is_win:
            return self.snake.score
        else:
            return self.snake.score-GRID_SIZE[0]*GRID_SIZE[1]
        
    def __getitem__(self, key):
        if key == 'snake':
            return self.snake
        if key == 'apple':
            return self.apple
        if key == 'is_terminal':
            return self.is_terminal
        if key == 'is_win':
            return self.is_win
        raise KeyError
    
    def __str__(self):
        rep = '='*GRID_SIZE[1] + '\n'
        rep += f'Snake score: {self.snake.score}\n'
        rep += '-'*GRID_SIZE[1] + '\n'
        for y in range(GRID_SIZE[0]):
            for x in range(GRID_SIZE[1]):
                pos = (x, y)
                if self.apple.position == pos:
                    rep += 'A'
                elif pos in self.snake.body:
                    if pos == self.snake.position:
                        rep += 'H'
                    else:
                        rep += 'T'
                else:
                    rep += ' '
            rep += '\n'
        rep += '='*GRID_SIZE[1]
        return rep