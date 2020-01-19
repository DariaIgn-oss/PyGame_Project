import pygame
import random
import os
import sys

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)

platforms = []
platform_sprites = pygame.sprite.Group()
sceleton_sprite = pygame.sprite.Group()
mist_sprite = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
shell_sprites = pygame.sprite.Group()

cameray = 1
score = 1
score_text = '1'
font = pygame.font.Font(None, 36)

FPS = 25
clock = pygame.time.Clock()

activity = False


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


def start_generate_Platform():
    global HEIGHT, platforms
    on = HEIGHT
    while on > -200:
        x_coord = random.randint(0, 720)
        platforms.append([x_coord, on])
        Platform(x_coord, on)
        on -= 40


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, image, sprite_group, widht=0, height=0):
        super().__init__(sprite_group)
        self.image = image
        self.rect = self.image.get_rect()
        if widht != 0 or height != 0:
            self.rect = pygame.Rect(x, y, 8, 46)
        self.rect.x, self.rect.y = x, y


class Sceleton(Object):
    skeleton_image = load_image('skeleton.png')
    skeleton_jump = [load_image('skeleton1.png'), load_image('skeleton2.png'), load_image('skeleton3.png')]
    game_over = False

    def __init__(self, x, y):
        super().__init__(x, y, Sceleton.skeleton_image, sceleton_sprite, 8, 46)
        self.isJump = False
        self.jump_count = 13

    def update(self, x=0, shot=False):
        global WIDTH, HEIGHT, cameray, score, score_text, font

        if self.isJump:
            if self.jump_count >= 0:
                self.rect = self.rect.move(0, -self.jump_count)
                self.jump_count -= 1
                score += 1
            elif self.jump_count < 0:
                self.isJump = False
                self.jump_count = 13
                self.image = Sceleton.skeleton_jump[2]
                score -= 5
        else:
            score -= 1

        if (pygame.sprite.spritecollideany(self, platform_sprites) or self.isJump) and not Sceleton.game_over:
            self.isJump = True
            self.image = Sceleton.skeleton_jump[0]
        else:
            self.rect = self.rect.move(0, self.jump_count)
            self.image = Sceleton.skeleton_jump[2]

        if pygame.sprite.spritecollideany(self, enemy_sprites):
            Sceleton.game_over = True

        if x != 0:
            if 0 < x < WIDTH - 24:
                self.rect.x = x

        if shot:
            Shell(self.rect.x, self.rect.y)

        if self.rect.y + 25 >= HEIGHT:
            game_over()

        if int(score_text) < score:
            score_text = str(score)

        string_rendered = font.render(score_text, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = 0, 0
        screen.blit(string_rendered, intro_rect)


class Shell(Object):
    shell_image = load_image('bone3.png')

    def __init__(self, x, y):
        self.image_orig = Shell.shell_image
        super().__init__(x, y, Shell.shell_image, shell_sprites)
        self.rot = 0
        self.rot_speed = random.randrange(-16, 16)

    def update(self):
        self.rect = self.rect.move(0, -10)
        self.rot = (self.rot + self.rot_speed) % 360
        self.image = pygame.transform.rotate(self.image_orig, self.rot)


class Platform(Object):
    platforms_image = [load_image('platform1.png', (255, 255, 255)), load_image('platform2.png')]

    def __init__(self, x=-80, y=-18):
        global platforms
        divider = random.randint(1, 11)
        if int(score_text) % 10 == 0:
            Platform.platforms_image.append(load_image('platform3.png'))
        if int(score_text) > 10 and int(score_text) % divider == 0:
            Enemy(platforms[-1][0] + 5, platforms[-1][1] - 35)
        if int(score_text) > 300:
            Platform.platforms_image = [load_image('platform3.png')]
        platform_image = random.choice(Platform.platforms_image)
        super().__init__(x, y, platform_image, platform_sprites)

    def update(self):
        global platforms, cameray
        self.rect = self.rect.move(0, cameray)
        check = platforms[1][1] + cameray
        platforms[1][1] += cameray
        global HEIGHT
        if check > HEIGHT:
            platforms.append([random.randint(0, 720), platforms[-1][1] - 40])
            Platform(platforms[-1][0], platforms[-1][1])
            platforms.pop(0)


class Mist(Object):
    mist_image = [load_image(f'mist{i}.png') for i in range(1, 9)]
    index = 0

    def __init__(self):
        super().__init__(0, 0, Mist.mist_image[Mist.index], mist_sprite)

    def update(self):
        Mist.index += 1
        if Mist.index == 63:
            Mist.index = 0
        else:
            self.image = Mist.mist_image[Mist.index // 8]


class Enemy(Object):
    enemy_image = load_image('gargoyle.png')

    def __init__(self, x, y):
        global WIDTH
        super().__init__(x, y, Enemy.enemy_image, enemy_sprites)
        self.jump_count = 5
        self.is_Jump = False

    def update(self):
        global WIDTH, cameray, score
        if pygame.sprite.spritecollideany(self, platform_sprites):
            self.is_Jump = True
        else:
            self.rect = self.rect.move(0, self.jump_count)

        if pygame.sprite.spritecollideany(self, shell_sprites):
            self.kill()
            score += 10

        if self.is_Jump:
            if self.jump_count >= 0:
                self.rect = self.rect.move(0, -self.jump_count)
                self.jump_count -= 1
            else:
                self.is_Jump = False
                self.jump_count = 5


def engine():
    global FPS, clock, activity, cameray
    start_generate_Platform()
    Sceleton(platforms[1][0], platforms[1][-1] - 45)
    Mist()
    pause = False
    image_fon = load_image('fon.jpg')
    y_pos = -3600
    image_pause = load_image('pause.png')
    arrow_image = load_image('bone1.png')
    pos = 0, 0
    while True:
        for event in pygame.event.get():
            pygame.mouse.set_visible(False)
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                if activity:
                    sceleton_sprite.update(pos[0])
            if activity and event.type == pygame.MOUSEBUTTONDOWN:
                sceleton_sprite.update(0, True)
            if not activity and event.type == pygame.MOUSEBUTTONDOWN:
                activity = True
                pause = False
            elif event.type == pygame.KEYDOWN and event.key == 32:
                pause = True
        screen.fill((0, 0, 0))
        screen.blit(image_fon, (0, y_pos))
        platform_sprites.draw(screen)
        sceleton_sprite.draw(screen)
        enemy_sprites.draw(screen)
        shell_sprites.draw(screen)
        mist_sprite.draw(screen)
        screen.blit(arrow_image, (pos))
        if activity:
            if y_pos < 0:
                y_pos += cameray
            sceleton_sprite.update()
            platform_sprites.update()
            enemy_sprites.update()
            shell_sprites.update()
            mist_sprite.update()
            clock.tick(FPS)
        if pause:
            activity = False
            screen.blit(image_pause, (0, 0))
        pygame.display.flip()


def start():
    global FPS, clock
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

def game_over():
    global FPS, clock, activity
    fon = load_image('game_over.png')
    screen.blit(fon, (0, 0))
    activity = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


start()
