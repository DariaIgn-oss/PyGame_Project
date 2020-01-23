import pygame
import sys
import os
from settings import objects_sprites, speed_score


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


def restart_level3():
    objects_sprites, speed_score
    for i in objects_sprites:
        objects_sprites.remove(i)
    speed_score.speed = 10
    speed_score.score = 0
