import math
import random

import pygame as pg
from settings import *


class GameObject:
    def __init__(self, app):
        self.app = app
        self.surface = app.surface

    def update(self):
        pass

    def draw(self):
        pass

    def eventHandling(self, e):
        pass


class EndlessBackground(GameObject):
    def __init__(self, app, path, pos_y):
        super().__init__(app)

        self.bg_img = pg.image.load(path).convert_alpha()

        self.bg_w = self.bg_img.get_width()
        self.scroll_offset = 0
        self.SPEED = app.game_speed  # pixel / s
        self.tiles = math.ceil(WIDTH / self.bg_w) + 1

        self.pos_y = pos_y

    def update(self):
        self.SPEED = self.app.game_speed

        self.scroll_offset -= self.SPEED * self.app.delta_time / 1000

        if abs(self.scroll_offset) > self.bg_w:
            self.scroll_offset = 0

    def draw(self):
        for i in range(self.tiles):
            self.surface.blit(self.bg_img, (i * self.bg_w + self.scroll_offset, self.pos_y))


class SpriteAnimated(GameObject):
    def __init__(self, app, path_list: list[str], time_per_frame: float = 0.2, scale: float = 1):
        super().__init__(app)

        self.images = [
            pg.image.load(path).convert_alpha() for path in path_list
        ]

        self.num_frames = len(self.images)
        self.current_frame = 0

        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()

        self.prev_tick = 0
        self.current_tick = 0
        self.interval = time_per_frame

    def update(self):
        self.current_tick = pg.time.get_ticks()

        if self.current_tick - self.prev_tick >= self.interval * 1000:
            self.current_frame += 1
            self.current_frame %= self.num_frames

            self.prev_tick = self.current_tick
            self.image = self.images[self.current_frame]

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def getImage(self):
        return self.image

    def setPos(self, pos: tuple[int, int]):
        self.rect.topleft = pos


class Dinosaur(GameObject):
    X = 80
    Y = 420
    Y_DUCK = 450
    JUMP_SPEED = 1300  # pixel / s
    GRAVITY = 7

    def __init__(self, app):
        super().__init__(app)

        self.duck_anim = SpriteAnimated(app, DUCKING, 0.2)
        self.run_anim = SpriteAnimated(app, RUNNING, 0.2)
        self.jump_anim = SpriteAnimated(app, JUMPING, 0.2)

        self.duck = False
        self.run = True
        self.jump = False

        self.jump_v = Dinosaur.JUMP_SPEED

        self.image = self.run_anim.getImage()
        self.rect = self.image.get_rect()
        self.rect.x = Dinosaur.X
        self.rect.y = Dinosaur.Y
        self.y = Dinosaur.Y

    def update(self):
        if self.run:
            self.run_anim.update()
            self.image = self.run_anim.getImage()
            self.rect.y = Dinosaur.Y
            self.y = float(self.rect.y)

        if self.duck:
            self.duck_anim.update()
            self.image = self.duck_anim.getImage()
            self.rect.y = Dinosaur.Y_DUCK
            self.y = float(self.rect.y)

        if self.jump:
            self.jump_anim.update()
            self.image = self.jump_anim.getImage()

            self.y -= self.jump_v * self.app.delta_time / 1000
            self.jump_v -= Dinosaur.GRAVITY

            self.rect.y = int(self.y)

            if self.y >= Dinosaur.Y:
                self.jump = False
                self.jump_v = Dinosaur.JUMP_SPEED

        if self.app.user_input[pg.K_UP] and not self.jump:
            self.duck = False
            self.run = False
            self.jump = True
        elif self.app.user_input[pg.K_DOWN] and not self.jump:
            self.duck = True
            self.run = False
            self.jump = False
        elif not (self.jump or self.app.user_input[pg.K_DOWN]):
            self.duck = False
            self.run = True
            self.jump = False

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def getMask(self):
        return pg.mask.from_surface(self.image)

    def getPos(self):
        return self.rect.topleft


class Cloud(GameObject):
    def __init__(self, app):
        super().__init__(app)
        self.x = WIDTH + random.randint(0, WIDTH)
        self.y = random.randint(50, 350)

        self.image = pg.image.load(CLOUD).convert_alpha()
        self.width = self.image.get_width()

    def update(self):
        self.x -= self.app.game_speed * self.app.delta_time / 1000
        if self.x < - self.width:
            self.x = WIDTH + random.randint(2000, 3000)
            self.y = random.randint(50, 350)

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))


class Obstacle(GameObject):
    def __init__(self, app, img_path, type):
        super().__init__(app)

        self.images = [pg.image.load(path).convert_alpha() for path in img_path]
        self.type = type
        self.rect = self.images[self.type].get_rect()
        self.rect.x = WIDTH
        self.x = WIDTH  # float

    def update(self):
        self.x -= self.app.game_speed * self.app.delta_time / 1000
        self.rect.x = int(self.x)
        if self.x < - self.rect.width:
            self.app.obstacles.pop()

    def draw(self):
        self.surface.blit(self.images[self.type], self.rect)

    def getMask(self):
        return pg.mask.from_surface(self.images[self.type])

    def getPos(self):
        return self.rect.topleft


class SmallCactus(Obstacle):
    def __init__(self, app, img_path):
        self.type = random.randint(0, 2)
        super().__init__(app, img_path, self.type)

        self.rect.bottom = 500


class LargeCactus(Obstacle):
    def __init__(self, app, img_path):
        self.type = random.randint(0, 2)
        super().__init__(app, img_path, self.type)

        self.rect.bottom = 500


class Bird(Obstacle):
    def __init__(self, app, img_path):
        self.type = 0
        super().__init__(app, img_path, self.type)

        self.anim = SpriteAnimated(app, img_path, 0.2)
        self.rect.y = 375

    def update(self):
        super().update()
        self.anim.update()

    def draw(self):
        self.surface.blit(self.anim.getImage(), self.rect)

    def getMask(self):
        return pg.mask.from_surface(self.anim.getImage())
