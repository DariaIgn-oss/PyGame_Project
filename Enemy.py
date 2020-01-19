import pygame
from settings import enemy_sprites, shell_sprites, WIDTH, cameray, score, platform_sprites
from technical_function import *
from Object import Object

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
