import sys
import pygame as pg
from UI import *
from setting import *


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RESOLUTION)
        pg.display.set_caption("Menu Example")

        self.bg = pg.transform.scale(pg.image.load("bg.jpg"), (WIDTH, HEIGHT))
        self.menu = Menu(self)

    def update(self):
        self.menu.update()

    def draw(self):
        self.surface.fill(BGCOLOR)
        self.surface.blit(self.bg, (0, 0))
        self.menu.draw()

    def run(self):

        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                self.menu.eventHandling(e)

            self.update()
            self.draw()

            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
