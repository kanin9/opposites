import pygame as pg


def main():
    pg.init()
    pg.display.set_caption("Fireboy and Watergirl")
    screen = pg.display.set_mode((800, 640))
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


if __name__ == '__main__':
    main()
    pg.quit()
