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
        fr = Fruit()
        fruits.add(fr)
        walls = pygame.sprite.Group()
        wl = Wall()
        walls.add(wl)

        all_sprites = pygame.sprite.Group()
        all_sprites.add(fr)
        all_sprites.add(wl)

        snakes = Snakes(all_sprites)
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()

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

            self.draw_board()
            if opt:
                snakes.update(pressed_keys)
            for snake in snakes.group:
                for fruit in fruits:
                    if pygame.sprite.collide_rect(snake, fruit):
                        fruit.kill()
                        new_fruit = Fruit()
                        fruits.add(new_fruit)
                        all_sprites.add(new_fruit)
                        snakes.add_snake()

                if (snake != snakes.head and snakes.head.rect.colliderect(snake))\
                or pygame.sprite.spritecollideany(snake, walls):
                    expl = Explosion(snakes.head.rect.copy())
                    opt = False
                    break
            for fw in all_sprites:
                self.screen.blit(fw.surf, fw.rect)

            if not opt:
                self.screen.blit(expl.surf, expl.rect)
            pygame.display.flip()
            self.clock.tick(GAME_SPEED)


        pygame.quit()

    def draw_board(self):
        self.screen.fill(BLACK)


if __name__ == '__main__':
    t = Game()
