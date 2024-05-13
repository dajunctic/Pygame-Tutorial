import sys
import pygame as pg
from UI import *
from setting import *


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RESOLUTION)
        pg.display.set_caption("Menu Example")

        self.menu = Menu(self)

    def update(self):
        pass

    def draw(self):
        self.surface.fill(BGCOLOR)

    def run(self):

        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if e.type == pg.MOUSEBUTTONDOWN:
                    pass

            self.update()
            self.draw()

            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
