import pygame

# Общие константы
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

fps = 30
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

x_first_image, y_first_image = WIDTH, 0
x_second_image, y_second_image = x_first_image * 2, 0

# Kseniya's constants
x_pos = WIDTH // 2
y_pos = HEIGHT - 60
range_between = 40
count = 0
width_of_rect = 15
height_of_rect = 80
width_of_image = 20
height_of_image = 48
w_of_monster = 126
h_of_monster = 252
height_of_fon = -13290
FPS = 50
boiler_count = HEIGHT + 10
count_of_hearts = 3
coef_heart = 0
pause_count = 0
coef_apdate = 0
fon_count = 0
pause = False
rects = []
skel_sprite = pygame.sprite.Group()
platfs_sprites = pygame.sprite.Group()
monster_sprites = pygame.sprite.Group()
