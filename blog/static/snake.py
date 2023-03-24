import pygame
from random import randrange

RES = 800  # Размер окна игры (ширина и высота)
SIZE = 50  # Размер блока змейки и яблока на игровом поле

# Затем определяются начальные значения для координат змейки и яблока, длина
# змейки, скорость змейки, переменные для хранения направления движения змейки и переменные для хранения счета игры.
x, y = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
length = 1
#  список кортежей, который будет содержать координаты всех сегментов змейки.
#  В начале игры змейка будет состоять только из одного сегмента с координатами (x, y),
#  которые были сгенерированы в предыдущем фрагменте кода
snake = [(x, y)]
# скорость змейки по x и y соответственно. Изначально змейка не двигается, поэтому скорость равна 0.
dx, dy = 0, 0
#  количество кадров в секунду. Изначально установлено на 60.
fps = 60
dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
score = 0
# snake_speed - начальная скорость змейки, установлена на 10. Скорость змейки будет увеличиваться при ее росте
speed_count, snake_speed = 0, 10

# Затем инициализируется Pygame и создается окно игры.
pygame.init()
surface = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
# Создание шрифтов для отображения текста на экране.
font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)

# img = pygame.image.load('1.jpg').convert()
img = pygame.image.load('static/1.jpg').convert()
# Функция close_game() для проверки событий, таких как закрытие окна.
def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

# Основной игровой цикл.
while True:
    # В этой строке кода используется метод blit() из Pygame,
    # который позволяет наложить одну поверхность на другую.
    # В данном случае, мы наложили изображение фона на поверхность игры.
    surface.blit(img, (0, 0))
    # drawing snake, apple
    # Эта строка кода использует функцию draw.rect() из Pygame для отображения каждого блока змеи на игровом поле.
    [pygame.draw.rect(surface, pygame.Color('green'), (i, j, SIZE - 1, SIZE - 1)) for i, j in snake]
    # Эта строка кода использует функцию draw.rect() из Pygame для отображения яблока на игровом поле.
    pygame.draw.rect(surface, pygame.Color('red'), (*apple, SIZE, SIZE))
    # show score
    render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
    surface.blit(render_score, (5, 5))
    # snake movement
    speed_count += 1
    if not speed_count % snake_speed:
        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-length:]
    # eating food
    if snake[-1] == apple:
        apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
        length += 1
        score += 1
        snake_speed -= 1
        snake_speed = max(snake_speed, 4)
    # game over
    if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
        while True:
            render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
            surface.blit(render_end, (RES // 2 - 200, RES // 3))
            pygame.display.flip()
            close_game()

    pygame.display.flip()
    clock.tick(fps)
    close_game()
    # controls
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        if dirs['W']:
            dx, dy = 0, -1
            dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
    elif key[pygame.K_s]:
        if dirs['S']:
            dx, dy = 0, 1
            dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
    elif key[pygame.K_a]:
        if dirs['A']:
            dx, dy = -1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
    elif key[pygame.K_d]:
        if dirs['D']:
            dx, dy = 1, 0
            dirs = {'W': True, 'S': True, 'A': False, 'D': True, }
