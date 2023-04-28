import os

import pygame as pg
import pygame.sprite

main_dir = os.path.split(os.path.abspath(__file__))[0]

vec = pg.math.Vector2


def load_image(file):
    """Загружает изображение для рендеринга"""
    file = os.path.join(main_dir, file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface


class Level:
    def __init__(self, layout, spawn):
        self.start = layout
        self.layout = layout
        self.group = pg.sprite.Group()

        for obj in self.start:
            self.group.add(obj)

        self.spawn = spawn

    def reset(self, players):
        self.group = pg.sprite.Group()
        for obj in self.layout:
            obj.reset()
            self.group.add(obj)

        for p in players:
            p.rect.x = self.spawn.x
            p.rect.y = self.spawn.y
            p.acc = vec(0, 0)
            p.vel = vec(0, 0)
            p.platforms = self.group
            p.alive = True
            p.finished = False


class Block(pg.sprite.Sprite):
    def __init__(self, pos, width, height, collidable, image):
        super().__init__()
        self.activated = None
        self.sprite = image
        self.img = load_image(image)
        self.width = width
        self.height = height
        self.pos = pos
        self.collidable = collidable

        self.image = pg.transform.smoothscale(self.img, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))
        self.rect.midbottom = self.pos

    def reset(self):
        self.rect.midbottom = self.pos
        self.activated = False

    def update(self, rect, vel, acc):
        pass

    def updateSprite(self, sprite):
        if self.sprite == sprite:
            return

        self.sprite = sprite
        self.img = load_image(sprite)
        self.image = pg.transform.smoothscale(self.img, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))
        self.rect.midbottom = self.pos

    def move(self):
        pass


class Water(Block):
    def __init__(self, pos):
        super(Water, self).__init__(pos, 40, 35, False, "assets/sprites/water.jpg")
        self.activated = False

    def move(self):
        if self.activated:
            self.updateSprite("assets/sprites/Tiles_lava/lava_tile1.png")
        else:
            self.updateSprite("assets/sprites/water.jpg")


class Lava(Block):
    def __init__(self, pos):
        super(Lava, self).__init__(pos, 40, 35, False, "assets/sprites/Tiles_lava/lava_tile1.png")
        self.activated = False

    def move(self):
        if self.activated:
            self.updateSprite("assets/sprites/water.jpg")
        else:
            self.updateSprite("assets/sprites/Tiles_lava/lava_tile1.png")


class LavaMiddle(Block):
    def __init__(self, pos):
        super(LavaMiddle, self).__init__(pos, 40, 40, False, "assets/sprites/Tiles_lava/lava_tile6.png")


class LavaLeft(Block):
    def __init__(self, pos):
        super(LavaLeft, self).__init__(pos, 40, 40, False, "assets/sprites/Tiles_lava/lava_tile5.png")


class LavaRight(Block):
    def __init__(self, pos):
        super(LavaRight, self).__init__(pos, 40, 40, False, "assets/sprites/Tiles_lava/lava_tile7.png")


class Brick(Block):
    def __init__(self, pos):
        super(Brick, self).__init__(pos, 40, 32, True, "assets/sprites/Tiles_rock/tile2s.png")


class BrickOverhang(Block):
    def __init__(self, pos):
        super(BrickOverhang, self).__init__(pos, 40, 40, True, "assets/sprites/Tiles_rock/tile8.png")


class Platform(Block):
    def __init__(self, pos, range):
        super(Platform, self).__init__(pos, 120, 15, True, "assets/sprites/platform.png")
        self.activated = False
        self.range = range
        self.velocity = 1

    def move(self):
        if self.activated:
            if self.rect.bottom > self.pos.y - self.range:
                self.rect.y -= self.velocity
        else:
            if self.rect.bottom < self.pos.y:
                self.rect.y += self.velocity

    def update(self, rect, vel, acc):
        print("Collided with a platform")


class Door(Block):
    def __init__(self, pos):
        super(Door, self).__init__(pos, 80, 124, False, "assets/sprites/doorclosed.png")
        self.activated = False


class Lever(Block):
    def __init__(self, pos, link):
        super(Lever, self).__init__(pos, 88, 52, False, "assets/sprites/levers/lever_05_02.png")
        self.activated = False
        self.link = link

    def reset(self):
        self.updateSprite("assets/sprites/levers/lever_05_02.png")

    def update(self, rect, vel, acc):
        if vel.x > 7:
            self.activated = True
            if type(self.link) == list:
                for _ in self.link:
                    _.activated = True
            else:
                self.link.activated = True
            self.updateSprite("assets/sprites/levers/lever_05_03.png")
        elif vel.x < -7:
            self.updateSprite("assets/sprites/levers/lever_05_02.png")

            if type(self.link) == list:
                for _ in self.link:
                    _.activated = False
            else:
                self.link.activated = False
            self.activated = False
        print("Collided with lever")
