import pygame
import random
from define import *
from tools import *

class Snake(pygame.sprite.Sprite):

    def __init__(self, rect):
        super(Snake, self).__init__()
        self.surf = pygame.Surface((SQ_SIZE,SQ_SIZE))
        self.surf.fill(WHITE)
        pygame.draw.rect(self.surf,GREEN, (1, 1, SQ_SIZE-2, SQ_SIZE-2))
        self.rect = self.surf.get_rect(center=(rect[0]+SQ_SIZE/2,rect[1]+SQ_SIZE/2))
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

class Snakes(pygame.sprite.Sprite):

    def __init__(self):
        super(Snakes, self).__init__()
        self.head = Snake((0,0))
        self.group = [self.head]


    def add_snake(self):
        rect = self.head.rect
        rect = (rect[0]+self.head.goto[0], rect[1]+self.head.goto[1], rect[2], rect[3])
        new_snake = Snake(rect)
        self.group.insert(0, new_snake)
        self.head = new_snake

    def update(self, pressed_keys):
        pass
