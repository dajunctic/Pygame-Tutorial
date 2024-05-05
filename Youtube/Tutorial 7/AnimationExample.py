import sys
import pygame as pg
from Animated import SpriteAnimated

RESOLUTION = WIDTH, HEIGHT = 1280, 720

pg.init()
surface = pg.display.set_mode((1280, 720))
pg.display.set_caption("Animation Example")
clock = pg.time.Clock()

kunoichi_idle = SpriteAnimated(surface, "Kunoichi/Idle.png", 9, time_per_frame=0.1, scale=2)
kunoichi_idle.setCenterPos((WIDTH // 4, HEIGHT // 2))

kunoichi_run = SpriteAnimated(surface, "Kunoichi/Run.png", 8, time_per_frame=0.1, scale=2)
kunoichi_run.setCenterPos((WIDTH // 2, HEIGHT // 2))

kunoichi_attack = SpriteAnimated(surface, "Kunoichi/Attack_2.png", 8, time_per_frame=0.1, scale=2)
kunoichi_attack.setCenterPos((WIDTH // 4 * 3, HEIGHT // 2))

def update():
    kunoichi_idle.update()
    kunoichi_run.update()
    kunoichi_attack.update()

def draw():
    surface.fill("#b8b4b4")

    kunoichi_idle.draw()
    kunoichi_run.draw()
    kunoichi_attack.draw()


while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

    update()
    draw()

    delta_time = clock.tick()
    pg.display.set_caption("Animation Example: " + str(round(clock.get_fps(), 2)))

    pg.display.flip()
