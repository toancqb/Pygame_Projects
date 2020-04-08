import pygame
import random
import time
import os.path
from define import *
from tools import *
from objects_class import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.ADDFRUIT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDFRUIT, 50000)

        fruits = pygame.sprite.Group()
        fruits.add(Fruit())
        # snakes_sprite_group = pygame.sprite.Group()

        snakes = Snakes()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()

        wall = Wall()
        fruits.add(wall)
        opt = True
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == self.ADDFRUIT:
                    new_fruit = Fruit()
                    fruits.add(new_fruit)
            pressed_keys = pygame.key.get_pressed()

            self.draw_board(None, None, None)
            if opt:
                snakes.update(pressed_keys)
            for snake in snakes.group:

                for fruit in fruits:
                    if pygame.sprite.collide_rect(snake, fruit):
                        fruit.kill()
                        new_fruit = Fruit()
                        fruits.add(new_fruit)
                        snakes.add_snake()
                self.screen.blit(snake.surf, snake.rect)

            for fruit in fruits:
                self.screen.blit(fruit.surf, fruit.rect)
            i = 1
            while i < snakes.len:
                if snakes.head.rect.colliderect(snakes.group[i]):
                    expl = Explosion(snakes.head.rect.copy())
                    opt = False
                    break
                i += 1
            if not opt:
                self.screen.blit(expl.surf, expl.rect)
            pygame.display.flip()
            self.clock.tick(GAME_SPEED)


        pygame.quit()

    def draw_board(self, lst_snake, fruit, wall):
        self.screen.fill(BLACK)


if __name__ == '__main__':
    t = Game()
