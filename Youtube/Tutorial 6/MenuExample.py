import sys
import pygame as pg
from UI import Button

RESOLUTION = WIDTH, HEIGHT = 1280, 720

pg.init()
surface = pg.display.set_mode((1280, 720))
pg.display.set_caption("Menu Example")

BGCOLOR = "#1B1F66"

buttons = [
    Button(surface, (WIDTH // 2, 200), "START"),
    Button(surface, (WIDTH // 2, 350), "OPTIONS"),
    Button(surface, (WIDTH // 2, 500), "QUIT"),
]


def update():
    for button in buttons:
        button.update()


def draw():
    surface.fill(BGCOLOR)

    for button in buttons:
        button.draw()


while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if e.type == pg.MOUSEBUTTONDOWN:
            pass

    update()
    draw()

    pg.display.flip()
