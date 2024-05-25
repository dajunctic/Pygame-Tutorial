import pygame as pg
import sys
RES = WIDTH, HEIGHT = 1280, 720


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RES)
        pg.display.set_caption("Mask Example")
        self.clock = pg.time.Clock()
        self.delta_time = 0

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.delta_time = self.clock.tick()
            pg.display.set_caption("Particle Effect Example: " + str(round(self.clock.get_fps())))
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
