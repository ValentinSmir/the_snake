from random import choice, randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

direction = [RIGHT, LEFT, UP, DOWN]


class GameObject:
    """Базовый класс."""

    def __init__(self, body_color=None) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self) -> None:
        """Этот метод должен определять, как объект
        будет отрисовываться на экране.
        """
        pass


class Apple(GameObject):
    """Класс описывающий яблоко."""

    def __init__(self, body_color: tuple = APPLE_COLOR) -> None:
        super().__init__(body_color)
        self.position_x, self.position_y = self.randomize_position()

    def randomize_position(self) -> tuple:
        """Случайная позиция яблока."""
        self.position = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                         (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
        return self.position

    def draw(self, surface):
        """Метод для рисовки яблока."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывающий змейку."""

    def __init__(self, body_color: tuple = SNAKE_COLOR) -> None:
        super().__init__(body_color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None
        self.last = None

    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод обновляет позицию змейки добавляя новую голову в начало списка
        и удаляя последний элемент.
        """
        head_x, head_y = self.get_head_position()
        direct_x, direct_y = self.direction
        self.posit = ((head_x + (direct_x * GRID_SIZE)) % SCREEN_WIDTH,
                      (head_y + (direct_y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, self.posit)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self) -> None:
        """Метод сбрасывает змейку в начальное
        состояние после столкновения с собой.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(direction)

    def draw(self, surface):
        """Метод отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self) -> None:
        """Метод  обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш, чтобы
    изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    apple = Apple()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.posit in snake.positions[2:-1]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
