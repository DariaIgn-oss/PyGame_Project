import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, image, sprite_group, widht=0, height=0):
        super().__init__(sprite_group)
        self.image = image
        self.rect = self.image.get_rect()
        if widht != 0 or height != 0:
            self.rect = pygame.Rect(x, y, 8, 46)
        self.rect.x, self.rect.y = x, y