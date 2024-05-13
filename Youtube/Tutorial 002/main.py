import pygame

RESOLUTION = (1280, 720)
FPS = 60


class App:
    def __init__(self):
        self.surface = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Pygame Tutorial")
        self.clock = pygame.time.Clock()

        self.x, self.y = 400, 400
        self.speed = 20
        self.move = True

    def run(self):
        is_running = True

        while is_running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    is_running = False

                if e.type == pygame.KEYDOWN:
                    self.keyHandle(e.type, e.key)

                # if e.type == pygame.KEYUP:
                #
                #     self.keyHandle(e.type, e.key)

            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, 1280, 720))

        pygame.draw.circle(self.surface, (12, 205, 235), (self.x, self.y), 100)

        pygame.draw.circle(self.surface, (0, 0, 255), (800, 300), 50)

    def checkCollision(self, x1, y1, r1, x2, y2, r2):
        dist = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return dist <= (r1 + r2) ** 2

    def keyHandle(self, typ, key):
        if typ == pygame.KEYDOWN:

            if key == pygame.K_w:
                if not self.checkCollision(self.x, self.y - self.speed, 100, 800, 300, 50):
                    self.y -= self.speed



            elif key == pygame.K_s:
                if not self.checkCollision(self.x, self.y + self.speed, 100, 800, 300, 50):
                    self.y += self.speed

            elif key == pygame.K_a:
                if not self.checkCollision(self.x - self.speed, self.y, 100, 800, 300, 50):
                    self.x -= self.speed

            elif key == pygame.K_d:
                if not self.checkCollision(self.x + self.speed, self.y, 100, 800, 300, 50):
                    self.x += self.speed


if __name__ == '__main__':
    game = App()
    game.run()
