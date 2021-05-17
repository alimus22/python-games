import pygame
import math
import sys
import random
from random import *

from pygame.constants import KEYUP

# Basic python implementation of the game Tetris.
# Handles most functionalities of a tetris game.
# Hold current block and press space to directly drop the tetramino
# are among the missing functionalities. Can be added in a future
# implementation/

# Constants
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
W_DIM = 600
H_DIM = 800
BOARD_WIDTH = 400
WIDTH = 40
ROWS = 20
COLS = 10
font = pygame.font.SysFont('freesansbold.ttf', 35)
WIN = pygame.display.set_mode((W_DIM, H_DIM))
pygame.display.set_caption("Tetris")

# List of all possible shape 'ids'
SHAPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']

# Dict. of all possible configurations for each shape.
# Shapes are stored in 4x4 matrices, each cell numbered from
# 0 to 15. The numbers in the lists below corresponds to the
# cells occupied by the corresponding tetramino disposition in
# the 4x4 matrix.
figures = {
    'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
    'J': [[1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8], [0, 4, 5, 6]],
    'L': [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],
    'O': [[1, 2, 5, 6]],
    'S': [[5, 6, 8, 9], [1, 5, 6, 10]],
    'T': [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],
    'Z': [[4, 5, 9, 10], [2, 6, 5, 9]]
}

# Dict. of colors associated with each shape.
colors = {
    'I': BLUE,
    'J': RED,
    'L': GREEN,
    'O': YELLOW,
    'S': PURPLE,
    'T': ORANGE,
    'Z': TEAL
}


# Cell class that composes the playing field. Each cell 'knows' if
# it is currently occupied or not and what type of tetramino is occupying
# it. It also hold the color of the occupying tetramino. If cell is not
# occupied, color is white.
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

# Tetramino class that handles the current tetramino (i.e. the one dropping,
# that can be controlled by the user). It holds its current position,
# disposition (depends on rotation), and if the tetramino has finished
# droping (if it can no longer go down). The tetramino position (x_pos and
# y_pos coordinates) corresponds to the upper left cell of the 4x4 matrix
# that contains tetramino's shape.


class Tetramino:

    def __init__(self, type, x, y):
        self.type = type
        self.graphs = figures[type]
        self.color = colors[type]
        self.disposition = 0
        self.x_pos = x
        self.y_pos = y
        self.locked = False

# Goes over a 4x4 matrix and according to current disposition, draws
# the corresponding tetramino.
    def display_tetramino(self, win, width):
        count = 0  # Number of the cell relative to the 4x4 matrix.

        # Looping through each cell of a 4x4 matrix. Starting at (x_pos, y_pos)
        for i in range(4):
            for j in range(4):
                cell_x = self.x_pos + j
                cell_y = self.y_pos + i
                if count in self.graphs[self.disposition]:
                    pygame.draw.rect(
                        win, self.color, (cell_x * width, cell_y * width, width, width))
                count += 1

# Verifies if the next position the tetramino is tryinig to go to
# is available. Returns true if it is, false if not. Goes over the
# 4x4 matrix corresponding to the next position and verifies if
# every cells that are to be occupied by the tetramino are available.
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

# Rotate the piece by changing its disposition index. Have to verify
# if the new dispotion is possible. This is not verified in 'next_pos_available()'
# because extra verification is needed for edge cases. For example, an 'I' next to
# the board limit in the vertical position should be able to rotate to the horizontal
# position. An offset should be added to the tetramino position for the horizontal
# disposition to be possible.
    def rotate(self, grid, rows, cols):
        old_disposition = self.disposition
        self.disposition = (self.disposition + 1) % len(self.graphs)
        for i in range(4):
            for j in range(4):
                cell_x = self.x_pos + j
                cell_y = self.y_pos + i
                if i * 4 + j in self.graphs[self.disposition]:
                    # If rotation made imposible by right wall, shift tetramino
                    # to the left by 1 cell.
                    if cell_x > cols - 1:
                        self.x_pos -= 1
                    # If rotation made imposible by left wall, shift tetramino
                    # to the right by 1 cell.
                    elif cell_x < 0:
                        self.x_pos += 1
                    # If rotation impossible for any other reason, move is
                    # impossible, keep old disposition.
                    elif cell_y > rows - 1 or grid[cell_y][cell_x].is_occupied():
                        self.disposition = old_disposition

    def go_left(self, grid, rows, cols):
        if self.next_pos_available(grid, rows, cols, (self.x_pos - 1, self.y_pos)):
            self.x_pos -= 1

    def go_right(self, grid, rows, cols):
        if self.next_pos_available(grid, rows, cols, (self.x_pos + 1, self.y_pos)):
            self.x_pos += 1

