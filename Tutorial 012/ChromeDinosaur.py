import math
import sys
import pygame as pg
from Settings import *
from GameObject import *


class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.user_input = None

        self.game_speed = 300

        self.bg = EndlessBackground(self, BG, 490)
        self.dinosaur = Dinosaur(self)
        self.clouds = [Cloud(self) for _ in range(3)]

        self.obstacles = []

        self.death = False

    def update(self):
        if self.death:
            return

        self.bg.update()
        self.dinosaur.update()
        for cloud in self.clouds:
            cloud.update()

        if len(self.obstacles) == 0:
            rand_obs = random.randint(0, 2)

            if rand_obs == 0:
                self.obstacles.append(SmallCactus(self, SMALL_CACTUS))
            elif rand_obs == 1:
                self.obstacles.append(LargeCactus(self, LARGE_CACTUS))
            elif rand_obs == 2:
                self.obstacles.append(Bird(self, BIRD))

        dino_x, dino_y = self.dinosaur.getPos()

        for obstacle in self.obstacles:
            obstacle.update()

            obs_x, obs_y = obstacle.getPos()

            offset_x = obs_x - dino_x
            offset_y = obs_y - dino_y

            if self.dinosaur.getMask().overlap(obstacle.getMask(), (offset_x, offset_y)):
                self.death = True

    def draw(self):
        self.surface.fill("#ffffff")
        self.bg.draw()

        for cloud in self.clouds:
            cloud.draw()

        for obstacle in self.obstacles:
            obstacle.draw()

        self.dinosaur.draw()

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.user_input = pg.key.get_pressed()

            self.update()
            self.draw()

            self.delta_time = self.clock.tick()
            pg.display.set_caption("Chrome Dinosaur - FPS: " + str(round(self.clock.get_fps(), 2)))
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
