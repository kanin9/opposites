import json

import pygame as pg
import pygame.sprite
from pygame.locals import *

import os
import levels
import world
from world import Block, load_image, Brick

main_dir = os.path.split(os.path.abspath(__file__))[0]

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

    def changeColor(self, mouse, color, hovercolor):
        if mouse[0] in range(self.rect.left, self.rect.right) and mouse[1] in range(self.rect.top,
                                                                                    self.rect.bottom):
            self.text = self.font.render(self.input, True, hovercolor)
        else:
            self.text = self.font.render(self.input, True, color)

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
        self.finished = False

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
                if type(obj) is world.Water and not obj.activated and self.identity == "fireboy":
                    self.alive = False

                if type(obj) is world.Water and not obj.activated and self.identity == "watergirl":
                    self.grounded = True

                if type(obj) is world.Water and obj.activated and self.identity == "fireboy":
                    self.grounded = True

                if type(obj) is world.LavaMiddle and self.identity == "watergirl":
                    self.alive = False

                if type(obj) is world.Door:
                    self.finished = True

                obj.update(self.rect, self.vel, self.acc, self.platforms, self)

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
                    if type(obj) is world.Water and not obj.activated and self.identity == "fireboy":
                        self.alive = False

                    if type(obj) is world.Water and not obj.activated and self.identity == "watergirl":
                        self.grounded = True

                    if type(obj) is world.Water and obj.activated and self.identity == "fireboy":
                        self.grounded = True

                    if type(obj) is world.Lava:
                        if not obj.activated:
                            if self.identity == "fireboy":
                                self.grounded = True
                            else:
                                self.alive = False
                        else:
                            if self.identity == "fireboy":
                                self.alive = False
                            else:
                                self.grounded = True

                    if type(obj) is world.LavaMiddle and self.identity == "watergirl":
                        self.alive = False

                    obj.update(self.rect, self.vel, self.acc, self.platforms, self)

                    if type(obj) is world.Door:
                        self.finished = True

                    if not obj.collidable:
                        continue

                    if self.vel.y > 0:
                        self.rect.bottom = obj.rect.top
                        self.grounded = True
                        self.vel.y = 0

                        if type(obj) is world.Platform:
                            self.vel.y = -1


                    elif self.vel.y < 0:
                        self.vel.y = 0
                        self.rect.top = obj.rect.bottom
        else:
            self.gravity = -1

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


def pause(screen):
    paused = True

    message = pygame.font.Font('assets/font.ttf', 32).render("Нажмите 'C' чтобы продолжить", True, "Yellow")
    messageRect = message.get_rect(center=(640, 320))

    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    paused = False

        screen.fill((0, 0, 0))
        screen.blit(message, messageRect)

        pg.display.update()


def exit(screen):
    paused = True

    message = pygame.font.Font('assets/font.ttf', 22).render("Ваша игра сохранена, нажмите Q чтобы выйти", True,
                                                             "Yellow")
    messageRect = message.get_rect(center=(640, 260))

    messageS = pygame.font.Font('assets/font.ttf', 22).render("Или нажмите C чтобы вернуться к игре", True,
                                                              "Yellow")
    messageSRect = message.get_rect(center=(690, 360))

    running = False

    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    paused = False
                if event.key == pg.K_c:
                    paused = False
                    running = True

        screen.fill((0, 0, 0))
        screen.blit(message, messageRect)
        screen.blit(messageS, messageSRect)

        pg.display.update()

    return running


