import sys
import pygame as pg

RESOLUTION = WIDTH, HEIGHT = 1280, 720

pg.init()
surface = pg.display.set_mode((1280, 720))
pg.display.set_caption("Menu Example")

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()


    pg.display.flip()
