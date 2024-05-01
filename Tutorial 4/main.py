import pygame, sys, random

RESOLUTION = WIDTH, HEIGHT = (1280, 720)
FPS = 60


class App:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("fonts/MightySouly-lxggD.ttf", 120)

        self.surface = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Ping Pong")
        self.clock = pygame.time.Clock()

        self.player1 = pygame.Rect(30, (HEIGHT - 200) // 2, 15, 200)
        self.player2 = pygame.Rect(WIDTH - 30 - 20, (HEIGHT - 200) // 2, 15, 200)
        self.player1_speed = 0
        self.player2_speed = 6
        self.player1_score = 0
        self.player2_score = 0

        self.size = 30
        self.ball = pygame.Rect(WIDTH // 2 - self.size // 2, HEIGHT // 2 - self.size // 2, self.size, self.size)
        self.ball_speed_x = 5
        self.ball_speed_y = 5

        self.bg_img = pygame.image.load("bg.png")
        self.ball_img = pygame.image.load("ball.png")
        self.ball_img = pygame.transform.scale(self.ball_img, (self.size, self.size))

        self.paddle = pygame.image.load("paddle.png")

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

    def player2_ai(self):
        # Random
        # self.player2_speed = random.choice((-6, 6))
        # self.player2.y += self.player2_speed

        # Strategy
        if self.player2.top < self.ball.y:
            self.player2.y += self.player2_speed
        elif self.player2.bottom > self.ball.y:
            self.player2.y -= self.player2_speed

    def show_score(self):
        score1_surf = self.font.render(str(self.player1_score), True, (152, 255, 0))
        score2_surf = self.font.render(str(self.player2_score), True, (152, 255, 0))

        score1_rect = score1_surf.get_rect()
        score2_rect = score2_surf.get_rect()

        score1_rect.center = (WIDTH // 2 - 200, 100)
        score2_rect.center = (WIDTH // 2 + 200, 100)

        self.surface.blit(score1_surf, score1_rect)
        self.surface.blit(score2_surf, score2_rect)


    def update(self):
        self.player1.y += self.player1_speed
        # self.player2.y += self.player2_speed
        self.player2_ai()

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

        if self.ball.right < 0:
            self.player2_score += 1
            self.reset()

        elif self.ball.left > WIDTH:
            self.player1_score += 1
            self.reset()


    def draw(self):
        # pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, 1280, 720))
        # pygame.draw.line(self.surface, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
        self.surface.blit(self.bg_img, (0, 0))

        # pygame.draw.rect(self.surface, (255, 255, 255), self.player1)
        # pygame.draw.rect(self.surface, (255, 255, 255), self.player2)
        self.surface.blit(self.paddle, self.player1)
        self.surface.blit(self.paddle, self.player2)

        # pygame.draw.rect(self.surface, (9, 150, 255), self.ball)
        # pygame.draw.circle(self.surface, (9, 150, 255), self.ball.center, self.size // 2)
        self.surface.blit(self.ball_img, self.ball.center)

        self.show_score()

    def keyHandle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player1_speed += -6
            if event.key == pygame.K_s:
                self.player1_speed += 6

            # if event.key == pygame.K_UP:
            #     self.player2_speed += -6
            # if event.key == pygame.K_DOWN:
            #     self.player2_speed += 6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.player1_speed += 6
            if event.key == pygame.K_s:
                self.player1_speed += -6

            # if event.key == pygame.K_UP:
            #     self.player2_speed += +6
            # if event.key == pygame.K_DOWN:
            #     self.player2_speed += -6


if __name__ == '__main__':
    game = App()
    game.run()
