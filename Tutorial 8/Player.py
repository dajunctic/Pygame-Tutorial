from Setting import *
from Animated import SpriteAnimated


class Player:
    IDLE = 'idle'
    RUN = 'run'
    WALK = 'walk'
    JUMP = 'jump'

    def __init__(self, surface: pg.Surface, center: tuple[int, int]):
        self.surface = surface
        self.center = center
        self.rect = None

        self.animations = {
            'idle': SpriteAnimated(surface, "Kunoichi/Idle.png", 9, time_per_frame=0.1, scale=2),
            'run': SpriteAnimated(surface, "Kunoichi/Run.png", 8, time_per_frame=0.1, scale=2),
            'walk': SpriteAnimated(surface, "Kunoichi/Walk.png", 8, time_per_frame=0.1, scale=2),
            'jump': SpriteAnimated(surface, "Kunoichi/Jump.png", 10, time_per_frame=0.08, scale=2),
        }

        self.status = Player.IDLE
        self.forward_status = Player.IDLE

        self.setTrigger(self.status)

        self.offset_x = 100
        self.offset_y = 100

    def setCenterPos(self, center: tuple[int, int]):
        self.center = center

    def setTrigger(self, status: str, forward_status: str = "idle", loop=True):
        self.status = status
        self.animations[self.status].reset()
        self.animations[self.status].setLoop(loop)
        self.rect = self.animations[self.status].getRect()
        self.forward_status = forward_status

    def update(self):
        self.animations[self.status].setCenterPos(self.center)
        self.animations[self.status].update()

        if self.animations[self.status].hasEnd():
            self.setTrigger(self.forward_status)

    def getRect(self):
        rect = self.animations[self.status].getRect()
        x = rect.x + self.offset_x
        y = rect.y + self.offset_y

        w = rect.w
        h = rect.h

        w = rect.w - self.offset_x * 2
        h = rect.h - self.offset_y * 2

        return pg.Rect(x, y, w, h)

    def draw(self):
        self.animations[self.status].draw()

        pg.draw.rect(self.surface, (0, 255, 0), self.getRect(), 2)

