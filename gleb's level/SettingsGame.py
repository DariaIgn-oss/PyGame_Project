import pygame
from OddFunctions import load_image


border_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
player_image = load_image("mario.png")

dct_variables = {'speed': 10, 'score': 0}