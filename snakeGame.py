import pygame as pygame
from random import randrange

WINDOW = 600
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)

get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

snake = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()

length = 1
snake_segments = [snake.copy()]
snake_direction = (0, 0)

food = snake.copy()
food.center = get_random_position()

screen = pygame.display.set_mode([WINDOW] * 2)
clock = pygame.time.Clock()
time, time_step = 0, 110

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake_direction = (0, -TILE_SIZE)
            if event.key == pygame.K_s:
                snake_direction = (0, TILE_SIZE)
            if event.key == pygame.K_a:
                snake_direction = (-TILE_SIZE, 0)
            if event.key == pygame.K_d:
                snake_direction = (TILE_SIZE, 0)

    screen.fill('black')

    # check borders
    selfeating = pygame.Rect.collidelist(snake, snake_segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or selfeating:
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_direction = 1, (0, 0)
        snake_segments = [snake.copy()]
    
    # check food
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1

    # draw food
    pygame.draw.rect(screen, 'red', food)

    # draw snake
    [pygame.draw.rect(screen, 'green', segment) for segment in snake_segments]

    # move snake
    time_now = pygame.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_direction)
        snake_segments.append(snake.copy())
        snake_segments = snake_segments[-length:]

    pygame.display.flip()
    clock.tick(60)