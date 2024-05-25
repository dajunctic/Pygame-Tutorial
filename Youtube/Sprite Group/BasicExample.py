import pygame as pg
import sys, random
RES = WIDTH, HEIGHT = 1280, 720
ASTEROID_IMG = []

def load_cache():
    spritesheet = pg.image.load("Asteroids.png").convert_alpha()
    w = spritesheet.get_width()
    h = spritesheet.get_height()
    sprite_w = w // 3
    sprite_h = h // 3

    for i in range(3):
        for j in range(3):
            sprite_x = i * sprite_w
            sprite_y = j * sprite_h

            ASTEROID_IMG.append(spritesheet.subsurface((sprite_x, sprite_y, sprite_w, sprite_h)))

class Obstacle:
    def __init__(self, app):
        self.app = app
        self.surface = app.surface

        self.type = random.randint(0, 8)
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(-400, -100)
        self.vx = random.randint(-50, 50)
        self.vy = random.randint(100, 200)

    def draw(self):
        self.surface.blit(ASTEROID_IMG[self.type], (int(self.x), int(self.y)))

    def update(self):
        self.x += self.vx * self.app.delta_time
        self.y += self.vy * self.app.delta_time


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 0
        load_cache()

        self.bg = pg.transform.scale(pg.image.load('bg.png').convert_alpha(), (WIDTH, HEIGHT))
        self.obstacles = [
            Obstacle(self) for _ in range(5)
        ]

        self.prev_tick = 0
        self.current_tick = 0
        self.interval = 1

    def update(self):
        self.current_tick = pg.time.get_ticks()
        if self.current_tick - self.prev_tick >= self.interval * 1000:
            self.obstacles.append(Obstacle(self))
            self.prev_tick = self.current_tick

        for obs in self.obstacles:
            obs.update()

            if obs.y > 720:
                self.obstacles.remove(obs)

    def draw(self):
        self.surface.blit(self.bg, (0, 0))
        for obs in self.obstacles:
            obs.draw()

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.update()
            self.draw()

            self.delta_time = self.clock.tick() / 1000  # second
            pg.display.set_caption("Sprite Group Example: " + str(round(self.clock.get_fps())))
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
