import pygame as pg
import sys
from Smoke import *

RES = WIDTH, HEIGHT = 1280, 720


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RES)
        pg.display.set_caption("Smoke Effect Example")
        self.clock = pg.time.Clock()
        self.delta = 0

        self.img = pg.image.load("smoke.png").convert_alpha()

        self.smoke_effect = SmokeEffect(self, self.img, WIDTH // 2, HEIGHT // 2, interval=0.05)

    def update(self):
        mx, my = pg.mouse.get_pos()

        self.smoke_effect.setPos((mx, my))
        self.smoke_effect.update()

    def draw(self):
        self.surface.fill("#282d2e")
        self.smoke_effect.draw()

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)

            self.update()
            self.draw()

            self.delta = self.clock.tick()
            pg.display.set_caption("Smoke Effect Example: " + str(round(self.clock.get_fps(), 2)))
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
