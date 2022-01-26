import pygame
import math
import sys
from random import *


pygame.init()
DIM = 500
WIDTH = 50
ROWS = 10
COL = 10
WIN = pygame.display.set_mode((DIM, DIM))
pygame.display.set_caption("Mine Sweeper")
font = pygame.font.SysFont('freesansbold.ttf', 75)
number_font = pygame.font.SysFont(None, 40)
NUM_MINE = 20
BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
WHITE_1 = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GRAY_1 = (175, 175, 175)
ORANGE = (250, 100, 0)


class Cell:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_marked = False
        self.width = width
        self.neighbors = 0
        self.y = row * width
        self.x = col * width

    def make_mine(self):
        self.is_mine = True

    def reveal(self, grid):
        self.is_revealed = True
        if self.neighbors == 0:
            self.reveal_neighbors(grid)

    def make_marked(self):
        self.is_marked = True

    def unmark(self):
        self.is_marked = False

    def draw(self, win):
        if self.is_revealed:
            if self.is_mine:
                pygame.draw.circle(
                    win, RED, (self.x + self.width / 2, self.y + self.width / 2), self.width * 0.3)
            else:
                msg = str(self.neighbors)
                if self.neighbors == 0:
                    msg = ''
                pygame.draw.rect(
                    win, GRAY, (self.x, self.y, self.width, self.width))
                number_image = number_font.render(msg, True, BLACK, GRAY)
                win.blit(number_image, (self.x + (self.width // 3.3),
                         self.y + (self.width // 3.3)))
        elif self.is_marked:
            msg = 'X'
            pygame.draw.rect(
                win, WHITE, (self.x, self.y, self.width, self.width))
            number_image = number_font.render(msg, True, ORANGE, WHITE)
            win.blit(number_image, (self.x + (self.width // 3.3),
                     self.y + (self.width // 3.3)))

    def check_neighbors(self, grid):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                row = self.row + i
                col = self.col + j
                if col < 0 or col > COL - 1 or row < 0 or row > ROWS - 1:
                    continue
                neighbor = grid[row][col]
                if neighbor.is_mine:
                    count += 1

        self.neighbors = count

    def reveal_neighbors(self, grid):
        for i in range(-1, 2):
            for j in range(-1, 2):
                row = self.row + i
                col = self.col + j
                if col < 0 or col > COL - 1 or row < 0 or row > ROWS - 1:
                    continue
                neighbor = grid[row][col]
                if not neighbor.is_mine and not neighbor.is_revealed:
                    neighbor.reveal(grid)


def make_grid(rows, width, num_mine):
    grid = []
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, WIDTH)
            grid[i].append(cell)

    cells = all_cells(rows)
    while count < num_mine:
        index = randrange(0, len(cells))
        i, j = cells[index]
        del cells[index]
        grid[i][j].make_mine()
        count += 1

    for i in range(rows):
        for j in range(rows):
            grid[i][j].check_neighbors(grid)

    return grid


def all_cells(rows):
    cells = []
    for i in range(rows):
        for j in range(rows):
            cells.append([i, j])
    return cells


def draw_grid(win, rows, width, dim):
    for i in range(rows):
        pygame.draw.line(win, BLACK, (i * width, 0), (i * width, dim))
        pygame.draw.line(win, BLACK, (0, i * width), (dim, i * width))


def draw(win, grid, rows, width, dim, status):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)

    if status == 'lost':
        message(win, 'You Lost !', dim)
    elif status == 'won':
        message(win, 'You Won !', dim)

    draw_grid(win, rows, width, dim)
    pygame.display.update()


def get_mouse_pos(pos, width):
    x, y = pos

    row = y // width
    col = x // width

    return row, col


def reveal_board(grid):
    for row in grid:
        for cell in row:
            cell.reveal(grid)


def message(win, text, dim):
    x = (dim / 2) - 100
    y = (dim / 2) - 30
    message = font.render(text, True, BLUE)
    win.blit(message, (x, y))


def main(win, rows, width, dim, num_mine):
    run = True
    status = ''
    grid = make_grid(rows, width, num_mine)
    mine_count = num_mine

    while run:
        draw(win, grid, rows, width, dim, status)

        if mine_count == 0:
            status = 'won'

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                i, j = get_mouse_pos(pygame.mouse.get_pos(), width)
                cell = grid[i][j]
                if cell.is_mine:
                    reveal_board(grid)
                    status = 'lost'
                else:
                    cell.reveal(grid)

            if pygame.mouse.get_pressed()[2]:
                i, j = get_mouse_pos(pygame.mouse.get_pos(), width)
                cell = grid[i][j]
                if cell.is_marked:
                    cell.unmark()
                    if cell.is_mine:
                        mine_count += 1
                else:
                    cell.make_marked()
                    if cell.is_mine:
                        mine_count -= 1

    pygame.display.quit()
    pygame.quit()
    sys.exit()


main(WIN, ROWS, WIDTH, DIM, NUM_MINE)
