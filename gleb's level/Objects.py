import pygame
import random
from constants import speed, width_obstacle, height_obstacle, width_obstacle_2, height_obstacle_2
from SettingsGame import all_sprites, border_sprite, enemy_sprite, player_sprite, dct_variables
from OddFunctions import load_image
score = dct_variables['score']


class ObstacleMain(pygame.sprite.Sprite):
    def __init__(self, group, width, height, x, y, sheet, columns, rows):
        super().__init__(group)
        # self.image = pygame.Surface([width, height])
        # pygame.draw.rect(self.image, color, [0, 0, width_obstacle_2, height_obstacle_2])
        # self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

        global score
        self.rect = self.rect.move(-self.speed, 0)
        if self.rect.x < -width_obstacle:
            self.remove(all_sprites)
            score += 10
        self.speed = speed
        dct_variables['score'] = score


class Platform(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, x, y, load_image(r'Obstacles\1.png'), 8, 2)
        y = random.randint(250, 450)


class Enemy(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(enemy_sprite, width_obstacle, height_obstacle, x, y), load_image(r'Obstacles\1.png'), 8, 2


class Obstacle_2(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, x, y, load_image(r'Obstacles\1.png'), 8, 2)


class Enemy_2(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, x, y, load_image(r'Obstacles\1.png'), 8, 2)


class Obstacle(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, x, y, load_image(r'Obstacles\1.png'), 1, 1)


class Border(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(border_sprite)
        self.image = pygame.Surface([0, 480])
        self.rect = pygame.Rect(0, 490, 800, 100)
