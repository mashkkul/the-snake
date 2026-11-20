from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Центральная позиция игрового поля:
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Словварь допустимых направлений
DIRECTION_MAP = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов с позицией, цветом и отрисовкой."""

    def __init__(self, body_color=None):
        self.position = CENTER_POSITION
        self.body_color = body_color

    def draw_cell(self, position, color=None):
        """Отрисовывает одну ячейку на игровом поле."""
        cell_color = color if color is not None else self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, cell_color, rect)

        if cell_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод отрисовки объекта (переопределяется в классах-потомках)."""
        raise NotImplementedError(
            'Метод draw должен быть переопределен в дочернем классе.'
        )


class Apple(GameObject):
    """Класс, описывающий яблоко на игровом поле."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=None):
        super().__init__(body_color)
        self.randomize_position(occupied_cells if occupied_cells else [])

    def randomize_position(self, occupied_cells):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            occupied_cells[0] if occupied_cells else CENTER_POSITION
        )
        while self.position in occupied_cells:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )

    def draw(self):
        """Метод draw класса Apple."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку и управляющий ее движением."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет положение змейки на поле."""
        head_position_x, head_position_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            (head_position_x + direction_x) % SCREEN_WIDTH,
            (head_position_y + direction_y) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод draw класса Snake."""
        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position())


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            new_direction = DIRECTION_MAP.get(
                (game_object.direction, event.key)
            )
            if new_direction:
                game_object.next_direction = new_direction


def main():
    """Главная функция игры."""
    # Инициализация PyGame:
    pg.init()
    # Создание экземпляров классов:
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        # Основная логика игры:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
