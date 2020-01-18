import pygame
from engine import engine
from settings import screen, FPS, clock
from technical_function import *

def start():
    global FPS, clock
    fon = load_image('headpiece.png')
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                engine()
        pygame.display.flip()
        clock.tick(FPS)

start()