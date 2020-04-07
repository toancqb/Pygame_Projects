import pygame
import random
import time
from define import *
from tools import *
from objects_class import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        snake = Snake()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        pass
                    if event.key == K_DOWN:
                        pass
                    if event.key == K_LEFT:
                        pass
                    if event.key == K_RIGHT:
                        pass
                    if event.key == K_ESCAPE:
                        running = False
            pressed_keys = pygame.key.get_pressed()


            self.draw_board(None, None, None)
            self.screen.blit(snake.surf, snake.rect)
            snake.update(pressed_keys)

            pygame.display.flip()
            self.clock.tick(GAME_SPEED)


        pygame.quit()

    def draw_board(self, lst_snake, fruit, wall):
        self.screen.fill(BLACK)

        # if lst_snake != []:
        #     for i in lst_snake:
        #         pygame.draw.rect(self.screen, GREEN, )



if __name__ == '__main__':
    t = Game()
