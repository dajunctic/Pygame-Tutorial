import math

import pygame as pg
import sys

RES = WIDTH, HEIGHT = 1280, 720


class EndlessBackground:
    def __init__(self, app, path):
        self.app = app
        self.surface = app.surface

        self.bg_img = pg.image.load(path).convert_alpha()

        self.bg_w = self.bg_img.get_width()
        self.scroll_offset = 0
        self.SPEED = 200  # pixel / s
        self.tiles = math.ceil(WIDTH / self.bg_w) + 1

    def update(self):
        self.scroll_offset -= self.SPEED * self.app.delta_time / 1000

        if abs(self.scroll_offset) > self.bg_w:
            self.scroll_offset = 0

    def draw(self):
        for i in range(self.tiles):
            self.surface.blit(self.bg_img, (i * self.bg_w + self.scroll_offset, 0))


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RES)
        pg.display.set_caption("Endless Background")
        self.clock = pg.time.Clock()
        self.delta_time = 0

        self.endless_bg = EndlessBackground(self, "bg.png")

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)

            self.update()
            self.draw()

            self.delta_time = self.clock.tick()
            pg.display.set_caption("Endless Background: " + str(round(self.clock.get_fps())))
            pg.display.flip()

    def update(self):
        self.endless_bg.update()

    def draw(self):
        self.endless_bg.draw()


if __name__ == '__main__':
    app = App()
    app.run()
