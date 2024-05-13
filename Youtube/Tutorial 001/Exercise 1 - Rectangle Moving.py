import pygame

RESOLUTION = (1280, 720)
FPS = 60


class App:
    def __init__(self):
        self.surface = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Pygame Tutorial")

        self.clock = pygame.time.Clock()
        self.x, self.y = 100, 100
        self.dx, self.dy = 1, 1

    def run(self):
        is_running = True

        while is_running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    is_running = False

            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

    def update(self):
        if self.y + 100 >= 720:
            self.dy = -1

        if self.x + 100 >= 1280:
            self.dx = -1

        if self.x <= 0:
            self.dx = 1

        if self.y <= 0:
            self.dy = 1

        self.x += self.dx * 4
        self.y += self.dy * 4

    def draw(self):
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, 1280, 720))

        pygame.draw.rect(self.surface, (255, 255, 255), (self.x, self.y, 100, 100))


if __name__ == '__main__':
    game = App()
    game.run()
