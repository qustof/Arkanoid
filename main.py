import pygame
from random import randrange as rnd #Импорт библиотеки Pygame и функции randrange из модуля random с псевдонимом rnd.

WIDTH, HEIGHT = 1200, 800 # Определение ширины и высоты игрового окна.
fps = 60 # Установка частоты кадров в секунду.
# Параметры для платформы игрока включая ширину, высоту и скорость.
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h) # Создание прямоугольника для платформы игрока.
# Установка радиуса и скорости мяча.
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)  # Создание прямоугольника для мяча с случайными начальными координатами.
dx, dy = 1, -1 # Начальные значения для вектора движения мяча.
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)] # # Создание списка прямоугольников для блоков.
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)] # Создание списка случайных цветов для блоков.

pygame.init() # Инициализация библиотеки Pygame.
sc = pygame.display.set_mode((WIDTH, HEIGHT)) # Создание окна игры заданных размеров. ширина высота
clock = pygame.time.Clock() # Создание объекта Clock для управления частотой кадров.
# задний фон
img = pygame.image.load('1.jpg').convert()


def detect_collision(dx, dy, ball, rect): # Функция для обнаружения и обработки столкновений мяча с другими объектами (платформой, блоками).
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


while True: # функция обрабатывает новые события и тд
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    # drawing world
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
    # ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    # коллизия лево право
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    # коллизия вверх
    if ball.centery < ball_radius:
        dy = -dy
    # коллизия вниз
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
        # Коллизия блоков
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        # Эффекты
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2
    # Проверяется проигрыш или победа
    if ball.bottom > HEIGHT:
        print('GAME OVER!')
        exit()
    elif not len(block_list):
        print('WIN!!!')
        exit()
    # контроль(клавиши)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed
    # обновление (фпс)
    pygame.display.flip()
    clock.tick(fps)