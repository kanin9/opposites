import pygame as pg
import pygame.sprite
from pygame.locals import *

import firstlevel
import world
from world import Block, load_image, Brick

WIDTH = 1280
HEIGHT = 640
FPS = 60
ACC = 1

FRICX = -0.12
FRICY = -0.12

GRAVITY = -0.7

FramePerSec = pg.time.Clock()
vec = pygame.math.Vector2


class Button:
    def __init__(self, pos, font, text, color, hovercolor):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.input = text
        self.font = font
        self.text = self.font.render(self.input, True, color)
        self.image = self.text
        self.color = color
        self.hovercolor = hovercolor
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def changeColor(self, mouse):
        if mouse[0] in range(self.rect.left, self.rect.right) and mouse[1] in range(self.rect.top,
                                                                                    self.rect.bottom):
            self.text = self.font.render(self.input, True, self.hovercolor)
        else:
            self.text = self.font.render(self.input, True, self.color)

    def clickEvent(self, mouse):
        if mouse[0] in range(self.rect.left, self.rect.right) and mouse[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False


vmin = 9999
vmax = -9999


class Player(pg.sprite.Sprite):
    def __init__(self, image, identity):
        super().__init__()

        self.identity = identity
        self.img = load_image(image)
        self.width = 50
        self.height = 75
        self.gravity = GRAVITY
        self.grounded = False
        self.platforms = None
        self.alive = True

        # self.surface = pg.Surface((80, 80))
        # self.surface.fill((128, 255, 40))

        self.image = pg.transform.smoothscale(self.img, (self.width, self.height))

        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))

        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT

    def move(self, bindings, events):
        self.acc = vec(0, 0)
        pressed = pg.key.get_pressed()

        kleft, kright, kdown, kup = bindings

        if pressed[kleft]:
            self.acc.x = -ACC
        if pressed[kright]:
            self.acc.x = ACC
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == kup and self.grounded:
                    self.vel.y += -30
                    self.grounded = False

        self.acc.x += self.vel.x * FRICX
        self.acc.y += self.vel.y * FRICY
        self.acc.y -= self.gravity

        self.vel.x += self.acc.x
        self.vel.y += self.acc.y

        self.rect.x += self.vel.x + self.acc.x * 0.5

        if self.platforms is not None:
            hits = pg.sprite.spritecollide(self, self.platforms, False)
            for obj in hits:
                if type(obj) is world.Water and self.identity == "fireboy":
                    self.alive = False

                obj.update(self.rect, self.vel)

                if not obj.collidable:
                    continue

                if type(obj) is world.Platform:
                    continue

                if self.vel.x > 0:
                    self.vel.x = 0
                    self.rect.right = obj.rect.left
                elif self.vel.x < 0:
                    self.vel.x = 0
                    self.rect.left = obj.rect.right

        self.rect.y += self.vel.y + self.acc.y * 0.5

        if self.platforms is not None:
            hits = pg.sprite.spritecollide(self, self.platforms, False)
            if hits:
                for obj in hits:
                    if type(obj) is world.Water and self.identity == "fireboy":
                        self.alive = False

                    obj.update(self.rect, self.vel)

                    if not obj.collidable:
                        continue

                    if self.vel.y > 0:
                        self.vel.y = 0
                        self.rect.bottom = obj.rect.top
                        self.grounded = True
                    elif self.vel.y < 0:
                        self.vel.y = 0
                        self.rect.top = obj.rect.bottom

        if self.rect.x > WIDTH - self.width:
            self.rect.x = WIDTH - self.width
        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.y > HEIGHT - self.height:
            self.rect.y = HEIGHT - self.height
            self.grounded = True
        if self.rect.y < 0:
            self.rect.y = 0

        # print(self.rect.x, self.rect.y)


def main():
    pg.init()
    pg.display.set_caption("Fireboy and Watergirl")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    running = True

    # level0 = pg.sprite.Group()
    # for block in firstlevel.layout:
    #    level0.add(block)

    level0 = firstlevel.FirstLevel()

    fireboy = Player("assets/sprites/fireboy.png", "fireboy")
    watergirl = Player("assets/sprites/watergirl.png", "watergirl")

    objects = pg.sprite.Group()
    players = pg.sprite.Group()
    players.add(fireboy)
    players.add(watergirl)

    bg = load_image("assets/sprites/bg.jpg")

    PLAY_BUTTON = Button(pos=(640, 360), text="Играть", color="Yellow", font=pygame.font.Font('assets/font.ttf', 32),
                         hovercolor="Black")

    PLAY_TEXT = pygame.font.Font('assets/font.ttf', 42).render("Противоположности", True, "Yellow")
    PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))

    currentscreen = "main"

    LEVEL0 = Button(pos=(640, 260), text="Первый уровень", color="Yellow", font=pygame.font.Font('assets/font.ttf', 32),
                    hovercolor="Black")
    LEVEL1 = Button(pos=(640, 360), text="Второй уровень", color="Yellow", font=pygame.font.Font('assets/font.ttf', 32),
                    hovercolor="Black")

    while running:
        events = []

        mousepos = pg.mouse.get_pos()

        for event in pg.event.get():
            events.append(event)
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    level0.reset([fireboy, watergirl])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if currentscreen == "main":
                    if PLAY_BUTTON.clickEvent(mousepos):
                        PLAY_BUTTON.color = "BLACK"
                        currentscreen = "select"
                elif currentscreen == "select":
                    if LEVEL0.clickEvent(mousepos):
                        currentscreen = "level0"
                        for obj in level0.start:
                            objects.add(obj)
                        level0.reset([fireboy, watergirl])

                    elif LEVEL1.clickEvent(mousepos):
                        currentscreen = "level1"

        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        if currentscreen == "main":
            screen.blit(PLAY_TEXT, PLAY_RECT)
            PLAY_BUTTON.changeColor(mousepos)
            screen.blit(PLAY_BUTTON.text, PLAY_BUTTON.text_rect)
        elif currentscreen == "select":
            screen.blit(LEVEL0.text, LEVEL0.text_rect)
            LEVEL0.changeColor(mousepos)
            screen.blit(LEVEL1.text, LEVEL1.text_rect)
            LEVEL1.changeColor(mousepos)

        if not fireboy.alive or not watergirl.alive:
            level0.reset([fireboy, watergirl])

        else:
            fireboy.move((K_LEFT, K_RIGHT, K_DOWN, K_UP), events)
            watergirl.move((K_a, K_d, K_s, K_w), events)

        for obj in level0.layout:
            obj.move()

        objects.draw(screen)
        players.draw(screen)

        pg.display.update()
        FramePerSec.tick(FPS)


if __name__ == '__main__':
    main()
    pg.quit()
