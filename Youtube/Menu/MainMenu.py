import sys
import pygame as pg

from UI import *
from setings import *


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode((1280, 720))
        pg.display.set_caption("Menu")
        self.user_input = None
        self.mouse_input = None

        self.bg = pg.transform.scale(pg.image.load(BG_IMG).convert_alpha(), (WIDTH, HEIGHT))
        self.menu = Menu(self)

    def update(self):
        self.menu.update()

    def draw(self):
        self.surface.blit(self.bg, (0, 0))
        self.menu.draw()

    def run(self):

        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                self.menu.eventHandling(e)

            self.user_input = pg.key.get_pressed()
            self.mouse_input = pg.mouse.get_pressed()  # 0 - mouse left, 1 - mouse middle, 2 - mouse right

            self.update()
            self.draw()

            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
