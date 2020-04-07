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
        snakes = Snakes()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
            pressed_keys = pygame.key.get_pressed()

            self.draw_board(None, None, None)
            for snake in snakes.group:
                snake.update(pressed_keys)
                self.screen.blit(snake.surf, snake.rect)

            pygame.display.flip()
            self.clock.tick(GAME_SPEED)


        pygame.quit()

    def draw_board(self, lst_snake, fruit, wall):
        self.screen.fill(BLACK)

        # for i in range(NX):
        #     for j in range(NY):
        #         pygame.draw.rect(self.screen, BLACK, (i*SQ_SIZE+1, j*SQ_SIZE+1, SQ_SIZE-2, SQ_SIZE-2))



if __name__ == '__main__':
    t = Game()
