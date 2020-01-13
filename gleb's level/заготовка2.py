import pygame
import sys
import os
import random
from Objects import Obstacle, Obstacle_2, Enemy, Enemy_2, Border, Platform
from SettingsGame import dct_variables, all_sprites, enemy_sprite, border_sprite, player_sprite

pygame.init()

fps = 60
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
width_obstacle = 50
width_obstacle_2 = 30
height_obstacle_2 = 50
height_obstacle = 40
speed = dct_variables['speed']
score = 0
speed_koef = 50
distance_between_obstacles = 50
x_last_obstacle = 0
count_obstacles_onlevel = 3
multiple_speed = True
progress = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    print(fullname)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image
    return image


def terminate():
    pygame.quit()
    sys.exit()



# class Border(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__(border_sprite)
#         self.image = pygame.Surface([0, 480])
#         self.rect = pygame.Rect(0, 490, 800, 100)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_sprite)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = 2
        self.jump = False

    def update(self, direction):
        if self.jump:
            if self.speed >= 0:
                self.rect.y -= (self.speed ** 3)
                if self.rect.y < 0:
                    self.rect.y = 15  # высота марио
            else:
                self.rect.y += (self.speed ** 2)
            self.speed -= 1
        if self.rect.y > 460:
            self.rect.y = 460
            self.jump = False
        if pygame.sprite.spritecollideany(self, border_sprite):
            self.jump = False

        # if direction == 1:
        #     if pygame.sprite.spritecollideany(self, all_sprites):
        #         start_screen()
#
#
# class Platform(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         y = random.randint(250, 450)
#         super().__init__(all_sprites)
#         self.image = pygame.Surface((width_obstacle, height_obstacle))
#         pygame.draw.rect(self.image, pygame.Color('red'), [0, 0, width_obstacle_2, height_obstacle_2], 0)
#         self.rect = pygame.Rect(x, y, width_obstacle, height_obstacle)
#         self.speed = speed
#
#     def update(self):
#         self.rect = self.rect.move(-self.speed, 0)
#         if self.rect.x < -width_obstacle:
#             self.remove(all_sprites)
#         self.speed = speed
#
#
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__(enemy_sprite)
#         self.image = pygame.Surface((width_obstacle, height_obstacle))
#         pygame.draw.rect(self.image, pygame.Color('yellow'), [0, 0, 50, 50], 0)
#         self.rect = pygame.Rect(x, y, width_obstacle, height_obstacle)
#         self.speed = speed
#
#     def update(self):
#         self.rect = self.rect.move(-self.speed, 0)
#         if self.rect.x < -width_obstacle:
#             self.remove(all_sprites)
#         self.speed = speed
#
#
# class Obstacle_2(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__(all_sprites)
#         self.image = pygame.Surface((width_obstacle, height_obstacle))
#         pygame.draw.rect(self.image, pygame.Color('red'), [0, 0, width_obstacle_2, height_obstacle_2], 0)
#         self.rect = pygame.Rect(x, y, width_obstacle, height_obstacle)
#         self.speed = speed
#
#     def update(self):
#         global score
#         self.rect = self.rect.move(-self.speed, 0)
#         if self.rect.x < -width_obstacle:
#             self.remove(all_sprites)
#             score += 20
#         self.speed = speed
#
#
# class Enemy_2(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__(all_sprites)
#         self.image = pygame.Surface((width_obstacle, height_obstacle))
#         pygame.draw.rect(self.image, pygame.Color('blue'), [0, 0, 30, 30], 0)
#         self.rect = pygame.Rect(x, y, width_obstacle, height_obstacle)
#         self.speed = speed
#
#     def update(self):
#         global score
#         self.rect = self.rect.move(-self.speed, 0)
#         if self.rect.x < -width_obstacle:
#             self.remove(all_sprites)
#             score += 50
#         self.speed = speed
#
#
#
# class Obstacle(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__(all_sprites)
#         self.image = pygame.Surface((width_obstacle, height_obstacle))
#         pygame.draw.rect(self.image, pygame.Color('white'), [0, 0, width_obstacle, height_obstacle], 0)
#         self.rect = pygame.Rect(x, y, width_obstacle, height_obstacle)
#         self.speed = speed
#
#     def update(self):
#         global score
#         self.rect = self.rect.move(-self.speed, 0)
#         if self.rect.x < -width_obstacle:
#             self.remove(all_sprites)
#             score += 10
#         self.speed = speed


running = True


def choose_obj(x, y):
    level = 0
    if progress > 200:
        level = 4
    elif progress > 150:
        level = 3
    elif progress > 100:
        level = 2
    elif progress > 50:
        level = 1
    number = random.randint(0, level)
    dct = {0: Obstacle, 1: Obstacle_2, 2: Platform, 3: Enemy, 4: Enemy_2}
    return dct[number](x, y)


def level():
    global x_first_image, x_second_image, speed, distance_between_obstacles, progress, x_last_obstacle, speed_koef, multiple_speed, count_obstacles_onlevel
    while running:
        # print(progress)
        while len(all_sprites) + len(enemy_sprite) < count_obstacles_onlevel:
            y = random.randint(0, player_y)
            x = WIDTH + random.randint(0, 5) * speed_koef
            progress += 1

            choose_obj(x, y)
            x_last_obstacle = x

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if pygame.key.get_pressed()[273]:
            player.jump = True
            player.speed = 3
            player_sprite.update('up')

        x_first_image, x_second_image = background_scroll(x_first_image, x_second_image, speed)

        all_sprites.update()
        enemy_sprite.update()
        enemy_sprite.draw(screen)
        # screen.fill((255, 255, 255))
        player_sprite.update(1)
        player_sprite.draw(screen)

        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
        print(speed)
        if progress % 15 == 0 and multiple_speed and progress < 150:
            speed += 1
            speed_koef += 10
            multiple_speed = False
        elif progress % 30 == 0 and multiple_speed:
            speed += 1
            speed_koef += 10
            multiple_speed = False
        elif progress % 15 == 1:
            multiple_speed = True
        if progress % 50 == 0 and count_obstacles_onlevel < 8:
            count_obstacles_onlevel += 1
        dct_variables['speed'] = speed


        font = pygame.font.Font(None, 30)
        text_coord = 50

        string_rendered = font.render(str(score), 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def background_scroll(x1, x2, speed=5):
    x1 -= speed
    x2 -= speed
    screen.blit(background, (x1, y_first_image))
    screen.blit(background, (x2, y_second_image))
    if x1 < -WIDTH:
        x1 = WIDTH
    if x2 < -WIDTH:
        x2 = WIDTH
    return x1, x2


# player_image = load_image('mario.png')
background = load_image('postapocalypse1.png')

background_size = background.get_size()
background_rect = background.get_rect()
background_width, background_height = background_size
x_first_image, y_first_image = WIDTH, 0
x_second_image, y_second_image = x_first_image * 2, 0




def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                level()  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)

player_x = 50
player_y = 440
Border()
# player = Player(player_x, player_y)
koef = 15

start_screen()
