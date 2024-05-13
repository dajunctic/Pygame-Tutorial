import sys

import pygame as pg

pg.init()
pg.font.init()
pg.mixer.init()

surface = pg.display.set_mode((1280, 720))
pg.mixer.music.load("Music Background/8-bit-legends-ancient-shrine.mp3")
pg.mixer.music.set_volume(0.5)
# pg.mixer.music.play()

level_up = pg.mixer.Sound("Sound Effect/level-up.mp3")
level_up.set_volume(0.5)  # value from 0 to 1

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit(0)

        if e.type == pg.KEYDOWN:
            if e.key == pg.K_SPACE:
                level_up.play()

    pg.display.flip()
