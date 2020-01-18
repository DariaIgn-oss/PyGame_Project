import pygame

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)

platforms = []
platform_sprites = pygame.sprite.Group()
sceleton_sprite = pygame.sprite.Group()
mist_sprite = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
shell_sprites = pygame.sprite.Group()

cameray = 1
score = 1
score_text = '1'
font = pygame.font.Font(None, 36)

FPS = 25
clock = pygame.time.Clock()