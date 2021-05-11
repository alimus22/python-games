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
        self.type = None

    def is_occupied(self, type):
        self.is_occupied = True
        self.type = type

    def not_occupied(self):
        self.is_occupied = False
        self.type = None


class Tetramino:

    def __init__(self, type, x, y):
        self.type = type
        self.graphs = figures[type]
        self.color = colors[type]
        self.disposition = 0
        self.x_pos = x
        self.y_pos = y

    def rotate_left(self):
        self.disposition
