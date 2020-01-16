import pygame
import random
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image
    return image


class Platform(pygame.sprite.Sprite):
    image = load_image('platform2.png')

    def __init__(self, xx, yy, ww, hh, vy, colorr):
        super().__init__(all_sprites)
        self.image = Platform.image
        pygame.draw.rect(self.image, colorr, [xx, yy, ww, hh], 0)
        self.rect = pygame.Rect(xx, yy, ww, hh)
        self.vy = vy

    def update(self):
        self.rect = self.rect.move(0, self.vy)


class Mario(pygame.sprite.Sprite):
    image = load_image('skeleton.png')

    def __init__(self, ww, hh, wi_of_im, he_of_im):
        super().__init__(mario_sprite)
        self.w = ww
        self.h = hh
        self.image = Mario.image
        self.rect = self.image.get_rect()
        self.rect.y = hh - 100
        self.rect.x = ww // 2
        self.w_of_im = wi_of_im
        self.he_of_im = he_of_im

    def update(self, direction):
        if direction == 'left':
            if self.rect.x + 8 > self.w - self.w_of_im:
                self.rect.x = self.w - self.w_of_im
            else:
                self.rect = self.rect.move(8, 0)
        elif direction == 'right':
            if self.rect.x - 8 < 0:
                self.rect.x = 0
            else:
                self.rect = self.rect.move(-8, 0)
        elif direction == 'up':
            if self.rect.y + 8 > self.h - self.he_of_im:
                self.rect.y = self.h - self.he_of_im
            else:
                self.rect = self.rect.move(0, 8)
        elif direction == 'down':
            if self.rect.y - 8 < 0:
                self.rect.y = 0
            else:
                self.rect = self.rect.move(0, -8)

        if direction == 1:
            if pygame.sprite.spritecollideany(self, all_sprites):
                start_screen()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(monster_sprites)
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
        self.rect = self.rect.move(0, 5)


pygame.init()
clock = pygame.time.Clock()

w, h = 800, 600
x_pos = w // 2
y_pos = h - 60
range_between = 40
running = True
count = 0
width_of_rect = 15
height_of_rect = 80
width_of_image = 20
height_of_image = 48
w_of_monster = 126
h_of_monster = 252
FPS = 50
boiler_count = h + 10
count_of_hearts = 3
z = 0
p = 0
n = 0
pause = False
rects = []

size = width, height = w, h
screen = pygame.display.set_mode(size)
mario_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
monster_sprites = pygame.sprite.Group()

color = pygame.Color(255, 255, 100)
boiler = pygame.transform.scale(load_image('boiler111.png', -1), (w, h))
Mario(w, h, width_of_image, height_of_image)


def hearts():
    global count_of_hearts
    count_of_hearts = 3


def pushing():
    global all_sprites, rects, FPS, boiler_count, count
    rects = []
    FPS = 60
    boiler_count = h + 10
    count = 0
    all_sprites = pygame.sprite.Group()
    # генерация платформ
    for i in range(250):
        x = random.randint(0, w - height_of_rect)
        if i == 0:
            y = random.randint(-h - range_between * i, -1 * width_of_rect - 140)
        else:
            y = random.randint(-h - range_between * i * 2, rects[i - 1][1] - range_between)
        rects.append([x, y])
        Platform(x, y, height_of_rect, width_of_rect, 5, color)
    # генерация монстров
    for i in range(7):
        x = random.randint(0, w - w_of_monster)
        y = random.randint(-2000, -h - 300)
        AnimatedSprite(load_image("monsters.png"), 8, 1, x, y)


def first_level():
    global count, FPS, x_pos, y_pos, boiler_count, z, pause, p, n
    flag = True
    # pygame.mouse.set_visible(False)
    heartimg = pygame.transform.scale(load_image('heart.png'), (55, 55))
    forest = pygame.transform.scale(load_image('triredd.jpg'), (w + 350, h + 550))
    intro_text = ['PAUSE']
    fon = pygame.transform.scale(load_image('grey_pause.png'), (w, h))
    font = pygame.font.Font(None, 80)
    while running:
        text_coord = h // 2 - 30
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and p % 2 == 0:
                pause = True
                for line in intro_text:
                    string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))
                    intro_rect = string_rendered.get_rect()
                    intro_rect.x = 300
                    intro_rect.top = text_coord
                    screen.blit(string_rendered, intro_rect)
                screen.blit(fon, (0, 0))
                p += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and p % 2 != 0:
                pause = False
                p += 1

        if not pause:
            if count % 1000 == 0 and FPS < 110:
                FPS += 3
            count += 8
            n += 1
            if n % 10 == 0:
                monster_sprites.update()

            if pygame.key.get_pressed()[275]:
                mario_sprite.update('left')
            elif pygame.key.get_pressed()[276]:
                mario_sprite.update('right')
            elif pygame.key.get_pressed()[274]:
                mario_sprite.update('up')
            elif pygame.key.get_pressed()[273]:
                mario_sprite.update('down')

            if boiler_count > 200 and flag:
                boiler_count -= 7
            else:
                boiler_count += 7
            if boiler_count < 200:
                flag = False

            all_sprites.update()
            screen.blit(forest, (-150, 0))
            screen.blit(boiler, (0, boiler_count))
            if boiler_count > h:
                mario_sprite.draw(screen)
            mario_sprite.update(1)
            all_sprites.draw(screen)
            monster_sprites.draw(screen)
            z += 1
            if z % 5 == 0:
                indent_from_right = 55
                shaking = 1
            else:
                indent_from_right = 53
                shaking = 0
            for i in range(count_of_hearts + 1):
                screen.blit(heartimg, (w - indent_from_right, shaking))
                indent_from_right += 60
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def main():
    intro_text = ['Побег из ада', 'Начать игру']
    if count_of_hearts == 0:
        game_overing()
    fon = pygame.transform.scale(load_image('hell.jpg'), (w, h))
    screen.fill((219, 233, 230))
    screen.blit(fon, (0, 0))
    font_intr = pygame.font.Font(None, 60)
    font_basic = pygame.font.Font(None, 40)
    text_coord = h // 2 - 180
    k = 0

    for line in intro_text:
        if k == 0:
            string_rendered = font_intr.render(line, 1, pygame.Color('white'))
        else:
            string_rendered = font_basic.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        if k == 0:
            intro_rect.x = 270
            text_coord += 80
        elif k == 1:
            intro_rect.x = 320
            text_coord += 40
        else:
            text_coord += 20
            intro_rect.x = 200
        k += 1
        intro_rect.top = text_coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 315 < event.pos[0] < 490 and 280 < event.pos[1] < 310:
                    intro_first_level()
        pygame.display.flip()
        clock.tick(FPS)


