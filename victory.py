import pygame
from technical_function import *
from settings import FPS, clock, activity, screen

def victory():
    victory = load_image('victory.png')
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
        screen.blit(victory, (int(x_pos), 0))
        pygame.display.flip()