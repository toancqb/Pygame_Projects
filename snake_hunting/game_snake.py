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

        self.font = pygame.font.SysFont("comicsansms", 35)
        self.font2 = pygame.font.SysFont("comicsansms", 72)

        self.ADDFRUIT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDFRUIT, 50000)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
            opt = self.Menu()
            if opt == 1:
                self.One_Player()
            elif opt == 2:
                self.Multi_Player()
            elif opt == 3:
                self.Snake_Arena()
            elif opt == -1:
                running = False

            self.clock.tick(10)

        pygame.quit()

    def draw_board(self, screen, COLOR):
        screen.fill(COLOR)

    def Menu(self):
        self.screen.fill(BLUE)

        txt = self.font2.render("-= Snake Game =-", True, RED)
        txt_center = (
            SCREEN_WIDTH/2 - txt.get_width() // 2,
            SCREEN_HEIGHT/2 - txt.get_height() // 2
        )

        txt2 = self.font.render("[One Player]", True, GREEN)
        txt2_center = (
            SCREEN_WIDTH/2 - txt2.get_width() // 2,
            SCREEN_HEIGHT/2 + 30
        )
        txt2rect = txt2.get_rect()
        txt3 = self.font.render("[Player 1 vs Player 2]", True, GREEN)
        txt3_center = (
            SCREEN_WIDTH/2 - txt3.get_width() // 2,
            SCREEN_HEIGHT/2 + 60
        )
        txt3rect = txt3.get_rect()

        txt4 = self.font.render("[Snakes Arena]", True, BLACK)
        txt4_center = (
            SCREEN_WIDTH/2 - txt4.get_width() // 2,
            SCREEN_HEIGHT/2 + 90
        )
        txt4rect = txt4.get_rect()

        ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(ADDCLOUD, 2000)

        clouds_decor = pygame.sprite.Group()
        clouds_decor.add(Cloud(SCREEN_WIDTH))
        clouds_decor.add(Cloud(SCREEN_WIDTH))
        option = -1
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_d:
                        option = 3
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pos_clicked = pygame.mouse.get_pos()
                        if check_position(pos_clicked,\
                        SCREEN_WIDTH/2-txt2.get_width(),SCREEN_WIDTH/2+txt2.get_width(),\
                        SCREEN_HEIGHT/2+30-txt2.get_height(),SCREEN_HEIGHT/2+30+txt2.get_height()):
                            option = 1
                            running = False
                        elif check_position(pos_clicked,\
                        SCREEN_WIDTH/2-txt3.get_width(),SCREEN_WIDTH/2+txt3.get_width(),\
                        SCREEN_HEIGHT/2+60-txt3.get_height(),SCREEN_HEIGHT/2+60+txt3.get_height()):
                            option = 2
                            running = False
                        elif check_position(pos_clicked,\
                        SCREEN_WIDTH/2-txt4.get_width(),SCREEN_WIDTH/2+txt4.get_width(),\
                        SCREEN_HEIGHT/2+90-txt4.get_height(),SCREEN_HEIGHT/2+90+txt4.get_height()):
                            option = 3
                            running = False

                if event.type == QUIT:
                    running = False
                if event.type == ADDCLOUD:
                    new_cloud = Cloud(SCREEN_WIDTH)
                    clouds_decor.add(new_cloud)

            clouds_decor.update()
            self.screen.fill(BLUE)

            self.screen.blit(txt, txt_center)
            self.screen.blit(txt2, txt2_center)
            self.screen.blit(txt3, txt3_center)
            self.screen.blit(txt4, txt4_center)

            for entity in clouds_decor:
                self.screen.blit(entity.surf, entity.rect)

            pygame.display.flip()
            self.clock.tick(30)

        return option

    def One_Player(self):
        fruits = pygame.sprite.Group()
        fr = Fruit(SCREEN_WIDTH)
        fruits.add(fr)
        walls = pygame.sprite.Group()
        wl = Wall(SCREEN_WIDTH)
        walls.add(wl)

        all_sprites = pygame.sprite.Group()
        all_sprites.add(fr)
        all_sprites.add(wl)

        snakes = Snakes(all_sprites, SCREEN_WIDTH,(0,0))
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
                    new_fruit = Fruit(SCREEN_WIDTH)
                    fruits.add(new_fruit)
            pressed_keys = pygame.key.get_pressed()

            self.draw_board(self.screen, BLACK)
            if opt:
                snakes.update(pressed_keys, 1)
            for snake in snakes.group:
                for fruit in fruits:
                    if pygame.sprite.collide_rect(snake, fruit):
                        fruit.kill()
                        new_fruit = Fruit(SCREEN_WIDTH)
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

    def Multi_Player(self):
        screen1 = pygame.Surface((SCREEN_WIDTH//2,SCREEN_HEIGHT))
        screen2 = pygame.Surface((SCREEN_WIDTH//2,SCREEN_HEIGHT))
        fruits = pygame.sprite.Group()
        fr = Fruit(SCREEN_WIDTH//2)
        fruits.add(fr)
        walls = pygame.sprite.Group()
        wl = Wall(SCREEN_WIDTH//2)
        walls.add(wl)

        all_sprites = pygame.sprite.Group()
        all_sprites2 = pygame.sprite.Group()
        all_sprites.add(fr)
        all_sprites.add(wl)
        all_sprites2.add(fr)
        all_sprites2.add(wl)

        snakes = Snakes(all_sprites, SCREEN_WIDTH//2, (0,0))
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()

        snakes2 = Snakes(all_sprites2, SCREEN_WIDTH//2, (0,0))
        snakes2.add_snake()
        snakes2.add_snake()
        snakes2.add_snake()
        snakes2.add_snake()

        opt = True
        opt2 = True
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == self.ADDFRUIT:
                    new_fruit = Fruit(SCREEN_WIDTH//2)
                    fruits.add(new_fruit)
            pressed_keys = pygame.key.get_pressed()

            self.draw_board(screen1, BLACK)
            self.draw_board(screen2, BLUE_D)
####################################
            if opt:
                snakes.update(pressed_keys, 2)
            for snake in snakes.group:
                for fruit in fruits:
                    if pygame.sprite.collide_rect(snake, fruit):
                        fruit.kill()
                        new_fruit = Fruit(SCREEN_WIDTH//2)
                        fruits.add(new_fruit)
                        all_sprites.add(new_fruit)
                        all_sprites2.add(new_fruit)
                        snakes.add_snake()

                if (snake != snakes.head and snakes.head.rect.colliderect(snake))\
                or pygame.sprite.spritecollideany(snake, walls):
                    expl = Explosion(snakes.head.rect.copy())
                    opt = False
                    break
            for fw in all_sprites:
                screen1.blit(fw.surf, fw.rect)

            if not opt:
                screen1.blit(expl.surf, expl.rect)
#################################
            if opt2:
                snakes2.update(pressed_keys, 1)
            for snake in snakes2.group:
                for fruit in fruits:
                    if pygame.sprite.collide_rect(snake, fruit):
                        fruit.kill()
                        new_fruit = Fruit(SCREEN_WIDTH//2)
                        fruits.add(new_fruit)
                        all_sprites.add(new_fruit)
                        all_sprites2.add(new_fruit)
                        snakes2.add_snake()

                if (snake != snakes2.head and snakes2.head.rect.colliderect(snake))\
                or pygame.sprite.spritecollideany(snake, walls):
                    expl = Explosion(snakes2.head.rect.copy())
                    opt2 = False
                    break
            for fw in all_sprites2:
                screen2.blit(fw.surf, fw.rect)

            if not opt2:
                screen2.blit(expl.surf, expl.rect)

            self.screen.blit(screen1, (0,0))
            self.screen.blit(screen2, (SCREEN_WIDTH//2,0))
            pygame.display.flip()
            self.clock.tick(GAME_SPEED)

    def Snake_Arena(self):
        fruits = pygame.sprite.Group()
        fr = Fruit(SCREEN_WIDTH)
        fruits.add(fr)
        walls = pygame.sprite.Group()
        wl = Wall(SCREEN_WIDTH)
        walls.add(wl)

        all_sprites = pygame.sprite.Group()
        all_sprites.add(fr)
        all_sprites.add(wl)

        snakes = Snakes(all_sprites, SCREEN_WIDTH,(0,0))
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()
        snakes.add_snake()

        snakes2 = Snakes(all_sprites, SCREEN_WIDTH,(0,SCREEN_HEIGHT-SQ_SIZE))
        snakes2.add_snake()
        snakes2.add_snake()
        snakes2.add_snake()
        snakes2.add_snake()
        snakes2.add_snake()
        snakes2.add_snake()
        snakes2.add_snake()
        snakes2.add_snake()
        snakes2.add_snake()

        sd = False
        sd2 = False
        opt = True
        opt2 = True
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == self.ADDFRUIT:
                    new_fruit = Fruit(SCREEN_WIDTH)
                    fruits.add(new_fruit)
            pressed_keys = pygame.key.get_pressed()

            self.draw_board(self.screen, BLACK)

            if opt:
                snakes.update(pressed_keys, 2)
                for snake in snakes.group:
                    for fruit in fruits:
                        if pygame.sprite.collide_rect(snake, fruit):
                            fruit.kill()
                            new_fruit = Fruit(SCREEN_WIDTH//2)
                            fruits.add(new_fruit)
                            all_sprites.add(new_fruit)
                            snakes.add_snake()

                    if (snake != snakes.head and snakes.head.rect.colliderect(snake))\
                    or pygame.sprite.spritecollideany(snake, walls)\
                    or snakes2.head.rect.colliderect(snake):
                        expl = Explosion(snakes.head.rect.copy())
                        all_sprites.add(expl)
                        sd = True
                        break
            if sd:
                for snake in snakes.group:
                    snake.kill()
                opt, sd = False, False
#################################
            if opt2:
                snakes2.update(pressed_keys, 1)
                for snake in snakes2.group:
                    for fruit in fruits:
                        if pygame.sprite.collide_rect(snake, fruit):
                            fruit.kill()
                            new_fruit = Fruit(SCREEN_WIDTH//2)
                            fruits.add(new_fruit)
                            all_sprites.add(new_fruit)
                            snakes2.add_snake()

                    if (snake != snakes2.head and snakes2.head.rect.colliderect(snake))\
                    or pygame.sprite.spritecollideany(snake, walls)\
                    or snakes.head.rect.colliderect(snake):
                        expl = Explosion(snakes2.head.rect.copy())
                        all_sprites.add(expl)
                        sd2 = True
                        break
            if sd2:
                for snake in snakes2.group:
                    snake.kill()
                opt2, sd2 = False, False

            for fw in all_sprites:
                self.screen.blit(fw.surf, fw.rect)

            pygame.display.flip()
            self.clock.tick(GAME_SPEED)

if __name__ == '__main__':
    t = Game()