def main(save):
    pg.init()
    pg.display.set_caption("Fireboy and Watergirl")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    running = True

    level0 = levels.FirstLevel()
    level1 = levels.SecondLevel()

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

    CONGRATS_TEXT = pygame.font.Font('assets/font.ttf', 42).render("Уровень пройден", True, "Yellow")
    CONGRATS_RECT = CONGRATS_TEXT.get_rect(center=(640, 260))
    NEXTLEVELBUTTON = Button(pos=(640, 360), text="Продолжить", color="Yellow",
                             font=pygame.font.Font('assets/font.ttf', 32),
                             hovercolor="Black")

    currentscreen = "main"

    LEVEL0 = Button(pos=(640, 260), text="Первый уровень", color="Yellow", font=pygame.font.Font('assets/font.ttf', 32),
                    hovercolor="Black")
    LEVEL1 = Button(pos=(640, 360), text="Второй уровень", color="Yellow", font=pygame.font.Font('assets/font.ttf', 32),
                    hovercolor="Black")

    currentlevel = None

    while running:
        events = []

        mousepos = pg.mouse.get_pos()

        for event in pg.event.get():
            events.append(event)
            if event.type == pg.QUIT:
                exit(screen)
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    currentlevel.reset([fireboy, watergirl])
                if event.key == pg.K_ESCAPE:
                    if currentscreen != "main" and currentscreen != "select":
                        pause(screen)
                if event.key == pg.K_q:
                    running = exit(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if currentscreen == "main":
                    if PLAY_BUTTON.clickEvent(mousepos):
                        currentscreen = "select"
                elif currentscreen == "select":
                    if LEVEL0.clickEvent(mousepos) and save['level0']:
                        currentscreen = "level0"
                        for obj in level0.start:
                            objects.add(obj)
                        level0.reset([fireboy, watergirl])
                        currentlevel = level0

                    elif LEVEL1.clickEvent(mousepos) and save['level1']:
                        currentscreen = "level1"
                        objects = pg.sprite.Group()
                        for obj in level1.start:
                            objects.add(obj)
                        level1.reset([fireboy, watergirl])
                        currentlevel = level1
                elif currentscreen == "level0":
                    if NEXTLEVELBUTTON.clickEvent(mousepos) and (watergirl.finished and fireboy.finished):
                        currentscreen = "level1"
                        save['level1'] = True
                        objects = pg.sprite.Group()
                        for obj in level1.start:
                            objects.add(obj)
                        level1.reset([fireboy, watergirl])
                        currentlevel = level1
                elif currentscreen == "level1" and (watergirl.finished and fireboy.finished):
                    if NEXTLEVELBUTTON.clickEvent(mousepos):
                        currentscreen = "main"
                        objects = pg.sprite.Group()
                        for p in players:
                            p.rect.x = WIDTH // 2
                            p.rect.y = HEIGHT
                            p.acc = vec(0, 0)
                            p.vel = vec(0, 0)
                            p.platforms = None
                            p.alive = True
                            p.finished = False

        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        disabled = (60, 60, 60)

        if currentscreen == "main":
            screen.blit(PLAY_TEXT, PLAY_RECT)
            PLAY_BUTTON.changeColor(mousepos, "YELLOW", "BLACK")
            screen.blit(PLAY_BUTTON.text, PLAY_BUTTON.text_rect)
        elif currentscreen == "select":
            LEVEL0.changeColor(mousepos, "YELLOW", "BLACK")
            if save['level1']:
                LEVEL1.changeColor(mousepos, "YELLOW", "BLACK")
            else:
                LEVEL1.changeColor(mousepos, disabled, disabled)
            screen.blit(LEVEL0.text, LEVEL0.text_rect)
            screen.blit(LEVEL1.text, LEVEL1.text_rect)

        if currentlevel is not None:
            for obj in currentlevel.layout:
                obj.move()

        objects.draw(screen)
        players.draw(screen)

        if not fireboy.alive or not watergirl.alive:
            currentlevel.reset([fireboy, watergirl])
        else:
            if watergirl.finished and fireboy.finished:
                screen.blit(CONGRATS_TEXT, CONGRATS_RECT)
                screen.blit(NEXTLEVELBUTTON.text, NEXTLEVELBUTTON.text_rect)
                NEXTLEVELBUTTON.changeColor(mousepos, "YELLOW", "BLACK")
            else:
                fireboy.move((K_LEFT, K_RIGHT, K_DOWN, K_UP), events)
                watergirl.move((K_a, K_d, K_s, K_w), events)

        pg.display.update()
        FramePerSec.tick(FPS)


if __name__ == '__main__':
    save = {
        'level0': True,
        'level1': False
    }

    try:
        with open('save.json', 'r') as f:
            save = json.loads(f.read())
    except FileNotFoundError as e:
        print(e)

    main(save)

    with open('save.json', 'w') as f:
        f.write(json.dumps(save))

    pg.quit()
