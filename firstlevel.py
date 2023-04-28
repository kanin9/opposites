import pygame as pg
from main import WIDTH, HEIGHT

from world import *

vec = pg.math.Vector2


class FirstLevel(Level):
    def __init__(self):
        layout = [Brick(vec(w, 40)) for w in range(20, WIDTH + 20, 40)]
        layout += [Brick(vec(w, HEIGHT)) for w in range(20, WIDTH + 20, 40)]
        layout += [Water(vec(340, HEIGHT - 40))]

        layout += [Brick(vec(w, HEIGHT - 200)) for w in range(20, WIDTH - 100, 40)]
        p1 = Platform(vec(WIDTH - 60, HEIGHT - 30), 200)
        layout += [Lever(vec(900, HEIGHT - 40), p1)]
        layout += [p1]
        layout += [Door(vec(500, HEIGHT - 235))]

        super(FirstLevel, self).__init__(layout, vec(20, HEIGHT - 120))