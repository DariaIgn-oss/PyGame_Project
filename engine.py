import pygame
from technical_function import *
from Sceleton import Sceleton
from Mist import Mist
from Platform import start_generate_Platform
from settings import screen, FPS, clock, platforms, sceleton_sprite, platform_sprites, mist_sprite, shell_sprites, \
    enemy_sprites, activity, cameray, generation


def engine():
    global FPS, clock, activity, cameray
    start_generate_Platform()
    Sceleton(platforms[1][0], platforms[1][-1] - 45)
    Mist()
    pause = False
    image_fon = load_image('fon1.png')
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
            sceleton_sprite.update()
            platform_sprites.update()
            enemy_sprites.update()
            shell_sprites.update()
            if y_pos < 0:
                y_pos += cameray
                mist_sprite.update()
            else:
                mist_sprite.kill()
                generation = False
            clock.tick(FPS)
        if pause:
            activity = False
            screen.blit(image_pause, (0, 0))
        pygame.display.flip()