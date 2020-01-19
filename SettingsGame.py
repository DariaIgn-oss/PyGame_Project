import pygame


border_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class SpeedScore:
    def __init__(self, speed, score):
        self.speed = speed
        self.score = score


speed_score = SpeedScore(10, 0)
