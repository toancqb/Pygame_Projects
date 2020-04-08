import pygame
import random
import os.path
from define import *
from tools import *

class Snake(pygame.sprite.Sprite):

    def __init__(self, rect, index, goto, scr_width):
        super(Snake, self).__init__()
        self.surf = pygame.Surface((SQ_SIZE,SQ_SIZE))
        self.surf.fill(WHITE)
        pygame.draw.rect(self.surf,GREEN, (1, 1, SQ_SIZE-2, SQ_SIZE-2))
        self.rect = self.surf.get_rect(center=(rect[0]+SQ_SIZE/2,rect[1]+SQ_SIZE/2))
        self.goto = goto
        self.index = index
        self.SCREEN_WIDTH = scr_width

    def update2(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.goto = (0, -SQ_SIZE)
        if pressed_keys[K_DOWN]:
            self.goto = (0, SQ_SIZE)
        if pressed_keys[K_LEFT]:
            self.goto = (-SQ_SIZE, 0)
        if pressed_keys[K_RIGHT]:
            self.goto = (SQ_SIZE, 0)

        self.rect.move_ip(self.goto[0],self.goto[1])

        if self.rect.left < 0:
            self.rect.left = self.SCREEN_WIDTH - SQ_SIZE
        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.top < 0:
            self.rect.top = SCREEN_HEIGHT - SQ_SIZE
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = 0

    def update3(self, pressed_keys):
        if pressed_keys[K_w]:
            self.goto = (0, -SQ_SIZE)
        if pressed_keys[K_s]:
            self.goto = (0, SQ_SIZE)
        if pressed_keys[K_a]:
            self.goto = (-SQ_SIZE, 0)
        if pressed_keys[K_d]:
            self.goto = (SQ_SIZE, 0)

        self.rect.move_ip(self.goto[0],self.goto[1])

        if self.rect.left < 0:
            self.rect.left = self.SCREEN_WIDTH - SQ_SIZE
        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.top < 0:
            self.rect.top = SCREEN_HEIGHT - SQ_SIZE
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = 0

    def update(self):
        self.rect.move_ip(self.goto[0],self.goto[1])

        if self.rect.left < 0:
            self.rect.left = self.SCREEN_WIDTH - SQ_SIZE
        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.top < 0:
            self.rect.top = SCREEN_HEIGHT - SQ_SIZE
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = 0

class Snakes(pygame.sprite.Sprite):

    def __init__(self, all_sprites, scr_width):
        super(Snakes, self).__init__()
        self.SCREEN_WIDTH = scr_width
        self.all_sprites = all_sprites
        self.head = Snake((0,0), 1, (SQ_SIZE, 0), self.SCREEN_WIDTH)
        self.group = [self.head]
        self.len = 1



    def add_snake(self):
        rect = self.head.rect
        rect = (rect[0]+self.head.goto[0], rect[1]+self.head.goto[1], rect[2], rect[3])
        new_snake = Snake(rect, self.len, self.head.goto, self.SCREEN_WIDTH)
        self.group.insert(0, new_snake)
        self.len += 1
        self.head = new_snake
        self.all_sprites.add(new_snake)

    def update(self, pressed_keys, opt):
        i = self.len-1
        while i > 0:
            self.group[i].goto = self.group[i-1].goto
            i -= 1
        if opt == 1:
            self.head.update2(pressed_keys)
        else:
            self.head.update3(pressed_keys)
        i = 1
        while i < self.len:
            self.group[i].update()
            i += 1

class Wall(pygame.sprite.Sprite):

    def __init__(self, scr_width):
        super(Wall, self).__init__()
        self.SCREEN_WIDTH = scr_width
        self.surf = pygame.Surface((SQ_SIZE*10,SQ_SIZE*2))
        self.surf.fill(ORANGE)
        pygame.draw.rect(self.surf,WHITE, (2, 2, 10*SQ_SIZE-4, 2*SQ_SIZE-4))
        self.rect = self.surf.get_rect(
            center = (self.SCREEN_WIDTH/2,
                      SCREEN_HEIGHT/2)
        )


class Fruit(pygame.sprite.Sprite):
    def __init__(self, scr_width):
        super(Fruit, self).__init__()
        self.SCREEN_WIDTH = scr_width
        self.surf = pygame.Surface((SQ_SIZE,SQ_SIZE))
        self.surf.fill(ORANGE)
        pygame.draw.rect(self.surf,RED, (2, 2, SQ_SIZE-4, SQ_SIZE-4))
        self.rect = self.surf.get_rect(
            center = (random.randint(SQ_SIZE,self.SCREEN_WIDTH-SQ_SIZE),
                      random.randint(SQ_SIZE,SCREEN_HEIGHT-SQ_SIZE))
        )


class Explosion(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(Explosion, self).__init__()
        self.surf = pygame.image.load(os.path.join("srcs", "explosion2.png"))
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        self.rect = rect

class Cloud(pygame.sprite.Sprite):
    def __init__(self, scr_width):
        super(Cloud, self).__init__()
        self.SCREEN_WIDTH = scr_width
        self.surf = pygame.image.load(os.path.join("srcs","cloud.png")).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(self.SCREEN_WIDTH+20, self.SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 4

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
