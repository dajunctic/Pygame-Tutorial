import random

import pygame as pg
import sys

RES = WIDTH, HEIGHT = 1280, 720


class Particle:
    def __init__(self, app, pos: tuple[int, int], velocity: tuple[int, int], radius):
        self.app = app
        self.surface = app.surface

        self.x, self.y = pos

        self.vx, self.vy = velocity
        self.radius = radius
        self.gravity = 0.5
        self.radius_rate = 2

        self.alive = True

    def update(self):
        self.x += self.vx * self.app.delta_time / 1000  # vx pixel / s
        self.y += self.vy * self.app.delta_time / 1000  # vy pixel / s

        self.vy += self.gravity

        self.radius -= self.radius_rate * self.app.delta_time / 1000

        if self.radius < 0:
            self.radius = 0
            self.alive = False

    def draw(self):
        pg.draw.circle(self.surface, "#ffffff", (self.x, self.y), self.radius)


class ParticleEffect:
    def __init__(self, app, pos: tuple[int, int], interval=0.1):
        self.app = app
        self.surface = app.surface

        self.x, self.y = pos

        self.particles = []

        self.prev_tick = 0
        self.current_tick = 0
        self.interval = interval

    def make_particle(self):
        vx = random.randint(-40, 40)
        vy = -100

        r = random.randint(6, 9)

        self.particles.append(Particle(self.app, (self.x, self.y), (vx, vy), r))

    def update(self):
        self.current_tick = pg.time.get_ticks()

        if self.current_tick - self.prev_tick >= self.interval * 1000:
            self.make_particle()

        self.particles = [particle for particle in self.particles if particle.alive]
        for particle in self.particles:
            particle.update()

    def draw(self):
        for particle in self.particles:
            particle.draw()

    def setPos(self, pos: tuple[int, int]):
        self.x, self.y = pos


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RES)
        pg.display.set_caption("Particle Effect Example")
        self.clock = pg.time.Clock()
        self.delta_time = 0

        self.particle_effect = ParticleEffect(self, (WIDTH // 2, HEIGHT // 2), 0.1)

    def update(self):
        mx, my = pg.mouse.get_pos()

        self.particle_effect.setPos((mx, my))
        self.particle_effect.update()

    def draw(self):
        self.surface.fill("#000000")

        self.particle_effect.draw()

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.update()
            self.draw()

            self.delta_time = self.clock.tick()
            pg.display.set_caption("Particle Effect Example: " + str(round(self.clock.get_fps())))
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
