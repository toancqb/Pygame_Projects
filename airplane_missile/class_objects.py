import pygame
import random
import os.path
import time
from define import *

class Player(pygame.sprite.Sprite):
    move_up_sound = None
    move_down_sound = None
    def __init__(self, move_up_sound, move_down_sound, ):
        super(Player, self).__init__()
        self.move_up_sound = move_up_sound
        self.move_down_sound = move_down_sound
        self.surf = pygame.image.load(os.path.join("srcs","jet.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                100,
                SCREEN_HEIGHT/2,
            )
        )

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -PLAYER_SPEED)
            #self.move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, PLAYER_SPEED)
            #self.move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        #self.surf = pygame.Surface((20, 10))
        #self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load(os.path.join("srcs","missile.png")).convert()
        self.surf = pygame.transform.scale(self.surf, (30, 15)).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)

    def update(self):
        global SCORE
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            SCORE[0] = SCORE[0] + 1
            self.kill()

class Gold(pygame.sprite.Sprite):
    def __init__(self):
        super(Gold, self).__init__()
        self.surf = pygame.image.load(os.path.join("srcs","coin_gold.png"))
        self.surf = pygame.transform.scale(self.surf, (32, 32))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.surf = pygame.image.load(os.path.join("srcs","boss.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH/4, SCREEN_WIDTH),
                0,
            )
        )
        self.speed = random.randint(ENEMY_SPEED_MAX/4, ENEMY_SPEED_MAX)

    def update(self):
        global SCORE
        n = random.randint(0, 20)
        self.rect.move_ip(-self.speed - n, self.speed)
        if self.rect.top > SCREEN_HEIGHT or self.rect.right <= 0:
            SCORE[0] = SCORE[0] + 10
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(os.path.join("srcs","cloud.png")).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = CLOUD_SPEED

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(Explosion, self).__init__()
        self.surf = pygame.image.load(os.path.join("srcs", "explosion2.png"))
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        self.rect = rect
        self.timer = 10 # after 10 frames, it will be destroyed
        self.speed = BULLET_SPEED

    def process(self):
        if self.timer < 0:
            self.kill()

    def update_timer(self):
        self.timer = self.timer - 1

    def update(self):
        self.rect.move_ip(-self.speed, 0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load(os.path.join("srcs", "bullet.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = rect
        self.speed = BULLET_SPEED

#    def cp_rect(self, rect):
#        return (rect[0], rect[1], rect[2], rect[3],)

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
