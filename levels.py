import pygame as pg
from main import WIDTH, HEIGHT

from world import *

vec = pg.math.Vector2


class FirstLevel(Level):
    def __init__(self):
        layout = []  # Brick(vec(w, 40)) for w in range(32, WIDTH + 64, 40)]

        layout += [Water(vec(380, HEIGHT - 220))]

        waterfall = [Water(vec(140, h)) for h in range(0, HEIGHT - 200, 35)]

        layout += waterfall

        layout += [Lever(vec(400, HEIGHT - 460), waterfall)]

        p1 = Platform(vec(WIDTH - 80, HEIGHT - 40), 190)
        layout += [Lever(vec(900, HEIGHT - 25), p1)]
        layout += [p1]

        layout += [Brick(vec(w, HEIGHT)) for w in range(20, WIDTH + 20, 40)]

        layout += [Brick(vec(w, HEIGHT - 220)) for w in range(20, WIDTH - 140, 40)]
        layout += [BrickOverhang(vec(w, HEIGHT - 220 + 40)) for w in range(20, WIDTH - 140, 40)]

        layout += [Brick(vec(w, HEIGHT - 440)) for w in range(180, WIDTH + 20, 40)]
        layout += [BrickOverhang(vec(w, HEIGHT - 440 + 40)) for w in range(180, WIDTH + 20, 40)]

        layout += [LavaLeft(vec(460, HEIGHT - 1)), LavaMiddle(vec(500, HEIGHT - 1)), LavaRight(vec(540, HEIGHT - 1))]

        layout += [Door(vec(800, HEIGHT - 500 + 35))]

        super(FirstLevel, self).__init__(layout, vec(20, HEIGHT - 120))


class SecondLevel(Level):
    def __init__(self):
        layout = [Brick(vec(w, HEIGHT)) for w in range(20, WIDTH + 20, 40)]

        layout += [Brick(vec(w, HEIGHT - 220)) for w in range(340, WIDTH - 300, 40)]
        layout += [BrickOverhang(vec(w, HEIGHT - 220 + 40)) for w in range(340, WIDTH - 300, 40)]

        layout += [Brick(vec(w, HEIGHT - 440)) for w in range(420, WIDTH - 300, 40)]
        layout += [BrickOverhang(vec(w, HEIGHT - 440 + 40)) for w in range(420, WIDTH - 300, 40)]

        lavafall = [Lava(vec(300, h)) for h in range(HEIGHT - 215, HEIGHT + 50, 35)]
        layout += lavafall

        layout += [Lever(vec(440, HEIGHT - 245), lavafall)]

        waterfall = [Water(vec(140, h)) for h in range(0, HEIGHT - 240, 35)]
        layout += waterfall

        p1 = Platform(vec(WIDTH - 200, HEIGHT - 220), 300)

        layout += [p1]
        layout += [Lever(vec(880, HEIGHT - 465), p1)]
        layout += [Door(vec(640, HEIGHT - 500 + 35))]

        super(SecondLevel, self).__init__(layout, vec(20, HEIGHT - 120))
