import random

from Setting import *


class Object:
    def __init__(self, app, rect: tuple[float, float, float, float]):
        self.app = app
        self.surface = app.surface

        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]

        self.right = self.x + self.w

        self.color = "#000000"
        self.speed = 200

    def update(self):
        self.x -= self.speed * self.app.delta_time / 1000.0
        self.right = self.x + self.w

    def draw(self):
        pg.draw.rect(self.surface, self.color, (self.x, self.y, self.w, self.h), 2)


class ObjectList:
    def __init__(self, app):
        self.app = app
        self.surface = app.surface

        self.objects = []
        self.makeObjects()

    def makeObjects(self):

        if len(self.objects):
            if self.objects[-1].right < WIDTH:
                space = random.randint(300, 400)

                x = self.objects[-1].x + space
                y = random.randint(400, 600)
                w = random.randint(150, 200)
                h = 30

                self.objects.append(Object(self.app, (x, y, w, h)))
        else:
            x = -300

            for i in range(5):
                space = random.randint(300, 400)

                x += space
                y = random.randint(400, 600)
                w = random.randint(150, 200)
                h = 30

                self.objects.append(Object(self.app, (x, y, w, h)))

    def update(self):
        tmp = []
        for object in self.objects:
            object.update()

            if object.right > 0:
                tmp.append(object)

        self.objects.clear()
        self.objects = tmp

        self.makeObjects()

    def draw(self):
        for object in self.objects:
            object.draw()
