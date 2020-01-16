import pygame
import random
from constants import speed, width_obstacle, height_obstacle, width_obstacle_2, height_obstacle_2
from SettingsGame import all_sprites, border_sprite, player_sprite, speed_score
from OddFunctions import load_image
clock = pygame.time.Clock()


class ObstacleMain(pygame.sprite.Sprite):
    def __init__(self, group, width, height, x, y, sheet, columns, rows):
        self.speed = speed
        self.count_time = 0
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x, y)
        super().__init__(group)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.count_time % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
        self.count_time += 1
        global speed_score
        self.rect = self.rect.move(-self.speed, 0)
        if self.rect.x < -width_obstacle:
            self.remove(all_sprites)
            speed_score.score += 10
        self.speed = speed_score.speed
        self.property()

    def property(self):
        pass


class Obstacle_4(ObstacleMain):
    def __init__(self, x, y):
        y = 440
        super().__init__(all_sprites, width_obstacle, height_obstacle, x, y, load_image(r'Obstacles\4.png'), 1, 1)

    def property(self):
        pass


class Obstacle_2(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, x, y, load_image(r'Obstacles\2.png'), 5, 1)

    def property(self):
        pass


class Obstacle_3(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, x, y, load_image(r'Obstacles\3.png'), 5, 1)

    def property(self):
        self.rect = self.rect.move(-10, 0)


class Obstacle(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(all_sprites, width_obstacle, height_obstacle, x, y, load_image(r'Obstacles\1.png'), 5, 1)

    def property(self):
        pass


class Border(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(border_sprite)
        self.image = pygame.Surface([0, 480])
        self.rect = pygame.Rect(0, 490, 800, 100)
