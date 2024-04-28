import pygame, sys, random

RESOLUTION = WIDTH, HEIGHT = (1280, 720)
FPS = 60


class App:
    def __init__(self):
        self.surface = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Ping Pong")
        self.clock = pygame.time.Clock()

        self.player1 = pygame.Rect(30, (HEIGHT - 200) // 2, 15, 200)
        self.player2 = pygame.Rect(WIDTH - 30 - 20, (HEIGHT - 200) // 2, 15, 200)
        self.player1_speed = 0
        self.player2_speed = 0

        self.size = 20
        self.ball = pygame.Rect(WIDTH // 2 - self.size // 2, HEIGHT // 2 - self.size // 2, self.size, self.size)
        self.ball_speed_x = 5
        self.ball_speed_y = 5

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                self.keyHandle(e)

            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

    def reset(self):
        self.ball = pygame.Rect(WIDTH // 2 - self.size // 2, HEIGHT // 2 - self.size // 2, self.size, self.size)
        self.ball_speed_x = random.choice((-1, 1)) * 5
        self.ball_speed_y = random.choice((-1, 1)) * 5

    def update(self):
        self.player1.y += self.player1_speed
        self.player2.y += self.player2_speed

        if self.player1.top <= 0:
            self.player1.top = 0
        if self.player1.bottom >= HEIGHT:
            self.player1.bottom = HEIGHT

        if self.player2.top <= 0:
            self.player2.top = 0
        if self.player2.bottom >= HEIGHT:
            self.player2.bottom = HEIGHT

        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            self.ball_speed_y *= -1
        # if self.ball.left <= 0 or self.ball.right >= WIDTH:
        #     self.ball_speed_x *= -1

        offset = 10
        if self.ball.colliderect(self.player1) and self.ball_speed_x < 0:
            if abs(self.ball.left - self.player1.right) < offset:
                self.ball_speed_x *= -1
            elif abs(self.ball.top - self.player1.bottom) < offset:
                self.ball_speed_y *= -1
            elif abs(self.ball.bottom - self.player1.top) < offset:
                self.ball_speed_y *= -1

        if self.ball.colliderect(self.player2) and self.ball_speed_x > 0:
            if abs(self.ball.right - self.player2.left) < offset:
                self.ball_speed_x *= -1
            elif abs(self.ball.top - self.player2.bottom) < offset:
                self.ball_speed_y *= -1
            elif abs(self.ball.bottom - self.player2.top) < offset:
                self.ball_speed_y *= -1

        if self.ball.right < 0 or self.ball.left > WIDTH:
            self.reset()


    def draw(self):
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, 1280, 720))
        pygame.draw.line(self.surface, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        pygame.draw.rect(self.surface, (255, 255, 255), self.player1)
        pygame.draw.rect(self.surface, (255, 255, 255), self.player2)

        # pygame.draw.rect(self.surface, (9, 150, 255), self.ball)
        pygame.draw.circle(self.surface, (9, 150, 255), self.ball.center, self.size // 2)

    def keyHandle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player1_speed += -6
            if event.key == pygame.K_s:
                self.player1_speed += 6

            if event.key == pygame.K_UP:
                self.player2_speed += -6
            if event.key == pygame.K_DOWN:
                self.player2_speed += 6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.player1_speed += 6
            if event.key == pygame.K_s:
                self.player1_speed += -6

            if event.key == pygame.K_UP:
                self.player2_speed += +6
            if event.key == pygame.K_DOWN:
                self.player2_speed += -6


if __name__ == '__main__':
    game = App()
    game.run()
