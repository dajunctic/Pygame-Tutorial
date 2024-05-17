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

        self.DEFAULT_SPEED = 300
        self.game_speed = self.DEFAULT_SPEED

        self.bg = EndlessBackground(self, BG, 490)
        self.dinosaur = Dinosaur(self)
        self.clouds = [Cloud(self) for _ in range(3)]

        self.obstacles = []

        self.death = False

        self.point = 0
        self.score = 0
        self.highscore = 0

        self.font = pg.Font("Assets/Fonts/PressStart2P-Regular.ttf")
        self.hi_text = self.font.render("HI", True, GRAY)
        self.hi_rect = self.hi_text.get_rect()
        self.hi_rect.center = (900, 50)

        self.game_over_img = pg.image.load("Assets/Other/GameOver.png").convert_alpha()
        self.game_over_rect = self.game_over_img.get_rect()
        self.game_over_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)

        self.reset_img = pg.image.load("Assets/Other/Reset.png").convert_alpha()
        self.reset_rect = self.reset_img.get_rect()
        self.reset_rect.center = (WIDTH // 2, HEIGHT // 2)

        self.space_text = self.font.render("SPACE TO PLAY AGAIN", True, GRAY)
        self.space_rect = self.space_text.get_rect()
        self.space_rect.center = (WIDTH // 2, HEIGHT - 50)

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
        self.surface.fill(WHITE)
        self.bg.draw()

        for cloud in self.clouds:
            cloud.draw()

        for obstacle in self.obstacles:
            obstacle.draw()

        self.dinosaur.draw()

        if self.death:
            self.surface.blit(self.game_over_img, self.game_over_rect)
            self.surface.blit(self.reset_img, self.reset_rect)
            self.surface.blit(self.space_text, self.space_rect)

    def calculateScore(self):
        if not self.death:
            self.point += 10 * self.delta_time / 1000
            self.score = int(self.point)
            if self.score % 100 == 0:
                self.game_speed += 2

            self.highscore = max(self.highscore, self.score)

        highscore_text = str(self.highscore).zfill(5)
        highscore_surf = self.font.render(highscore_text, True, GRAY)
        highscore_rect = highscore_surf.get_rect()
        highscore_rect.center = (1000, 50)

        score_text = str(self.score).zfill(5)
        score_surf = self.font.render(score_text, True, GRAY)
        score_rect = score_surf.get_rect()
        score_rect.center = (1200, 50)

        self.surface.blit(self.hi_text, self.hi_rect)
        self.surface.blit(highscore_surf, highscore_rect)
        self.surface.blit(score_surf, score_rect)

    def reset(self):
        self.point = 0
        self.obstacles.clear()
        self.game_speed = self.DEFAULT_SPEED

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.user_input = pg.key.get_pressed()

            self.update()
            self.draw()
            self.calculateScore()

            if self.death:
                if self.user_input[pg.K_SPACE]:
                    self.death = False
                    self.reset()

            self.delta_time = self.clock.tick()
            pg.display.set_caption("Chrome Dinosaur - FPS: " + str(round(self.clock.get_fps(), 2)))
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
