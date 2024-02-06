from Direction import Direction
from constants import GRID_SIZE, YELLOW

class Snake:
    snake_counter = 0
    def __init__(self, initial_position, color=YELLOW, alergic_to_apples=False) -> None:
        self.position: tuple[int, int] = initial_position
        self.body: list[tuple[int, int]] = [initial_position]
        self.score = 0
        self.color = color
        self.direction = None
        self.new_direction = None
        self.add_segment = False
        self.head_prev_position = None
        self.idx = self.snake_counter
        Snake.snake_counter += 1
        self.is_dead = False
        self.alergic_to_apples = alergic_to_apples

    def get_possible_actions(self) -> list[Direction]:
        if self.direction is None or self.alergic_to_apples:
            return list(Direction)
        
        possible_actions = []

        for direction in list(Direction):
            if abs(self.direction.value - direction.value) == 2:
                continue

            possible_actions.append(direction)
        return possible_actions
    
    def change_direction(self, direction: Direction) -> None:
        if self.new_direction is None:
            self.new_direction = direction
        elif direction is not None and self.direction is not None and (abs(self.direction.value-direction.value) != 2 or self.alergic_to_apples):
            self.new_direction = direction

    def did_eat(self, apple):
        if self.position == apple.position:
            self.score += 1
            if not self.alergic_to_apples:
                self.add_segment = True
            return True
        return False
    
    def kill(self, other):
        self.score += 10
        other.die()

    def die(self):
        self.is_dead = True
        self.score -= GRID_SIZE[0]*GRID_SIZE[1]
    
    def move(self):
        self.direction = self.new_direction

        new_pos = self.position
        if self.direction == Direction.LEFT:
            new_pos = (self.position[0]-1, self.position[1])
        if self.direction == Direction.RIGHT:
            new_pos = (self.position[0]+1, self.position[1])
        if self.direction == Direction.UP:
            new_pos = (self.position[0], self.position[1]-1)
        if self.direction == Direction.DOWN:
            new_pos = (self.position[0], self.position[1]+1)

        self.head_prev_position = self.position
        self.position = new_pos

        for i, segment in enumerate(self.body):
            prev_pos = segment
            self.body[i] = new_pos
            new_pos = prev_pos
        
        if self.add_segment:
            self.body.append(new_pos)
            self.add_segment = False

    def __str__(self):
        return f"Snake {self.idx}"