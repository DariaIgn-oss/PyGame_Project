import pygame
import random
from Objects import Obstacle, Obstacle_2, Obstacle_3, Obstacle_4, Border
from settings import objects_sprites, border_sprite, player_sprite, speed_score, screen, WIDTH, HEIGHT
# from Player import Player
from technical_function import terminate, load_image, restart_level3
from third_level import start


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sheet, columns, rows):
        super().__init__(player_sprite)
        self.speed = 2
        self.jump = False
        self.walk = []
        self.jump_and_fall = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.walk[self.cur_frame]
        self.rect = self.rect.move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                if j == 0 and i > 0 and i < 7:
                    self.walk.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))
                if j == 5 and i == 1:
                    self.jump_and_fall.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

    def update(self):
        for i in objects_sprites:
            if pygame.sprite.collide_mask(self, i):
                global x_first_image, x_second_image, y_first_image, y_second_image, WIDTH, progress
                objects_sprites.update()
                player_sprite.draw(screen)
                objects_sprites.draw(screen)
                pygame.display.flip()
                restart_level3()
                screen.fill((0, 0, 0))
                progress = 0
                start_screen2()
                x_first_image, y_first_image = WIDTH, 0
                x_second_image, y_second_image = x_first_image * 2, 0
                background_scroll(x_first_image, x_second_image, speed_score.speed)
                # terminate()

        if not self.jump:
            self.cur_frame = (self.cur_frame + 1) % len(self.walk)
            self.image = self.walk[self.cur_frame]
            pygame.mixer.Sound('data/step.wav').play()
        if self.jump:
            if self.speed >= 0:
                self.rect.y -= (self.speed ** 3)
                self.image = self.jump_and_fall[-1]
                if self.rect.y < 0:
                    self.rect.y = self.rect.size[1] // 9  # высота героя
            else:
                self.rect.y += (self.speed ** 2)
            self.speed -= 1
        if self.rect.y > 440:
            self.rect.y = 440
            self.jump = False
        if pygame.sprite.spritecollideany(self, border_sprite):
            self.last_frame_fall = False
            self.jump = False
        self.mask = pygame.mask.from_surface(self.image, 300)


pygame.init()
pygame.mixer.init()

pause = False
fps = 20
clock = pygame.time.Clock()
speed_koef = 50
count_obstacles_onlevel = 3
multiple_speed = True
progress = 0

running = True


def choose_obj(x, y):
    level = 0
    if progress > 30:
        level = 3
    elif progress > 20:
        level = 2
    elif progress > 10:
        level = 1
    number = random.randint(0, level)
    dct = {0: Obstacle, 1: Obstacle_2, 2: Obstacle_3, 3: Obstacle_4}
    return dct[number](x, y)


def level():
    global x_first_image, x_second_image, speed_score, progress, x_last_obstacle, speed_koef, multiple_speed, count_obstacles_onlevel, pause
    pygame.mouse.set_visible(False)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause
        if not pause:
            while len(objects_sprites) < count_obstacles_onlevel:
                y = random.randint(0, player_y)
                x = WIDTH + random.randint(0, 5) * speed_koef
                progress += 1
                choose_obj(x, y)
            pygame.display.update()
            if pygame.key.get_pressed()[273]:
                player.jump = True
                player.speed = 3

            x_first_image, x_second_image = background_scroll(x_first_image, x_second_image, speed_score.speed)

            objects_sprites.update()
            if not (x_first_image > player_x and x_second_image > player_x):
                player_sprite.update()
                player_sprite.draw(screen)

            objects_sprites.draw(screen)

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
    if progress == 50:
        pygame.mixer.stop()
        start()


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


def start_screen2():
    intro_text = ["Вы выбрались из котла!", "",
                  "Теперь вам нужно пробежать мимо чертовых руин!",
                  "Для начала игры нажмите SPACE"]

    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.Sound('data/level_audio.wav').play()
                level()  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


player_x = 50
player_y = 440
Border()
player = Player(player_x, player_y, load_image(r"Hero\skeletonBase.png"), 10, 6)  # magic numbers, must fix

start_screen2()

