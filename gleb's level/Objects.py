import pygame
import random
from constants import speed, width_obstacle, height_obstacle, width_obstacle_2, height_obstacle_2
from settings import all_sprites, border_sprite, enemy_sprite, player_sprite, dct_variables
score = dct_variables['score']


class ObstacleMain(pygame.sprite.Sprite):
    def __init__(self, group, width, height, color, x, y):
        super().__init__(group)
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, [0, 0, width_obstacle_2, height_obstacle_2])
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def update(self):
        global score
        self.rect = self.rect.move(-self.speed, 0)
        if self.rect.x < -width_obstacle:
            self.remove(all_sprites)
            score += 10
        self.speed = speed
        dct_variables['score'] = score


class Platform(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, pygame.Color('red'), x, y)
        y = random.randint(250, 450)


class Enemy(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(enemy_sprite, width_obstacle, height_obstacle, pygame.Color('yellow'), x, y)


class Obstacle_2(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, pygame.Color('red'), x, y)


class Enemy_2(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, pygame.Color('blue'), x, y)


class Obstacle(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, pygame.Color('white'), x, y)


class Border(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(border_sprite)
        self.image = pygame.Surface([0, 480])
        self.rect = pygame.Rect(0, 490, 800, 100)