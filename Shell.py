import pygame
import random
from technical_function import load_image
from settings import shell_sprites
from Object import Object

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