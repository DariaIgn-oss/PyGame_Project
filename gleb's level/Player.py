import pygame
from SettingsGame import player_sprite, border_sprite, player_image, all_sprites
from OddFunctions import terminate


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sheet, columns, rows):
        super().__init__(player_sprite)
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = 2
        self.jump = False
        self.walk = []
        self.jump_and_fall = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.walk[self.cur_frame]
        self.rect = self.rect.move(pos_x, pos_y)

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
        if not self.jump:
            self.cur_frame = (self.cur_frame + 1) % len(self.walk)
            self.image = self.walk[self.cur_frame]
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
        for i in all_sprites:
            if pygame.sprite.collide_mask(self, i):
                terminate()
