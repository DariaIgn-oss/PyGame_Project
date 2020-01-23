import pygame
import random
from settings import *
from game_over import game_over
from technical_function import load_image

clock = pygame.time.Clock()


class ObstacleMain(pygame.sprite.Sprite):
    def __init__(self, group, x, y, sheet, columns, rows):
        self.speed = speed_score.speed
        self.count_time = 0
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x, y)
        self.width = self.image.get_size()[0]
        for i in objects_sprites:
            while pygame.sprite.collide_mask(self, i):
                self.rect.x += 10
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
        self.rect = self.rect.move(-self.speed, 0)
        if self.rect.x < -self.width:
            self.remove(objects_sprites)
            speed_score.score += 10
        self.speed = speed_score.speed
        self.property()

    def property(self):
        pass


class Obstacle_4(ObstacleMain):
    def __init__(self, x, y):
        y = 440
        super().__init__(objects_sprites, x, y, load_image(r'Obstacles\4.png'), 1, 1)

    def property(self):
        self.random_shoot_coord = random.randint(300, 500)
        if self.rect.x > self.random_shoot_coord:
            self.shoot = False
        if self.rect.x < self.random_shoot_coord and not self.shoot:
            Spear(self.rect.x, self.rect.y)
            self.shoot = True


class Obstacle_2(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(objects_sprites, x, y, load_image(r'Obstacles\2.png'), 4, 1)

    def property(self):
        if len(self.frames) < 6:
            self.frames.append(load_image(r'Obstacles\22.png'))
            self.frames.append(load_image(r'Obstacles\23.png'))


class Obstacle_3(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(objects_sprites, x, y, load_image(r'Obstacles\3.png'), 5, 1)

    def property(self):
        self.rect = self.rect.move(-10, 0)


class Obstacle(ObstacleMain):
    def __init__(self, x, y):
        super().__init__(objects_sprites, x, y, load_image(r'Obstacles\1.png'), 5, 1)

    def property(self):
        pass


class Border(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(border_sprite)
        self.image = pygame.Surface([0, 480])
        self.rect = pygame.Rect(0, 490, 800, 100)


class Spear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(objects_sprites)
        self.image = load_image('spear.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.speed_y = 2

    def update(self, *args):
        self.rect.x -= speed_score.speed + speed_score.speed // 2
        if self.speed_y >= 0:
            self.rect.y -= (self.speed_y ** 3)
        else:
            self.rect.y += (self.speed_y ** 2)
        if self.rect.x < -self.image.get_size()[0]:
            self.remove(objects_sprites)


# Daria's Objects


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, image, sprite_group, widht=0, height=0):
        super().__init__(sprite_group)
        self.image = image
        self.rect = self.image.get_rect()
        if widht != 0 or height != 0:
            self.rect = pygame.Rect(x, y, 8, 46)
        self.rect.x, self.rect.y = x, y


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


def start_generate_platform():
    global HEIGHT, platforms
    on = HEIGHT
    while on > -200:
        x_coord = random.randint(0, 720)
        platforms.append([x_coord, on])
        Platform(x_coord, on)
        on -= 40


class Platform(Object):
    platforms_image = [load_image('platform1.png', (255, 255, 255)), load_image('platform2.png')]

    def __init__(self, x=-80, y=-18):
        global platforms
        divider = random.randint(1, 11)
        if count_platforms > 1 and count_platforms % 10 == 0:
            Platform.platforms_image.append(load_image('platform3.png'))
        if count_platforms > 10 and count_platforms % divider == 0:
            Enemy(platforms[-1][0] + 5, platforms[-1][1] - 35)
        if count_platforms > 500:
            Platform.platforms_image = [load_image('platform3.png')]
        platform_image = random.choice(Platform.platforms_image)
        super().__init__(x, y, platform_image, platform_sprites)

    def update(self):
        global platforms, cameray, count_platforms, generation
        self.rect = self.rect.move(0, cameray)
        check = platforms[1][1] + cameray
        platforms[1][1] += cameray
        global HEIGHT
        if check > HEIGHT and generation:
            platforms.append([random.randint(0, 720), platforms[-1][1] - 40])
            Platform(platforms[-1][0], platforms[-1][1])
            platforms.pop(0)
            count_platforms += 1

        if count_platforms == 1000:
            end()
