import pygame
from technical_function import *
from settings import FPS, clock, activity, screen


def game_over():
    global FPS, clock, activity
    fon = load_image('game_over.png')
    screen.blit(fon, (0, 0))
    activity = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()