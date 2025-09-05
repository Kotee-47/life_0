# Импорты
import time

import pygame
import random
from pygame.locals import *
from time import sleep

# Константы цветов RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# Создаем окно
pygame.init()
root = pygame.display.set_mode((1000, 1000))
# 2х мерный список с помощью генераторных выражений
cells = [[random.choice([0, 1]) for j in range(root.get_width() // 20)] for i in range(root.get_height() // 20)]
pause = False
ckl = 0
speed = 200
fast = False
slow = False
textrect = pygame.Rect(10, 10, 100, 30)
font = pygame.font.SysFont('Segoe UI', 36, True)


# Функция определения кол-ва соседей
def near(pos: list, system=[[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]):
    count = 0
    for i in system:
        if cells[(pos[0] + i[0]) % len(cells)][(pos[1] + i[1]) % len(cells[0])]:
            count += 1
    return count


# Основной цикл
while 1:
    # Заполняем экран белым цветом
    root.fill(WHITE)
    p = True
    if ckl < speed:
        ckl += 1
    else:
        ckl = 0
    if fast:
        if speed > 50:
            speed -= 50
            print('faster', speed)
    if slow:
        if speed < 2000:
            speed += 50
            print('slower', speed)
    fast = False
    slow = False

    # Рисуем сетку
    for i in range(0, root.get_height() // 20):
        pygame.draw.line(root, BLACK, (0, i * 20), (root.get_width(), i * 20))
    for j in range(0, root.get_width() // 20):
        pygame.draw.line(root, BLACK, (j * 20, 0), (j * 20, root.get_height()))
    for i in pygame.event.get():
        if i.type == QUIT:
            quit()
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and p:
            print('pressed')
            if pause:
                pause = False
            elif not pause:
                pause = True
            p = False
            print(pause)
        if key[pygame.K_UP]:
            fast = True
        if key[pygame.K_DOWN]:
            slow = True

    # Проходимся по всем клеткам

    if not pause and ckl == 0:
        for i in range(0, len(cells)):
            for j in range(0, len(cells[i])):
                pygame.draw.rect(root, (255 * cells[i][j] % 256, 0, 0), [i * 20, j * 20, 20, 20])
        # Обновляем экран
        pygame.draw.rect(root, 'blue', textrect)
        text_surface = font.render(str(speed), True, 'black')
        text_rect = text_surface.get_rect(center=textrect.center)
        root.blit(text_surface, text_rect)
        pygame.display.update()
        cells2 = [[0 for j in range(len(cells[0]))] for i in range(len(cells))]
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                if cells[i][j]:
                    if near([i, j]) not in (2, 3):
                        cells2[i][j] = 0
                        continue
                    cells2[i][j] = 1
                    continue
                if near([i, j]) == 3:
                    cells2[i][j] = 1
                    continue
                cells2[i][j] = 0
        cells = cells2
