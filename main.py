import pygame
from engine import engine
from settings import screen, FPS, clock, activity
from technical_function import *

pygame.mixer.music.load('music\\music.mp3')
pygame.mixer.music.play()

def start():
    global FPS, clock, activity
    fon = load_image('headpiece2.png')
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