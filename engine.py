import pygame
from technical_function import *
from Objects import Mist, Sceleton, start_generate_platform
from settings import screen, FPS, clock, platforms, sceleton_sprite, platform_sprites, mist_sprite, shell_sprites, \
    enemy_sprites, activity, cameray, generation
from victory import victory


def engine():
    global FPS, clock, activity, cameray, generation
    start_generate_platform()
    Sceleton(platforms[1][0], platforms[1][-1] - 45)
    Mist()
    pause = False
    image_fon = load_image('fon.png')
    y_pos = -1200 # начальная позиция
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
            if not activity and event.type == pygame.MOUSEBUTTONDOWN and generation:
                activity = True
                pause = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = True
        screen.fill((0, 0, 0))
        screen.blit(image_fon, (0, y_pos))
        platform_sprites.draw(screen)
        sceleton_sprite.draw(screen)
        enemy_sprites.draw(screen)
        shell_sprites.draw(screen)
        screen.blit(arrow_image, (pos))
        if activity:
            sceleton_sprite.update()
            platform_sprites.update()
            enemy_sprites.update()
            shell_sprites.update()
            if y_pos < 0:
                y_pos += cameray
                mist_sprite.draw(screen)
                mist_sprite.update()
            else:
                victory()
                generation = False
                activity = False
            clock.tick(FPS)
        if pause and generation:
            activity = False
            screen.blit(image_pause, (0, 0))
        pygame.display.flip()