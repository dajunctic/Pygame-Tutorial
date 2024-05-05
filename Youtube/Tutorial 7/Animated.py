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
        self.cut_img()

        self.prev_tick = 0  # millisecond
        self.current_tick = 0  # millisecond
        self.time_per_frame = time_per_frame  # second

    def cut_img(self):
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
        self.current_tick = pg.time.get_ticks()

        if self.current_tick - self.prev_tick >= self.time_per_frame * 1000:
            self.current_frame += 1
            self.current_frame %= self.num_frames

            self.prev_tick = self.current_tick

            self.image = self.images[self.current_frame]

    def draw(self):
        self.surface.blit(self.image, self.rect)