def intro_first_level():
    global count_of_hearts
    pygame.mouse.set_visible(False)
    # intro_text = []
    text = pygame.Surface((w, h))
    text.set_alpha(0)
    intro_text = ['Начало испытаний начинается', 'С АДСКОГО КОТЛА', 'Правила игры такие',
                  'Огибайте препятствия и доберитесь до поверхности', 'Постарайтесь не умереть, у вас 3 попытки']
    if count_of_hearts == 0:
        game_overing()
    fon = pygame.transform.scale(load_image('fir.jpg'), (w + 20, h + 20))
    screen.fill((219, 233, 230))
    screen.blit(fon, (-10, 0))
    font_intr = pygame.font.Font(None, 60)
    font_basic = pygame.font.Font(None, 35)
    text_coord = h // 2 - 180

    k = 0

    for line in intro_text:
        if k == 0 or k == 1 or k == 2:
            string_rendered = font_intr.render(line, 1, pygame.Color(180, 180, 180))
        else:
            string_rendered = font_basic.render(line, 1, pygame.Color(180, 180, 180))
        intro_rect = string_rendered.get_rect()
        if k == 0:
            intro_rect.x = 100
            text_coord += 80
        elif k == 1 or k == 2:
            intro_rect.x = 220
            text_coord += 40
        else:
            intro_rect.x = 100
            text_coord += 20
        string_rendered = font_intr.render(line, 1, pygame.Color(180, 180, 180))
        intro_rect = string_rendered.get_rect()
        k += 1
        intro_rect.top = text_coord
        text_coord += intro_rect.height
        text.blit(string_rendered, intro_rect)
    place = h
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                count_of_hearts -= 1
                pushing()
                first_level()
        screen.blit(text, (0, place))
        if place <= 0:
            place = 0
        else:
            place -= 1
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    global count_of_hearts
    intro_text = ["Вы угодили в кипящий котел!", 'Правила игры такие',
                  'Огибайте препятствия и доберитесь до поверхности',
                  'Постарайтесь не умереть, у вас 3 попытки', 'Кликните любой клавишей']
    if count_of_hearts == 0:
        game_overing()
    fon = pygame.transform.scale(load_image('ruin.jpg'), (w, h + 50))
    screen.fill((219, 233, 230))
    screen.blit(fon, (0, 0))
    font_intr = pygame.font.Font(None, 58)
    font_basic = pygame.font.Font(None, 30)
    font_click = pygame.font.Font(None, 19)
    text_coord = h // 2 - 160
    k = 0

    for line in intro_text:
        if k == 0:
            string_rendered = font_intr.render(line, 1, pygame.Color(180, 180, 170))
        elif line == intro_text[-1]:
            string_rendered = font_click.render(line, 1, pygame.Color(200, 180, 190))
        else:
            string_rendered = font_basic.render(line, 1, pygame.Color(180, 180, 170))
        intro_rect = string_rendered.get_rect()
        if k == 0:
            intro_rect.x = 100
            text_coord += 80
        elif k == 1:
            intro_rect.x = 280
            text_coord += 40
        elif line == intro_text[-1]:
            text_coord += 150
            intro_rect.x = 300
        else:
            intro_rect.x = 140
            text_coord += 20
        k += 1
        intro_rect.top = text_coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if count_of_hearts == 0:
                    game_overing()
                else:
                    count_of_hearts -= 1
                    pushing()
                    first_level()
        pygame.display.flip()
        clock.tick(FPS)


def game_overing():
    image = pygame.transform.scale(load_image('overing.png'), (w, h))
    x_poss = -800
    y_poss = 0
    v = 400
    runningg = True
    screen.blit(image, (x_poss, y_poss))
    while runningg:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mouse.set_visible(True)
                hearts()
                main()
        screen.fill((0, 0, 0))
        if x_poss < 0:
            x_poss += v * clock.tick() / 1000
        screen.blit(image, (int(x_poss), y_poss))
        pygame.display.flip()


main()