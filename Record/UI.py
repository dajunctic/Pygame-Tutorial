import sys

import pygame as pg
from setings import *


class UIComponent:
    def __init__(self, app):
        self.app = app
        self.surface = app.surface

    def update(self):
        pass

    def draw(self):
        pass

    def eventHandling(self, e):
        pass


class Menu(UIComponent):
    HOME = 'home'
    OPTIONS = 'option'

    def __init__(self, app):
        super().__init__(app)

        self.scene = Menu.OPTIONS
        self.theme = pg.image.load(THEME_IMG).convert_alpha()
        self.theme.set_alpha(140)  # 1 - 255

        self.UIComponents = {
            Menu.HOME: [
                Text(self.app, "Spider-man", pos=(1000, 320), size=60),
                Text(self.app, "No way home", pos=(1000, 400), size=40),
                Button(self.app, pos=(200, 300), text="START", font_size=35),
                Button(self.app, pos=(200, 400), text="OPTION", font_size=35, onclick=[self.changeOptionScene]),
                Button(self.app, pos=(200, 500), text="QUIT", font_size=35, onclick=[Menu.quit]),
            ],
            Menu.OPTIONS: [
                Text(self.app, "OPTION", pos=(WIDTH // 2, 50), size=35),
                SelectSetting(self.app, "Display mode", ["Fullscreen", "Windowed", "Borderless"],
                              pos=(100, 140), offset=250),
                SelectSetting(self.app, "Resolution", ["1280 x 720", "1960 x 1080", "3920 x 2160"],
                              pos=(100, 260), offset=250),
                CheckboxSetting(self.app, "Vsync", (100, 380), offset=475),
                CheckboxSetting(self.app, "Shadow", (100, 420), offset=475),
                SliderSetting(self.app, "Music", pos=(WIDTH // 2 + 100, 140), offset=180),
                SliderSetting(self.app, "Sound", pos=(WIDTH // 2 + 100, 190), offset=180),
                ToggleSetting(self.app, "Voice Language", ["English", "Vietnamese", "Japanese", "Korean", "Chinese"],
                              pos=(WIDTH // 2 + 100, 400), offset=310),
                Button(self.app, pos=(100, 600), text="BACK", font_size=35, topleft=True, onclick=[self.changeHomeScene]),
            ]
        }

    def draw(self):
        if self.scene == Menu.OPTIONS:
            self.surface.blit(self.theme, (0, 0))

        for component in self.UIComponents[self.scene]:
            component.draw()

    def update(self):
        for component in self.UIComponents[self.scene]:
            component.update()

    def eventHandling(self, e):
        for component in self.UIComponents[self.scene]:
            component.eventHandling(e)

    def changeHomeScene(self):
        self.scene = Menu.HOME

    def changeOptionScene(self):
        self.scene = Menu.OPTIONS

    @classmethod
    def quit(cls):
        pg.quit()
        sys.exit(0)

class Text(UIComponent):
    def __init__(self, app, text: str, color=COLOR, pos: tuple[int, int] = (WIDTH // 2, HEIGHT // 2),
                 font="fonts/Roboto-Medium.ttf", size: int = 40, topleft=False):
        super().__init__(app)

        self.text = text
        self.color = color

        self.pos = pos

        self.font = pg.font.Font(font, size)

        self.text_surf = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surf.get_rect()

        if topleft:
            self.text_rect.topleft = pos
        else:
            self.text_rect.center = pos

    def draw(self):
        self.surface.blit(self.text_surf, self.text_rect)

    def getRect(self):
        return self.text_rect


class Button(UIComponent):
    def __init__(self, app, pos: tuple[int, int], text: str, size: tuple[int, int] = (200, 60),
                 font_size: int = 60, onclick=None, topleft=False):
        super().__init__(app)

        self.functions = onclick

        self.w = size[0]
        self.h = size[1]
        self.x = pos[0] - self.w // 2 if not topleft else pos[0]
        self.y = pos[1] - self.h // 2 if not topleft else pos[1]

        self.hover_active = False

        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.hover_rect = pg.Rect(self.x - 5, self.y - 5, self.w + 10, self.h + 10)

        self.text = Text(self.app, text, pos=self.rect.center, size=font_size)
        self.hover_text = Text(self.app, text, pos=self.rect.center, size=font_size + 5)

    def update(self):
        mouse = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse):
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
            if self.hover_rect.collidepoint(pg.mouse.get_pos()):
                for function in self.functions:
                    function()


class SelectSetting(UIComponent):
    def __init__(self, app, text, selections: list[str], pos, offset=150):
        super().__init__(app)

        self.text = Text(app, text, pos=pos, size=30, topleft=True)
        self.rect = pg.Rect(pos[0] + offset, pos[1], 250, 40)

        self.selections = [
            Text(app, selection, size=20, pos=self.rect.center) for selection in selections
        ]

        self.down = pg.transform.scale(pg.image.load("assets/down.png"), (20, 20))

        spacing = 35
        self.selections_click = [
            Text(app, selection, size=20, pos=(self.rect.centerx, self.rect.centery + spacing * i))
            for i, selection in enumerate(selections)
        ]

        self.current = 0
        self.pos = pos

        self.choosing = False

    def eventHandling(self, e):
        mouse = pg.mouse.get_pos()
        if e.type == pg.MOUSEBUTTONUP:
            if not self.choosing:
                if self.rect.collidepoint(mouse):
                    self.choosing = True
            else:
                for i, select in enumerate(self.selections_click):
                    if select.getRect().collidepoint(mouse):
                        self.current = i
                        self.choosing = False
                        break

                if self.choosing and self.rect.collidepoint(mouse):
                    self.choosing = False

    def draw(self):
        self.text.draw()
        pg.draw.rect(self.surface, COLOR, self.rect, 2)
        self.surface.blit(self.down, (self.rect.right - 30, self.rect.top + 10))

        if self.choosing:
            for select in self.selections_click:
                select.draw()
        else:
            self.selections[self.current].draw()

class CheckboxSetting(UIComponent):
    def __init__(self, app, text, pos, offset=200):
        super().__init__(app)
        self.text = Text(app, text, pos=pos, size=30, topleft=True)
        self.rect = pg.Rect(pos[0] + offset, pos[1], 30, 30)

        self.check_img = pg.transform.scale(pg.image.load('assets/check.png'), (30, 30))
        self.uncheck_img = pg.transform.scale(pg.image.load('assets/uncheck.png'), (30, 30))

        self.active = False

    def eventHandling(self, e):
        mouse = pg.mouse.get_pos()
        if e.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(mouse):
                self.active = not self.active

    def draw(self):
        self.text.draw()
        if self.active:
            self.surface.blit(self.check_img, self.rect)
        else:
            self.surface.blit(self.uncheck_img, self.rect)


class SliderSetting(UIComponent):
    def __init__(self, app, text, pos, offset=150, value=50):
        super().__init__(app)

        self.text = Text(app, text, pos=pos, size=30, topleft=True)

        self.start = pos[0] + offset
        self.width = 300
        self.end = self.start + self.width

        self.bar = pg.Rect(self.start, pos[1] + 12, self.width, 10)
        self.rod = pg.Rect(self.start + self.width // 2, pos[1] + 1, 10, 30)

        self.pressed = False

    def update(self):
        x, y = mx, my = pg.mouse.get_pos()

        if self.pressed:
            if mx < self.start:
                x = self.start
            elif mx > self.end - self.rod.width:
                x = self.end - self.rod.width

            self.rod.x = x

    def draw(self):
        self.text.draw()
        pg.draw.rect(self.surface, COLOR, self.bar)
        pg.draw.rect(self.surface, "#27b8b3", self.rod)

    def eventHandling(self, e):
        mouse = pg.mouse.get_pos()

        if e.type == pg.MOUSEBUTTONDOWN:
            if self.bar.collidepoint(mouse) or self.rod.collidepoint(mouse):
                self.pressed = True

        if e.type == pg.MOUSEBUTTONUP:
            self.pressed = False


class ToggleSetting(UIComponent):
    def __init__(self, app, text, options, pos, offset):
        super().__init__(app)

        self.text = Text(app, text, pos=pos, size=30, topleft=True)
        self.rect = pg.Rect(pos[0] + offset, pos[1] + 3, 150, 30)

        self.left = pg.transform.scale(pg.image.load('assets/left-arrow.png').convert_alpha(), (24, 24))
        self.left_rect = self.left.get_rect()
        self.left_rect.topleft = (self.rect.left - 24, self.rect.top)

        self.right = pg.transform.scale(pg.image.load('assets/right-arrow.png').convert_alpha(), (24, 24))
        self.right_rect = self.right.get_rect()
        self.right_rect.topleft = (self.rect.right, self.rect.top)

        self.options = [
            Text(app, opt, COLOR, self.rect.center, size=25) for opt in options
        ]

        self.current = 0

    def eventHandling(self, e):
        mouse = pg.mouse.get_pos()

        if e.type == pg.MOUSEBUTTONUP:
            if self.left_rect.collidepoint(mouse):
                self.current = (self.current + len(self.options) - 1) % len(self.options)
            elif self.right_rect.collidepoint(mouse):
                self.current = (self.current + 1) % len(self.options)

    def draw(self):
        self.text.draw()
        self.surface.blit(self.left, self.left_rect)
        self.surface.blit(self.right, self.right_rect)
        self.options[self.current].draw()
