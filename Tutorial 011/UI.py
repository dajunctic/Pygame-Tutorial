import pygame as pg
from setting import *

pg.font.init()


class Menu:
    HOME = 'home'
    OPTIONS = 'options'

    def __init__(self, app):
        self.app = app
        self.surface = app.surface

        self.scene = Menu.HOME

        self.home_buttons = [
            Button(self.app, (WIDTH // 2, 200), "START"),
            Button(self.app, (WIDTH // 2, 350), "OPTIONS"),
            Button(self.app, (WIDTH // 2, 500), "QUIT"),
        ]

    def update(self):
        if self.scene == Menu.HOME:
            for button in self.home_buttons:
                button.update()

        elif self.scene == Menu.OPTIONS:
            pass

    def draw(self):
        if self.scene == Menu.HOME:
            for button in self.home_buttons:
                button.draw()

        elif self.scene == Menu.OPTIONS:
            pass


class Button:
    FONT = [
        pg.font.Font("fonts/MightySouly-lxggD.ttf", 60),
        pg.font.Font("fonts/MightySouly-lxggD.ttf", 65),
    ]
    COLOR = "#27E7C9"

    def __init__(self, app, center: tuple[int, int], text: str):
        self.surface = app.surface

        self.w = 300
        self.h = 80
        self.x = center[0] - self.w // 2
        self.y = center[1] - self.h // 2

        self.hover_active = False

        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.hover_rect = pg.Rect(self.x - 5, self.y - 5, self.w + 10, self.h + 10)

        self.text_surf = self.FONT[0].render(text, True, self.COLOR)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = center

        self.hover_text_surf = self.FONT[1].render(text, True, self.COLOR)
        self.hover_text_rect = self.hover_text_surf.get_rect()
        self.hover_text_rect.center = center

    def update(self):
        x, y = pg.mouse.get_pos()

        if self.rect.collidepoint(x, y):
            self.hover_active = True
        else:
            self.hover_active = False

    def draw(self):
        if self.hover_active:
            pg.draw.rect(self.surface, self.COLOR, self.hover_rect, 2, 20)
            self.surface.blit(self.hover_text_surf, self.hover_text_rect)
        else:
            pg.draw.rect(self.surface, self.COLOR, self.rect, 2, 20)
            self.surface.blit(self.text_surf, self.text_rect)
