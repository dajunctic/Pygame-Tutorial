from Setting import *
from Player import Player
from Object import ObjectList


class Game:
    def __init__(self):

        pg.init()
        self.surface = pg.display.set_mode(RESOLUTION)
        pg.display.set_caption("Player Example")
        self.clock = pg.time.Clock()
        self.delta_time = 0

        self.player = Player(self.surface, (200, 200))
        self.objectList = ObjectList(self)

    def update(self):
        self.player.update()
        self.objectList.update()

    def draw(self):
        self.surface.fill("#b8b4b4")
        self.player.draw()
        self.objectList.draw()

    def handleKeyboard(self, e):
        if e.type == pg.KEYDOWN:
            pass

        if e.type == pg.KEYUP:
            if e.key == pg.K_SPACE:
                self.player.setTrigger(Player.JUMP, Player.IDLE, False)

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                self.handleKeyboard(e)

            self.update()
            self.draw()

            self.delta_time = self.clock.tick()
            pg.display.set_caption("Animation Example: " + str(round(self.clock.get_fps(), 2)))

            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