# Make the tetramino go down by 1 cell. If move is impossible,
# the tetramino is then 'locked' and can no longer move.

    def go_down(self, grid, rows, cols):
        if self.next_pos_available(grid, rows, cols, (self.x_pos, self.y_pos + 1)):
            self.y_pos += 1
        else:
            self.locked = True

# When tetramino is locked and can no longer move. Pass tetramino
# information to the cells composing it and mark them as occupied.
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

# Create a grid made of Cell objects that make up
# the game board.


def make_grid(rows, cols, width):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            cell = Cell(i, j, width)
            grid[i].append(cell)
    return grid

# Draw a grid with the specified number of rows and coloumns.


def draw_grid(rows, cols, width, win, board_dim, h_dim):
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * width), (board_dim, i * width))
    for j in range(cols + 1):
        pygame.draw.line(win, BLACK, (j * width, 0), (j * width, h_dim))


# Displays the board game, the score, the current tetramino,
# as well as all the 'locked' tetraminos.
def draw(grid, rows, cols, width, win, w_dim, h_dim, tetramino, score, next_shape):
    win.fill(BLACK)
    for row in grid:
        for cell in row:
            # Draws the cell with the right color depending on
            # its status
            cell.draw(win)
    # Display and update current score
    message1 = font.render("Score: ", True, RED)
    message2 = font.render("Next: ", True, RED)
    win.blit(message1, (430, 100))
    win.blit(message2, (430, 500))
    update_score(win, score)
    # Shows the next tetramino
    next_tetramino = Tetramino(next_shape, 11, 14)
    next_tetramino.display_tetramino(win, width, grid, rows, cols)
    # Displays the currently falling tetramino.
    tetramino.display_tetramino(win, width, grid, rows, cols)
    draw_grid(rows, cols, width, win, w_dim, h_dim)
    pygame.display.update()


def update_score(win, score):
    display_score = font.render(str(score), True, RED)
    win.blit(display_score, (445, 130))

# Randomly choses a shape among available_shapes list. When a
# shape is chosen, it is taken off from the list.


def get_shape(available_shapes):
    ran_num = randrange(0, len(available_shapes))
    return available_shapes.pop(ran_num)

# Check if all cells of a given line are occupied. If so
# returns true else returns false.


def check_line(line):
    is_complete = True
    for cell in line:
        if not cell.is_occupied():
            is_complete = False
            break
    return is_complete

# When a tetramino is locked, all the rows passing through its
# 4x4 matrix are checked for complete lines. If a line is completely
# occupied, its content is cleared and replaced by the line above.
# All lines above it are shifted by 1 row.


def break_lines(tetramino, grid, rows, cols):
    start_line = tetramino.get_y_pos()
    lines_to_break = 0
    for i in range(start_line, start_line + 4):
        if i < rows and i > 0:
            line = grid[i]
            if check_line(line):
                lines_to_break += 1
                for j in range(i, 1, -1):
                    # Shifting all rows above the deleted row.
                    for k in range(cols):
                        grid[j][k].occupied = grid[j - 1][k].occupied
                        grid[j][k].tetramino = grid[j - 1][k].tetramino
                        grid[j][k].color = grid[j - 1][k].color
    # returns a score. This can be reworked.
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
            if len(available_shapes) < 2:
                available_shapes = SHAPES.copy()
            tetramino = Tetramino(next_shape, 4, 0)
            next_shape = get_shape(available_shapes)
            score += new_score
            pass
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
        draw(grid, rows, cols, width, win, w_dim,
             h_dim, tetramino, score, next_shape)
        clock.tick(fps)


main(ROWS, COLS, WIDTH, WIN, BOARD_WIDTH, H_DIM)
