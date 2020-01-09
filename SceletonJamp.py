import pygame
import random
import os
import sys

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
platforms = []
platform_sprites = pygame.sprite.Group()
mario_sprite = pygame.sprite.Group()

cameray = 1
score = 1
score_text = '1'
font = pygame.font.Font(None, 36)

FPS = 25
clock = pygame.time.Clock()

def terminate():
    pygame.quit()
    sys.exit()


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


class Mario(pygame.sprite.Sprite):
    skeleton_image = load_image('skeleton.png')
    skeleton_jump = [load_image('skeleton1.png'), load_image('skeleton2.png'), load_image('skeleton3.png')]

    def __init__(self, x, y):
        super().__init__(mario_sprite)
        self.image = Mario.skeleton_image
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, 8, 46)
        self.isJump = False
        self.jump_count = 13
        # global mario_coord
        # mario_coord.append(x, y)

    def update(self, x=0):
        global WIDTH, HEIGHT, cameray, score, score_text, font

        if self.isJump:
            if self.jump_count >= 0:
                self.rect = self.rect.move(0, -self.jump_count)
                self.jump_count -= 1
                score += 1
            elif self.jump_count < 0:
                self.isJump = False
                self.jump_count = 13
                self.image = Mario.skeleton_jump[2]
                score -= 3
        else:
            score -= 1

        if pygame.sprite.spritecollideany(self, platform_sprites) or self.isJump:
            self.isJump = True
            self.image = Mario.skeleton_jump[0]
        else:
            self.rect = self.rect.move(0, self.jump_count)
            self.image = Mario.skeleton_jump[2]

        if x != 0:
            if 0 < x < WIDTH - 24:
                self.rect.x = x

        if self.rect.y >= HEIGHT:
            terminate()

        if int(score_text) < score:
            score_text = str(score)

        string_rendered = font.render(score_text, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = 0, 0
        screen.blit(string_rendered, intro_rect)

class Platform(pygame.sprite.Sprite):
    platforms_image = [load_image('platform1.png'), load_image('platform2.png')]

    def __init__(self, x=-80, y=-18):
        global score_text
        super().__init__(all_sprites, platform_sprites)
        if int(score_text) % 50 == 0:
            Platform.platforms_image.append(load_image('platform3.png'))
        if int(score_text) > 400:
            Platform.platforms_image = [load_image('platform3.png')]
        platform_image = random.choice(Platform.platforms_image)
        self.image = platform_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        global platforms, cameray
        self.rect = self.rect.move(0, cameray)
        check = platforms[1][1] + cameray
        platforms[1][1] += cameray
        global HEIGHT
        if check > HEIGHT:
            platforms.append([random.randint(0, 720), platforms[-1][1] - 20])
            Platform(platforms[-1][0], platforms[-1][1])
            platforms.pop(0)


def start_generate_Platform():
    global HEIGHT, platforms
    on = HEIGHT
    while on > -100:
        x_coord = random.randint(0, 720)
        platforms.append([x_coord, on])
        Platform(x_coord, on)
        on -= 20


def engine():
    global FPS, clock, score_text
    start_generate_Platform()
    Mario(platforms[1][0], platforms[1][-1] - 45)
    activity = False
    pause = False
    image_fon = load_image('fon1.png')
    image_pause = load_image('pause.png')
    while True:
        for event in pygame.event.get():
            pygame.mouse.set_visible(False)
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION and activity:
                mario_sprite.update(event.pos[0])
            if not activity and event.type == pygame.MOUSEBUTTONDOWN:
                activity = True
                pause = False
            elif event.type == pygame.KEYDOWN and event.key == 32:
                pause = True
        screen.fill((0, 0, 0))
        screen.blit(image_fon, (0, 0))
        all_sprites.draw(screen)
        mario_sprite.draw(screen)
        if activity:
            mario_sprite.update()
            all_sprites.update()
            platform_sprites.update()
            clock.tick(FPS)
        if pause:
            activity = False
            screen.blit(image_pause, (0, 0))
        pygame.display.flip()


def start():
    global FPS, clock, score
    fon = load_image('headpiece.png')
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                engine()
        pygame.display.flip()
        clock.tick(FPS)


start()