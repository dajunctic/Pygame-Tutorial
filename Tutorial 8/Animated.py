import pygame as pg


class SpriteAnimated(pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, path: str, num_frames: int, time_per_frame: float = 0.2, scale: float = 1):
        super().__init__()

        self.surface = surface
        self.sprite_sheet = pg.image.load(path).convert_alpha()

        self.width = self.sprite_sheet.get_width()
        self.height = self.sprite_sheet.get_height()
        self.scale = scale

        self.num_frames = num_frames
        self.current_frame = 0

        self.images = []
        self.cutImg()

        self.prev_tick = 0  # millisecond
        self.current_tick = 0  # millisecond
        self.time_per_frame = time_per_frame  # second

        self.loop = True
        self.end = False

    def reset(self):
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.prev_tick = self.current_tick
        self.end = False
        self.loop = True

    def getRect(self):
        return self.rect

    def hasEnd(self):
        return self.end

    def setLoop(self, loop):
        self.loop = loop

    def cutImg(self):
        sprite_width = self.width // self.num_frames

        for i in range(self.num_frames):
            img_rect = pg.Rect(i * sprite_width, 0, sprite_width, self.height)

            img = self.sprite_sheet.subsurface(img_rect)
            img = pg.transform.scale(img, (self.scale * img.get_width(), self.scale * img.get_height()))

            self.images.append(img)

        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()

    def setCenterPos(self, center: tuple[int, int]):
        self.rect.center = center

    def update(self):
        if self.end:
            return

        self.current_tick = pg.time.get_ticks()

        if self.current_tick - self.prev_tick >= self.time_per_frame * 1000:
            self.current_frame += 1
            self.current_frame %= self.num_frames

            if not self.loop and self.current_frame == 0:
                self.end = True

            self.prev_tick = self.current_tick

            self.image = self.images[self.current_frame]

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def drawRect(self):
        pg.draw.rect(self.surface, (0, 255, 0), self.rect, 2)
