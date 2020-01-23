from engine import engine
from settings import *
from technical_function import *


def start():
    pygame.mixer.music.load('music\\third_level.mp3')
    pygame.mixer.music.play()
    global FPS, clock, activity
    fon = load_image('headpiece2.png')
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                engine()
        pygame.display.flip()
        clock.tick(FPS)


# start()
