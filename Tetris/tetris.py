import pygame
import math
import sys
import random
from random import *

from pygame.constants import KEYUP


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 230, 0)
PURPLE = (205, 0, 255)
ORANGE = (255, 100, 0)
TEAL = (0, 255, 255)

pygame.init()
W_DIM = 500
H_DIM = 800
BOARD_WIDTH = 400
WIDTH = 40
ROWS = 20
COLS = 10
font = pygame.font.SysFont('freesansbold.ttf', 35)
WIN = pygame.display.set_mode((W_DIM, H_DIM))
pygame.display.set_caption("Tetris")

SHAPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

figures = {
    'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
    'J': [[1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8], [0, 4, 5, 6]],
    'L': [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],
    'O': [[1, 2, 5, 6]],
    'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
    'T': [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],
    'Z': [[4, 5, 9, 10], [2, 6, 5, 9]]
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
        self.occupied = False
        self.tetramino = None
        self.color = WHITE

    def make_occupied(self, tetramino):
        self.occupied = True
        self.tetramino = tetramino
        self.color = colors[tetramino]

    def is_occupied(self):
        return self.occupied

    def not_occupied(self):
        self.occupied = False
        self.tetramino = None
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.col * self.width, self.row * self.width, self.width, self.width))


class Tetramino:

    def __init__(self, type, x, y):
        self.type = type
        self.graphs = figures[type]
        self.color = colors[type]
        self.disposition = 0
        self.x_pos = x
        self.y_pos = y
        self.locked = False

    def display_tetramino(self, win, width, grid, rows, cols):
        count = 0
        for i in range(4):
            for j in range(4):
                cell_x = self.x_pos + j
                cell_y = self.y_pos + i
                if count in self.graphs[self.disposition]:
                    pygame.draw.rect(
                        win, self.color, (cell_x * width, cell_y * width, width, width))
                count += 1

    def next_pos_available(self, grid, rows, cols, next_pos):
        available = True
        next_x, next_y = next_pos
        for i in range(4):
            for j in range(4):
                cell_x = next_x + j
                cell_y = next_y + i
                if i * 4 + j in self.graphs[self.disposition]:
                    if cell_x > cols - 1 or cell_x < 0 or cell_y > rows - 1 or grid[cell_y][cell_x].is_occupied():
                        available = False
        return available

    def rotate(self, grid, rows, cols):
        old_disposition = self.disposition
        self.disposition = (self.disposition + 1) % len(self.graphs)
        if not self.next_pos_available(grid, rows, cols, (self.x_pos, self.y_pos)):
            self.disposition = old_disposition

    def go_left(self, grid, rows, cols):
        if self.next_pos_available(grid, rows, cols, (self.x_pos - 1, self.y_pos)):
            self.x_pos -= 1

    def go_right(self, grid, rows, cols):
        if self.next_pos_available(grid, rows, cols, (self.x_pos + 1, self.y_pos)):
            self.x_pos += 1

    def go_down(self, grid, rows, cols):
        if self.next_pos_available(grid, rows, cols, (self.x_pos, self.y_pos + 1)):
            self.y_pos += 1
        else:
            self.locked = True

    def lock(self, grid):
        for i in range(4):
            for j in range(4):
                cell_x = self.x_pos + j
                cell_y = self.y_pos + i
                if i * 4 + j in self.graphs[self.disposition]:
                    cell = grid[cell_y][cell_x]
                    cell.make_occupied(self.type)

    def is_locked(self):
        return self.locked

    def get_y_pos(self):
        return self.y_pos


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


def draw(grid, rows, cols, width, win, w_dim, h_dim, tetramino, score):
    win.fill(BLACK)
    for row in grid:
        for cell in row:
            cell.draw(win)
    message = font.render("Score: ", True, RED)
    win.blit(message, (415, 100))
    update_score(win, score)
    tetramino.display_tetramino(win, width, grid, rows, cols)
    draw_grid(rows, cols, width, win, w_dim, h_dim)
    pygame.display.update()


def update_score(win, score):
    display_score = font.render(str(score), True, RED)
    win.blit(display_score, (445, 130))


def get_shape(available_shapes):
    if len(available_shapes) < 4:
        available_shapes = SHAPES.copy()
    ran_num = randrange(0, len(available_shapes))
    return available_shapes.pop(ran_num)


def check_line(line):
    is_complete = True
    for cell in line:
        if not cell.is_occupied():
            is_complete = False
            break
    return is_complete


def break_lines(tetramino, grid, rows, cols):
    start_line = tetramino.get_y_pos()
    lines_to_break = 0
    for i in range(start_line, start_line + 4):
        if i < rows and i > 0:
            line = grid[i]
            if check_line(line):
                lines_to_break += 1
                for j in range(i, 1, -1):
                    for k in range(cols):
                        grid[j][k].occupied = grid[j - 1][k].occupied
                        grid[j][k].tetramino = grid[j - 1][k].tetramino
                        grid[j][k].color = grid[j - 1][k].color
    return 10 * (lines_to_break ** 2)


def main(rows, cols, width, win, w_dim, h_dim):
    score = 0
    clock = pygame.time.Clock()
    run = True
    grid = make_grid(rows, cols, width)
    available_shapes = SHAPES.copy()
    current_shape = get_shape(available_shapes)
    next_shape = get_shape(available_shapes)
    tetramino = Tetramino(current_shape, 4, 0)
    pressing_down = False
    fps = 5

    while run:
        if pressing_down:
            fps = 30
        if tetramino.is_locked():
            tetramino.lock(grid)
            new_score = break_lines(tetramino, grid, rows, cols)
            tetramino = Tetramino(next_shape, 4, 0)
            next_shape = get_shape(available_shapes)
            score += new_score

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                tetramino = Tetramino(next_shape, 4, 0)
                next_shape = get_shape(available_shapes)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    tetramino.rotate(grid, rows, cols)
                if event.key == pygame.K_LEFT:
                    tetramino.go_left(grid, rows, cols)
                if event.key == pygame.K_RIGHT:
                    tetramino.go_right(grid, rows, cols)
                if event.key == pygame.K_DOWN:
                    pressing_down = True
            if event.type == KEYUP:
                pressing_down = False
                fps = 5
        tetramino.go_down(grid, rows, cols)
        draw(grid, rows, cols, width, win, w_dim, h_dim, tetramino, score)
        clock.tick(fps)


main(ROWS, COLS, WIDTH, WIN, BOARD_WIDTH, H_DIM)
