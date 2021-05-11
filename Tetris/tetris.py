import pygame
import math
import sys
from random import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 230, 0)
PURPLE = (205, 0, 255)
ORANGE = (255, 100, 0)
TEAL = (2255, 205, 205)

pygame.init()
W_DIM = 500
H_DIM = 800
BOARD_WIDTH = 400
WIDTH = 40
ROWS = 20
COLS = 10
WIN = pygame.display.set_mode((W_DIM, H_DIM))

figures = {
    'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
    'J': [[1, 5, 8, 9], [0, 4, 5, 6], [1, 2, 5, 9], [0, 1, 2, 6]],
    'L': [[1, 5, 9, 10], [0, 1, 2, 4], [0, 1, 5, 9], [2, 4, 5, 6]],
    'O': [[1, 2, 5, 6]],
    'S': [[1, 2, 4, 5], [1, 5, 6, 10]],
    'T': [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],
    'Z': [[0, 1, 5, 6], [2, 5, 6, 9]]
}

colors = {
    'I': BLUE,
    'J': RED,
    'L': GREEN,
    'O': YELLOW,
    'S': PURPLE,
    'T': ORANGE,
    'Z': TEAL
}


class Cell:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        self.is_occupied = False
        self.tetramino = None

    def is_occupied(self, tetramino):
        self.is_occupied = True
        self.tetramino = type

    def not_occupied(self):
        self.is_occupied = False
        self.type = None

    def draw(self, win):
        if self.tetramino == None:
            pygame.draw.rect(
                win, WHITE, (self.col, self.row, self.width, self.width))


class Tetramino:

    def __init__(self, type, x, y):
        self.type = type
        self.graphs = figures[type]
        self.color = colors[type]
        self.disposition = 0
        self.x_pos = x
        self.y_pos = y

    def rotate(self):
        length = len(self.graphs)
        self.disposition = (self.disposition + 1) % length


def make_grid(rows, cols, width):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            cell = Cell(i, j, width)
            grid[i].append(cell)
    return grid


def draw_grid(rows, cols, width, win, board_dim, h_dim):
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * width), (board_dim, i * width))
    for j in range(cols + 1):
        pygame.draw.line(win, BLACK, (j * width, 0), (j * width, h_dim))


def draw(grid, rows, cols, width, win, w_dim, h_dim):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)
    draw_grid(rows, cols, width, win, w_dim, h_dim)
    pygame.display.update()


def main(rows, cols, width, win, w_dim, h_dim):
    run = True
    grid = make_grid(rows, cols, width)
    while run:
        draw(grid, rows, cols, width, win, w_dim, h_dim)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False


main(ROWS, COLS, WIDTH, WIN, BOARD_WIDTH, H_DIM)
