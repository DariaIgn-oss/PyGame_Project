import random
from technical_function import load_image
from settings import platforms, platform_sprites, score_text, cameray, HEIGHT
from Object import Object
from Enemy import Enemy

def start_generate_Platform():
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
        if int(score_text) % 10 == 0:
            Platform.platforms_image.append(load_image('platform3.png'))
        if int(score_text) > 10 and int(score_text) % divider == 0:
            Enemy(platforms[-1][0] + 5, platforms[-1][1] - 35)
        if int(score_text) > 300:
            Platform.platforms_image = [load_image('platform3.png')]
        platform_image = random.choice(Platform.platforms_image)
        super().__init__(x, y, platform_image, platform_sprites)

    def update(self):
        global platforms, cameray
        self.rect = self.rect.move(0, cameray)
        check = platforms[1][1] + cameray
        platforms[1][1] += cameray
        global HEIGHT
        if check > HEIGHT:
            platforms.append([random.randint(0, 720), platforms[-1][1] - 40])
            Platform(platforms[-1][0], platforms[-1][1])
            platforms.pop(0)