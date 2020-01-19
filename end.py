from technical_function import *
from settings import screen


def end():
    global FPS, clock, activity
    fon = load_image('land.png')
    screen.blit(fon, (0, 0))
    activity = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()