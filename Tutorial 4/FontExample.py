import sys, pygame

pygame.init()
pygame.font.init()

surface = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Test")

bg_img = pygame.image.load("bg.png")

font = pygame.font.Font("fonts/MightySouly-lxggD.ttf", 120)

text_surf = font.render("Hello Everyone", True, (255, 255, 255))
text_rect = text_surf.get_rect()
text_rect.center = 640, 360

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        surface.blit(bg_img, (0, 0))

        surface.blit(text_surf, text_rect)

        pygame.display.flip()
