import sys
import random

import pygame
pygame.init()

grid = (39, 29)
cell = (20, 20)
width = grid[0] * cell[0]
height = grid[1] * cell[1]
size = (width, height)

screen = pygame.display.set_mode(size)

directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
direction = directions[2]

actual_direction = directions[2]

snake = []
content = [[""] * grid[1] for x in range(grid[0])]

pygame.time.set_timer(31, 100)
pygame.event.post(pygame.event.Event(31))

def get_mouse_coord():
    if len(snake) == grid[0] * grid[1]:
        sys.exit()
    while True:
        x = random.randint(0, grid[0] - 1)
        y = random.randint(0, grid[1] - 1)
        if 's' not in content[x][y]:
            return x, y


def init():
    snake.extend([(grid[0]/2, grid[1]/2), (grid[0]/2-1, grid[1]/2)])
    content[grid[0]/2][grid[1]/2] = 's'
    content[grid[0]/2-1][grid[1]/2] = 's'

    mouse = get_mouse_coord()
    content[mouse[0]][mouse[1]] = 'm'

init()


while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        dir_ = directions[event.key - 273]
        if dir_[0] != -1 * actual_direction[0] or dir_[1] != -1 * actual_direction[1]:
            direction = dir_
    elif event.type == 31:
        head = ((snake[0][0] + direction[0]) % grid[0], (snake[0][1] + direction[1]) % grid[1])
        head_content = 's'
        tail = snake[-1]

        if 's' in content[head[0]][head[1]]:
            sys.exit()
        elif 'm' in content[head[0]][head[1]]:
            head_content = 'sm'
            mouse = get_mouse_coord()
            content[mouse[0]][mouse[1]] = 'm'

        snake = [head] + snake
        content[head[0]][head[1]] = head_content

        if 'm' in content[tail[0]][tail[1]]:
            content[tail[0]][tail[1]] = 's'
        else:
            snake = snake[:-1]
            content[tail[0]][tail[1]] = ''

        actual_direction = direction

        screen.fill((0, 0, 0))
        for x in range(grid[0]):
            for y in range(grid[1]):
                if content[x][y] == 's':
                    screen.fill((255, 255, 255), pygame.Rect(x * cell[0], y * cell[1], cell[0], cell[1]))
                elif content[x][y] == 'm':
                    screen.fill((100, 100, 100), pygame.Rect(x * cell[0], y * cell[1], cell[0], cell[1]))
                elif content[x][y] == 'sm':
                    screen.fill((200, 200, 200), pygame.Rect(x * cell[0], y * cell[1], cell[0], cell[1]))
                if snake[0] == (x, y):
                    if direction == directions[0]:  # UP
                        screen.fill((200, 100, 100), pygame.Rect(x * cell[0] + 4, y * cell[1] + 2, 4, 8))
                        screen.fill((200, 100, 100), pygame.Rect(x * cell[0] + 12, y * cell[1] + 2, 4, 8))
                    elif direction == directions[1]:  # DOWN
                        screen.fill((200, 100, 100), pygame.Rect(x * cell[0] + 4, y * cell[1] + 10, 4, 8))
                        screen.fill((200, 100, 100), pygame.Rect(x * cell[0] + 12, y * cell[1] + 10, 4, 8))
                    elif direction == directions[2]:  # RIGHT
                        screen.fill((200, 100, 100), pygame.Rect(x * cell[0] + 10, y * cell[1] + 4, 8, 4))
                        screen.fill((200, 100, 100), pygame.Rect(x * cell[0] + 10, y * cell[1] + 12, 8, 4))
                    elif direction == directions[3]:  # LEFT
                        screen.fill((200, 100, 100), pygame.Rect(x * cell[0] + 2, y * cell[1] + 4, 8, 4))
                        screen.fill((200, 100, 100), pygame.Rect(x * cell[0] + 2, y * cell[1] + 12, 8, 4))
        pygame.display.flip()
