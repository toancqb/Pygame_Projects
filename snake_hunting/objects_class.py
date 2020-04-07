import pygame
import random
from define import *
from tools import *

class Snake(pygame.sprite.Sprite):

    def __init__(self):
        super(Snake, self).__init__()
        self.surf = pygame.Surface((SQ_SIZE,SQ_SIZE))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect()
        self.goto = (SQ_SIZE, 0)

    def update(self, pressed_keys):
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
            self.rect.left = SCREEN_WIDTH - SQ_SIZE
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.top < 0:
            self.rect.top = SCREEN_HEIGHT - SQ_SIZE
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = 0
