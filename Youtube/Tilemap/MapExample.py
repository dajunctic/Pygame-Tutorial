import pygame as pg
import sys
from pytmx.util_pygame import load_pygame

RES = WIDTH, HEIGHT = 1280, 800

class Tile(pg.sprite.Sprite):
    def __init__(self, image, pos, *group):
        super().__init__(*group)
        self.image = pg.transform.scale(image, (32, 32))
        self.rect = self.image.get_rect(topleft=pos)

class App:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(RES)
        pg.display.set_caption("Map Example")
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.map_data = load_pygame("map.tmx")
        self.sprite_group = pg.sprite.Group()

        for layer in self.map_data.visible_layers:
            for x, y, surf in layer.tiles():
                pos = (x * 32, y * 32)

                Tile(surf, pos, self.sprite_group)

    def draw(self):
        self.sprite_group.draw(self.surface)


    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.draw()

            self.delta_time = self.clock.tick()
            pg.display.set_caption("Map Example: " + str(round(self.clock.get_fps())))
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
