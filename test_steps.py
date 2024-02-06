import time
from Direction import Direction
from Snake import Snake
from SnakeGame import SnakeGame
from constants import GREEN, BLUE, GRID_SIZE
from Apple import Apple
from State import State


if __name__ == '__main__':
    snake= Snake((0, 0), BLUE)
    apple = Apple(snake)
    apple.position = (0, 1)
    state = State(
        snake,
        apple,
        False,
        False
    )
    game = SnakeGame(state, True)

    actions = [
        Direction.DOWN,
        Direction.RIGHT,
        Direction.UP,
        Direction.LEFT,
    ]
    
    print(game.get_state())
    while not game.is_end:
        for a in actions:
            game.step(a)
            print(a)
            # game.display()
            print("="*10, "Game Step", "="*10)
            print(game.get_state())
            if game.is_end:
                break
            # time.sleep(1)

    print(game.snake.position)
    print(game.is_win)
    