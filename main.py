from SnakeGame import SnakeGame


if __name__ == '__main__':
    game = SnakeGame()

    while not game.is_end:
        snake1_action = game.handle_events()
        game.step(snake1_action)
        game.display()

    if game.winner is None:
        print("Draw")
    else:
        print(game.winner)
        print(game.winner.score)