from settings import sceleton_sprite, platform_sprites, screen
from settings import *
from technical_function import *
from Object import Object
from Shell import Shell
from game_over import game_over


class Sceleton(Object):
    skeleton_image = load_image('skeleton.png')
    skeleton_jump = [load_image('skeleton1.png'), load_image('skeleton2.png'), load_image('skeleton3.png')]
    game_over = False

    def __init__(self, x, y):
        super().__init__(x, y, Sceleton.skeleton_image, sceleton_sprite, 8, 46)
        self.isJump = False
        self.jump_count = 13

    def update(self, x=0, shot=False):
        global WIDTH, HEIGHT, cameray, score, score_text, font

        if self.isJump:
            if self.jump_count >= 0:
                self.rect = self.rect.move(0, -self.jump_count)
                self.jump_count -= 1
                score += 1
            elif self.jump_count < 0:
                self.isJump = False
                self.jump_count = 13
                self.image = Sceleton.skeleton_jump[2]
                score -= 5
        else:
            score -= 1

        if (pygame.sprite.spritecollideany(self, platform_sprites) or self.isJump) and not Sceleton.game_over:
            self.isJump = True
            self.image = Sceleton.skeleton_jump[0]
        else:
            self.rect = self.rect.move(0, self.jump_count)
            self.image = Sceleton.skeleton_jump[2]

        if pygame.sprite.spritecollideany(self, enemy_sprites):
            Sceleton.game_over = True

        if x != 0:
            if 0 < x < WIDTH - 24:
                self.rect.x = x

        if shot:
            Shell(self.rect.x, self.rect.y)

        if self.rect.y + 25 >= HEIGHT:
            game_over()

        if int(score_text) < score:
            score_text = str(score)

        string_rendered = font.render(score_text, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = 0, 0
        screen.blit(string_rendered, intro_rect)