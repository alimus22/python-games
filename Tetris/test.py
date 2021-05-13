from random import *

SHAPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']


def get_shape(available_shapes):
    print(available_shapes)
    ran_num = randrange(0, len(available_shapes))
    return available_shapes.pop(ran_num)


def shapes():
    available_shapes = SHAPES.copy()
    for i in range(100):
        if len(available_shapes) < 2:
            available_shapes = SHAPES.copy()
        print(get_shape(available_shapes))


shapes()
