from technical_function import *
from settings import clock, screen


def victory():
    victory_image = load_image('victory.png')
    x_pos = -800
    v = 400
    running = True
    screen.blit(victory, (x_pos, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((255, 255, 255))
        if x_pos < 0:
            x_pos += v * clock.tick() / 1000
        screen.blit(victory_image, (int(x_pos), 0))
        pygame.display.flip()
