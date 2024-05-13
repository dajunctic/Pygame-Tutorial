import random

import pygame as pg


def scale(img: pg.Surface, factor):
    w, h = factor * img.get_width(), factor * img.get_height()

    return pg.transform.scale(img, (w, h))


class SmokeParticle:
    def __init__(self, app, image, x, y):
        self.app = app
        self.surface = app.surface

        self.x = x
        self.y = y

        self.image = image

        self.vx = 0
        self.vy = -random.randint(100, 200)

        self.scale_img = 0.1
        self.image = scale(image, self.scale_img)
        self.scale_rate = 0.3

        self.alpha = 255
        self.alpha_rate = -100
        self.alpha_a = 1

        self.alive = True

    def update(self):
        self.x += self.vx * self.app.delta / 1000
        self.y += self.vy * self.app.delta / 1000

        self.scale_img += self.scale_rate * self.app.delta / 1000
        self.alpha += self.alpha_rate * self.app.delta / 1000
        self.alpha_rate += self.alpha_a * self.app.delta / 1000

        if self.alpha < 0:
            self.alpha = 0
            self.alive = False

        self.image = scale(self.app.img, self.scale_img)
        self.image.set_alpha(self.alpha)

    def draw(self):
        self.surface.blit(self.image, self.image.get_rect(center=(self.x, self.y)))


class SmokeEffect:
    def __init__(self, app, image, x, y, interval=0.1):
        self.app = app
        self.surface = app.surface

        self.image = image

        self.x = x
        self.y = y

        self.particles = []

        self.prev_tick = 0
        self.current_tick = 0
        self.interval = interval

    def update(self):
        self.particles = [smoke for smoke in self.particles if smoke.alive]

        self.current_tick = pg.time.get_ticks()
        if self.current_tick - self.prev_tick >= self.interval * 1000:
            self.particles.append(SmokeParticle(self.app, self.image, self.x, self.y))
            self.prev_tick = self.current_tick

        for smoke in self.particles:
            smoke.update()

        print(len(self.particles))

    def draw(self):
        for smoke in self.particles:
            smoke.draw()

    def setPos(self, center:tuple[int, int]):
        self.x, self.y = center

