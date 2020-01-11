import pygame
# from Player import Player


fps = 30
WIDTH = 800
HEIGHT = 600

# border_sprite = pygame.sprite.Group()
# all_sprites = pygame.sprite.Group()
# enemy_sprite = pygame.sprite.Group()
# player_sprite = pygame.sprite.Group()
width_obstacle = 50
width_obstacle_2 = 30
height_obstacle_2 = 50
height_obstacle = 40
speed = 10
score = 0
speed_koef = 50
distance_between_obstacles = 50
x_last_obstacle = 0
count_obstacles_onlevel = 3
multiple_speed = True
progress = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


running = True





x_first_image, y_first_image = WIDTH, 0
x_second_image, y_second_image = x_first_image * 2, 0

# player_x = 50
# player_y = 440
# player = Player(player_x, player_y)