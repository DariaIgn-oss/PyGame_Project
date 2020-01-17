import pygame
import random
from Objects import Obstacle, Obstacle_2, Obstacle_3, Obstacle_4, Border
from SettingsGame import all_sprites, border_sprite, player_sprite, speed_score, screen, WIDTH, HEIGHT
from Player import Player
from OddFunctions import terminate, load_image


pygame.init()
pygame.mixer.init()

fps = 20
clock = pygame.time.Clock()
speed_koef = 50
count_obstacles_onlevel = 3
# jump = pygame.mixer.music.load('data/level_audio.wav')
multiple_speed = True
progress = 0

running = True


def choose_obj(x, y):
    level = 0
    if progress > 20:
        level = 3
    elif progress > 30:
        level = 2
    elif progress > 10:
        level = 1
    number = random.randint(0, level)
    dct = {0: Obstacle, 1: Obstacle_2, 2: Obstacle_3, 3: Obstacle_4}
    return dct[number](x, y)


def level():
    global x_first_image, x_second_image, speed_score, progress, x_last_obstacle, speed_koef, multiple_speed, count_obstacles_onlevel
    while running:
        while len(all_sprites) < count_obstacles_onlevel:
            y = random.randint(0, player_y)
            x = WIDTH + random.randint(0, 5) * speed_koef
            progress += 1
            choose_obj(x, y)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if pygame.key.get_pressed()[273]:
            # pygame.mixer.music.load('data/jump.wav')
            # pygame.mixer.music.play()
            # pygame.mixer.Sound('data/jump.wav').play()
            player.jump = True
            player.speed = 3

        x_first_image, x_second_image = background_scroll(x_first_image, x_second_image, speed_score.speed)

        all_sprites.update()
        player_sprite.update()
        player_sprite.draw(screen)

        all_sprites.draw(screen)

        font = pygame.font.Font(None, 30)
        text_coord = 50

        string_rendered = font.render(str(speed_score.score), 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(fps)
        progress_counter()


def progress_counter():
    global multiple_speed, speed_koef, count_obstacles_onlevel
    if progress % 15 == 0 and multiple_speed and progress < 150:
        speed_score.speed += 1
        speed_koef += 10
        multiple_speed = False
    elif progress % 30 == 0 and multiple_speed:
        speed_score.speed += 1
        speed_koef += 10
        multiple_speed = False
    elif progress % 15 == 1:
        multiple_speed = True
    if progress % 50 == 0 and count_obstacles_onlevel < 8:
        count_obstacles_onlevel += 1


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
                pygame.mixer.Sound('data/level_audio.wav').play()
                level()  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


player_x = 50
player_y = 440
Border()
player = Player(player_x, player_y, load_image(r"Hero\skeletonBase.png"), 10, 6)  # magic numbers, must fix

start_screen()