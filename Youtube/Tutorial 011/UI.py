import sys

import pygame as pg
from setting import *

pg.font.init()

COLOR = "#ffffff"


class UIComponent:
    def __init__(self, app):
        self.surface = app.surface

    def update(self):
        pass

    def draw(self):
        pass

    def eventHandling(self, e):
        pass


class Menu:
    HOME = 'home'
    OPTIONS = 'options'

    def __init__(self, app):
        self.app = app
        self.surface = app.surface

        self.scene = Menu.HOME
        self.setting_theme = pg.image.load("theme.png").convert_alpha()
        self.setting_theme.set_alpha(140)

        self.home_buttons = [
            Text(self.app, "Spider-Man", COLOR, pos=(1000, 320), size=60),
            Text(self.app, "No Way Home", COLOR, pos=(1000, 400), size=40),
            Button(self.app, (200, 300), "START", size=(200, 60), font_size=35),
            Button(self.app, (200, 400), "OPTIONS", size=(200, 60), font_size=35,
                   onclick=self.setOptionScene),
            Button(self.app, (200, 500), "QUIT", size=(200, 60), font_size=35, onclick=Menu.quit),
        ]

        self.options_buttons = [
            Text(self.app, "OPTIONS", COLOR, (WIDTH // 2, 50), size=35),
            Button(self.app, (200, 650), "BACK", (200, 60), font_size=30, onclick=self.setHomeScene),
            SelectSetting(self.app, "Display mode", ["Full Screen", "Window", "BorderLess"]
                          , (200, 150)),
            SelectSetting(self.app, "Resolution", ["1280 x 720", "1960 x 1080", "3920 x 2160"]
                          , (180, 270), offset=170),
            CheckboxSetting(self.app, "Vsync", (150, 390), offset=420),
            CheckboxSetting(self.app, "Shadow", (160, 430), offset=410),
            SliderSetting(self.app, "Music", (WIDTH // 2 + 100, 150), offset=150),
            SliderSetting(self.app, "Sound", (WIDTH // 2 + 100, 200), offset=150),
            ToggleSetting(self.app, "Voice Language",
                          options=["English", "Vietnamese", "Japanese", "Korean", "Chinese"],
                          pos=(WIDTH // 2 + 170, 400), offset=200)
        ]

    def update(self):
        if self.scene == Menu.HOME:
            for button in self.home_buttons:
                button.update()

        elif self.scene == Menu.OPTIONS:
            for button in self.options_buttons:
                button.update()

    def draw(self):
        if self.scene == Menu.HOME:
            for button in self.home_buttons:
                button.draw()

        elif self.scene == Menu.OPTIONS:
            self.surface.blit(self.setting_theme, (0, 0))

            for button in self.options_buttons:
                button.draw()

    def eventHandling(self, e):
        if self.scene == Menu.HOME:
            for button in self.home_buttons:
                button.eventHandling(e)

        elif self.scene == Menu.OPTIONS:
            for button in self.options_buttons:
                button.eventHandling(e)

    def setHomeScene(self):
        self.scene = Menu.HOME

    def setOptionScene(self):
        self.scene = Menu.OPTIONS

    @classmethod
    def quit(cls):
        pg.quit()
        sys.exit(0)


class SelectSetting(UIComponent):
    def __init__(self, app, text, selections: list[str], pos: tuple[int, int], offset=150):
        super().__init__(app)
        self.surface = app.surface

        self.text = Text(app, text, pos=pos, size=30)
        self.rect = pg.Rect(pos[0] + offset, pos[1] - 20, 250, 40)

        self.selections = [
            Text(app, selection, size=20, pos=self.rect.center) for selection in selections
        ]

        self.down = pg.image.load("down.png")
        self.down = pg.transform.scale(self.down, (20, 20))

        spacing = 35

        self.selections_click = [
            Text(app, selection, size=20, pos=(self.rect.centerx, self.rect.centery + i * spacing)) for i, selection in
            enumerate(selections)
        ]

        self.current = 0
        self.pos = pos

        self.choosing = False

    def draw(self):
        self.text.draw()
        pg.draw.rect(self.surface, COLOR, self.rect, 2)
        self.surface.blit(self.down, (self.rect.right - 30, self.rect.top + 10))

        if self.choosing:
            for selection in self.selections_click:
                selection.draw()
        else:
            self.selections[self.current].draw()

    def eventHandling(self, e):
        mx, my = pg.mouse.get_pos()

        if e.type == pg.MOUSEBUTTONUP:
            if not self.choosing:

                if self.rect.collidepoint((mx, my)):
                    self.choosing = True
            else:

                for i, selection in enumerate(self.selections_click):
                    if selection.getRect().collidepoint((mx, my)):
                        self.current = i
                        self.choosing = False
                        break

                if self.choosing and self.rect.collidepoint((mx, my)):
                    self.choosing = False


class ToggleSetting(UIComponent):
    def __init__(self, app, text, options, pos, offset):
        super().__init__(app)
        self.surface = app.surface
        self.text = Text(app, text, COLOR, pos, size=30)

        self.rect = pg.Rect(pos[0] + offset, pos[1] - 16, 150, 30)

        self.left = pg.transform.scale(pg.image.load("left-arrow.png"), (24, 24))
        self.left_rect = self.left.get_rect()
        self.left_rect.x, self.left_rect.y = self.rect.left - 32, self.rect.y

        self.right = pg.transform.scale(pg.image.load("right-arrow.png"), (24, 24))
        self.right_rect = self.right.get_rect()
        self.right_rect.x, self.right_rect.y = self.rect.right, self.rect.y

        self.options = [
            Text(app, opt, COLOR, self.rect.center, size=25) for opt in options
        ]

        self.current = 0

    def eventHandling(self, e):
        mouse = pg.mouse.get_pos()

        if e.type == pg.MOUSEBUTTONUP:
            if self.left_rect.collidepoint(mouse):
                self.current = (self.current + len(self.options) - 1) % len(self.options)
            if self.right_rect.collidepoint(mouse):
                self.current = (self.current + 1) % len(self.options)

    def draw(self):
        self.text.draw()
        self.surface.blit(self.left, self.left_rect)
        self.surface.blit(self.right, self.right_rect)
        self.options[self.current].draw()


class CheckboxSetting(UIComponent):
    def __init__(self, app, text, pos, offset=150):
        super().__init__(app)
        self.surface = app.surface

        self.text = Text(app, text, COLOR, pos, size=30)

        self.rect = pg.Rect(pos[0] + offset, pos[1] - 15, 30, 30)

        self.check_img = pg.transform.scale(pg.image.load("check.png"), (30, 30))
        self.uncheck_img = pg.transform.scale(pg.image.load("uncheck.png"), (30, 30))

        self.active = False

    def eventHandling(self, e):
        mx, my = pg.mouse.get_pos()

        if e.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint((mx, my)):
                self.active = not self.active

    def draw(self):
        self.text.draw()
        if self.active:
            self.surface.blit(self.check_img, self.rect)
        else:
            self.surface.blit(self.uncheck_img, self.rect)


class SliderSetting(UIComponent):
    def __init__(self, app, text, pos, offset=150):
        super().__init__(app)
        self.surface = app.surface

        self.text = Text(app, text, COLOR, pos, size=30)

        self.start = pos[0] + offset
        self.width = 300
        self.end = self.start + self.width

        self.value = 50  # 0 -> 100

        self.bar = pg.Rect(self.start, pos[1] - 10, self.width, 10)
        self.rod = pg.Rect(self.start + self.width // 2, pos[1] - 20, 10, 30)

        self.pressed = False

    def update(self):
        x, y = mx, my = pg.mouse.get_pos()

        if self.pressed:
            if mx < self.start:
                x = self.start
            elif mx > self.end:
                x = self.end - self.rod.width

            self.rod.x = x

            self.value = int((self.rod.x - self.start) / self.width * 100)
            print(self.value)

    def draw(self):
        pg.draw.rect(self.surface, COLOR, self.bar)
        pg.draw.rect(self.surface, "#27b8b3", self.rod)
        self.text.draw()

    def eventHandling(self, e):
        mouse = pg.mouse.get_pos()

        if e.type == pg.MOUSEBUTTONDOWN:
            if self.bar.collidepoint(mouse) or self.rod.collidepoint(mouse):
                self.pressed = True

        if e.type == pg.MOUSEBUTTONUP:
            self.pressed = False


class Text(UIComponent):
    def __init__(self, app, text: str, color=COLOR, pos: tuple[int, int] = (0, 0),
                 font: str = "fonts/Roboto-Medium.ttf", size: int = 40):
        super().__init__(app)
        self.surface = app.surface
        self.font = pg.font.Font(font, size)

        self.text_surf = self.font.render(text, True, color)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = pos

    def eventHandling(self, e):
        pass

    def setPos(self, center: tuple[int, int]):
        self.text_rect.center = center

    def draw(self):
        self.surface.blit(self.text_surf, self.text_rect)

    def getRect(self):
        return self.text_rect

    def setTopRightPos(self, pos):
        self.text_rect.x = pos[0]
        self.text_rect.y = pos[1]


class Button(UIComponent):

    def __init__(self, app, center: tuple[int, int], text: str, size: tuple[int, int] = (300, 80), font_size: int = 60,
                 onclick=None):
        super().__init__(app)
        self.surface = app.surface

        self.function = onclick

        self.w = size[0]
        self.h = size[1]
        self.x = center[0] - self.w // 2
        self.y = center[1] - self.h // 2

        self.hover_active = False

        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.hover_rect = pg.Rect(self.x - 5, self.y - 5, self.w + 10, self.h + 10)

        self.text = Text(app, text, size=font_size, pos=center, color=COLOR)
        self.hover_text = Text(app, text, size=font_size + 5, pos=center, color=COLOR)

    def update(self):
        x, y = pg.mouse.get_pos()

        if self.rect.collidepoint(x, y):
            self.hover_active = True
        else:
            self.hover_active = False

    def draw(self):
        if self.hover_active:
            pg.draw.rect(self.surface, COLOR, self.hover_rect, 2, 20)
            self.hover_text.draw()
        else:
            pg.draw.rect(self.surface, COLOR, self.rect, 2, 20)
            self.text.draw()

    def eventHandling(self, e):
        if e.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                if self.function:
                    self.function()
