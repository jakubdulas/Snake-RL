import pygame
from constants import *
from Direction import Direction
import random
from Snake import Snake
from Apple import Apple
from State import State
import time


class SnakeGame:
    def __init__(self, state=None, simulation_mode=False, snake_alergic_to_apples=False) -> None:
        self.simulation_mode = simulation_mode
        self.snake_alergic_to_apples = snake_alergic_to_apples

        self.reset()

        if state:
            self.load_state(state)
            
    def reset(self):
        if not self.simulation_mode:
            pygame.init()
            self.screen = pygame.display.set_mode(WINDOW_SIZE)
            self.clock = pygame.time.Clock()
            self.MOVE_SNAKE = pygame.USEREVENT + 1
            pygame.time.set_timer(self.MOVE_SNAKE, 300)

        self.snake = Snake((GRID_SIZE[0]//2, GRID_SIZE[1]//2), GREEN, self.snake_alergic_to_apples)
        self.generate_apple()
    
        self.is_end = False
        self.is_win = False
        self.events_disabled = False

    def disable_events(self):
        self.events_disabled = True

    def load_state(self, state):
        self.snake = state['snake']
        self.apple = state['apple']
        self.is_end = state['is_terminal']

    def generate_apple(self):
        self.apple = Apple(self.snake)

    def terminate(self):
        self.is_end = True

    def check_collision(self):
        if min(self.snake.position) < 0 or max(self.snake.position) >= GRID_SIZE[0]:
            self.terminate()
        
        if self.snake.position in self.snake.body[1:]:
            self.terminate()

    def check_win(self):
        if len(self.snake.body) == GRID_SIZE[0]*GRID_SIZE[1]:
            self.terminate()
            self.is_win = True

    def get_state(self):
        return State(self.snake, self.apple, self.is_end, self.is_win)

    def move_snake(self):
        if not self.is_end:
            self.snake.move()

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        snake_action = None
        if keys[pygame.K_a]:
            snake_action = Direction.LEFT
        elif keys[pygame.K_d]:
            snake_action = Direction.RIGHT
        elif keys[pygame.K_w]:
            snake_action = Direction.UP
        elif keys[pygame.K_s]:
            snake_action = Direction.DOWN

        return snake_action
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.is_end:
                pygame.quit()
            elif event.type == self.MOVE_SNAKE:
                self.move_snake()

    def step(self, snake_action=None):
        self.snake.change_direction(snake_action)
        if self.simulation_mode or self.events_disabled:
            self.move_snake()
        else:
            self.handle_events()
        
        if self.snake.did_eat(self.apple):
            self.generate_apple()

        self.check_win()
        self.check_collision()

    def draw_apple(self):
        pygame.draw.rect(self.screen, self.apple.color, (self.apple.position[0]*BLOCK_SIZE, self.apple.position[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_snake(self):
        pygame.draw.rect(self.screen, YELLOW, (self.snake.position[0] * BLOCK_SIZE, self.snake.position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for segment in self.snake.body[1:]:
            pygame.draw.rect(self.screen, self.snake.color, (segment[0] * BLOCK_SIZE, segment[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def display(self):
        if self.simulation_mode:
            raise Exception("Cannot display when simulation mode is on")
        
        self.screen.fill(BLACK)
        self.draw_apple()
        self.draw_snake()

        pygame.display.flip()
        self.clock.tick(FPS)


if __name__ == '__main__':
    game = SnakeGame(snake_alergin_to_apples=True)

    while not game.is_end:
        action = game.handle_keys()
        game.step(action)
        game.display()

