import pygame
from technical_function import *
from settings import FPS, clock, activity, screen

def game_over():
    image = load_image('game_over.png')
    x_pos = -800
    v = 400
    running = True
    screen.blit(image, (x_pos, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((0, 0, 0))
        if x_pos < 0:
            x_pos += v * clock.tick() / 1000
        screen.blit(image, (int(x_pos), 0))
        pygame.display.flip()