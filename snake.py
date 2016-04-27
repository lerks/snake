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

pygame.time.set_timer(31, 75)
pygame.event.post(pygame.event.Event(31))

def get_mouse_coord():
    if len(snake) == grid[0] * grid[1]:
        pygame.time.set_timer(31, 0)
    while True:
        x = random.randint(0, grid[0] - 1)
        y = random.randint(0, grid[1] - 1)
        if 's' not in content[x][y]:
            return x, y


def get_rat_coord():
    candidates = []
    for x in range(grid[0]-1):
        for y in range(grid[1]-1):
            if content[x][y] == '' and content[x+1][y] == '' and content[x][y+1] == '' and content[x+1][y+1] == '':
                candidates += [(x, y)]
    if len(candidates) == 0:
        return None
    return random.choice(candidates)


def init():
    snake.extend([(grid[0]/2, grid[1]/2), (grid[0]/2-1, grid[1]/2)])
    content[grid[0]/2][grid[1]/2] = 's'
    content[grid[0]/2-1][grid[1]/2] = 's'

    mouse = get_mouse_coord()
    content[mouse[0]][mouse[1]] = 'm'


init()


rat_position = None
rat_life = None
rat_life_max = 50
rat_cycle = 0
rat_cycle_max = 5


score = 0


while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if 273 <= event.key <= 276:
            dir_ = directions[event.key - 273]
            if dir_[0] != -1 * actual_direction[0] or dir_[1] != -1 * actual_direction[1]:
                direction = dir_
    elif event.type == 31:
        head = ((snake[0][0] + direction[0]) % grid[0], (snake[0][1] + direction[1]) % grid[1])
        tail = snake[-1]

        if 'm' in content[tail[0]][tail[1]] or 'r' in content[tail[0]][tail[1]]:
            content[tail[0]][tail[1]] = 's'
        else:
            snake = snake[:-1]
            content[tail[0]][tail[1]] = ''

        if rat_life is not None:
            rat_life -= 1
            if rat_life == 0:
                content[rat_position[0]][rat_position[1]] = ''
                content[rat_position[0]+1][rat_position[1]] = ''
                content[rat_position[0]][rat_position[1]+1] = ''
                content[rat_position[0]+1][rat_position[1]+1] = ''
                rat_position = None
                rat_life = None

        if 's' in content[head[0]][head[1]]:
            pygame.time.set_timer(31, 0)
        elif 'r' in content[head[0]][head[1]]:
            score += 20 + 480 * rat_life / rat_life_max
            content[rat_position[0]][rat_position[1]] = ''
            content[rat_position[0]+1][rat_position[1]] = ''
            content[rat_position[0]][rat_position[1]+1] = ''
            content[rat_position[0]+1][rat_position[1]+1] = ''
            content[head[0]][head[1]] = 'sr'
            rat_position = None
            rat_life = None
            snake = [head] + snake
        elif 'm' in content[head[0]][head[1]]:
            score += 10
            content[head[0]][head[1]] = 'sm'
            mouse = get_mouse_coord()
            content[mouse[0]][mouse[1]] = 'm'
            snake = [head] + snake

            # Rat
            rat_cycle += 1
            if rat_cycle == rat_cycle_max:
                rat_position = get_rat_coord()
                if rat_position is not None:
                    rat_life = rat_life_max
                    content[rat_position[0]][rat_position[1]] = 'r'
                    content[rat_position[0]+1][rat_position[1]] = 'r'
                    content[rat_position[0]][rat_position[1]+1] = 'r'
                    content[rat_position[0]+1][rat_position[1]+1] = 'r'
                rat_cycle = 0
        else:
            content[head[0]][head[1]] = 's'
            snake = [head] + snake

        actual_direction = direction

        screen.fill((0, 0, 0))
        for x in range(grid[0]):
            for y in range(grid[1]):
                if content[x][y] == 's':
                    screen.fill((255, 255, 255), pygame.Rect(x * cell[0], y * cell[1], cell[0], cell[1]))
                elif content[x][y] == 'm':
                    screen.fill((100, 100, 100), pygame.Rect(x * cell[0], y * cell[1], cell[0], cell[1]))
                elif content[x][y] == 'r':
                    screen.fill((140, 93, 32), pygame.Rect(x * cell[0], y * cell[1], cell[0], cell[1]))
                elif content[x][y] == 'sm':
                    screen.fill((200, 200, 200), pygame.Rect(x * cell[0], y * cell[1], cell[0], cell[1]))
                elif content[x][y] == 'sr':
                    screen.fill((138, 117, 90), pygame.Rect(x * cell[0], y * cell[1], cell[0], cell[1]))
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

        myfont = pygame.font.SysFont("Monospace", 40)
        label = myfont.render(str(score), 1, (255, 255, 255))
        screen.blit(label, (30, 30))

        if rat_life is not None:
            s = pygame.Surface((width, height)).convert_alpha()
            s.fill((255, 0, 0, 128), pygame.Rect(50, height - 70, (width - 100) * rat_life / rat_life_max, 20))
            screen.blit(s, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        pygame.display.flip()
