import pygame
from OddFunctions import load_image


border_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
player_image = load_image("mario.png")


class SpeedScore:
    def __init__(self, speed, score):
        self.speed = speed
        self.score = score


speed_score = SpeedScore(10, 0)
