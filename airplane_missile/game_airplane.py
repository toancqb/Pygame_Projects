
import pygame
import random
import os.path
import time
from class_objects import *
from define import *
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards

## define.py

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_SPEED_MIN = 5
ENEMY_SPEED_MAX = 20
CLOUD_SPEED = 4
BULLET_SPEED = 10
#SCORE = 0
GREEN = (0, 128, 0)
BLUE = (135, 206, 250)
RED = (255, 0, 0)

##

## class_objects.py

# import pygame
# import random
# import os.path
# import time
# from define import *
#
# SCORE = 0

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
            SCORE = SCORE + 1
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
            SCORE = SCORE + 10
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

    def process(self):
        if self.timer < 0:
            self.kill()

    def update_timer(self):
        self.timer = self.timer - 1

    def update(self):
        self.rect.move_ip(BULLET_SPEED)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load(os.path.join("srcs", "bullet.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = rect
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

##

class Game():

    def __init__(self):

        # Load and play background music
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("srcs", "spacetheme.mp3"))
        pygame.mixer.music.play(loops=-1)
        # Load all sound files
        # Sound sources: Jon Fincher
        self.move_up_sound = pygame.mixer.Sound(os.path.join("srcs","Rising_putter.ogg"))
        self.move_down_sound = pygame.mixer.Sound(os.path.join("srcs","Falling_putter.ogg"))
        self.collision_sound = pygame.mixer.Sound(os.path.join("srcs","explosion.wav"))
        self.gold_sound = pygame.mixer.Sound(os.path.join("srcs","dropmetalthing.ogg"))

        pygame.init()
        self.font = pygame.font.SysFont("comicsansms", 35)
        self.font2 = pygame.font.SysFont("comicsansms", 72)

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        self.ADDBOSS = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ADDBOSS, 5000)

        self.ADDCLOUD = pygame.USEREVENT + 3
        pygame.time.set_timer(self.ADDCLOUD, 2000)

        self.ADDGOLD = pygame.USEREVENT + 4
        pygame.time.set_timer(self.ADDGOLD, 5000)

        self.highest_score = self.get_highest_score()
        global SCORE
        while True:
            self.replay = False
            SCORE = 0
            self.menu()
            self.game_play()
            self.ck_sv_highest_score()
            self.game_over()
            if self.replay == False:
                break

        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()

    def menu(self):
        self.screen.fill(BLUE)

        txt = self.font2.render("-=Airplane Missile Game=-", True, RED)
        txt_center = (
            SCREEN_WIDTH/2 - txt.get_width() // 2,
            SCREEN_HEIGHT/2 - txt.get_height() // 2
        )

        txt2 = self.font.render("Press <Space> to Play", True, GREEN)
        txt2_center = (
            SCREEN_WIDTH/2 - txt2.get_width() // 2,
            SCREEN_HEIGHT/2 + 30
        )

        clouds_decor = pygame.sprite.Group()
        clouds_decor.add(Cloud())
        clouds_decor.add(Cloud())
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        running = False
                elif event.type == QUIT:
                    running = False
                elif event.type == self.ADDCLOUD:
                    new_cloud = Cloud()
                    clouds_decor.add(new_cloud)

            clouds_decor.update()
            self.screen.fill(BLUE)

            self.screen.blit(txt, txt_center)
            self.screen.blit(txt2, txt2_center)

            for entity in clouds_decor:
                self.screen.blit(entity.surf, entity.rect)

            pygame.display.flip()
            self.clock.tick(30)

    def game_play(self):
        global SCORE
        player = Player(self.move_up_sound, self.move_down_sound)
        # Create groups to hold enemy sprites, cloud sprites, and all sprites
        # - enemies is used for collision detection and position updates
        # - clouds is used for position updates
        # - all_sprites is used for rendering
        enemies = pygame.sprite.Group()
        golds = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        new_bullet = Bullet(player.rect.copy())
                        bullets.add(new_bullet)
                        all_sprites.add(new_bullet)
                elif event.type == QUIT:
                    running = False
                elif event.type == self.ADDENEMY:
                    new_enemy = Enemy()
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
                elif event.type == self.ADDBOSS:
                    new_boss = Boss()
                    enemies.add(new_boss)
                    all_sprites.add(new_boss)
                elif event.type == self.ADDCLOUD:
                    new_cloud = Cloud()
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)
                elif event.type == self.ADDGOLD:
                    new_gold = Gold()
                    golds.add(new_gold)
                    all_sprites.add(new_gold)

            pressed_keys = pygame.key.get_pressed()

            player.update(pressed_keys)
            enemies.update()
            bullets.update()
            golds.update()
            clouds.update()
            for e in explosions:
                e.update_timer()
                e.process()

            self.screen.fill(BLUE)

            for entity in all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            for g in golds:
                if pygame.sprite.collide_rect(player, g):
                    self.gold_sound.play()
                    g.kill()
                    SCORE += 50

            if pygame.sprite.spritecollideany(player, enemies):
                self.move_up_sound.stop()
                self.move_down_sound.stop()
                self.collision_sound.play()
                expl = Explosion(player.rect.copy())
                self.screen.blit(expl.surf, expl.rect)
                player.kill()
                pygame.display.flip()
                time.sleep(2)

                running = False

            for bullet in pygame.sprite.groupcollide(bullets, enemies, True, True):
                self.collision_sound.play()
                expl = Explosion(bullet.rect.copy())
                explosions.add(expl)
                all_sprites.add(expl)

            tmp_txt = "SCORE: ["+str(SCORE)+"]              HIGHEST SCORE: -=["+str(self.highest_score)+"]=-"
            txt = self.font.render(tmp_txt, True, GREEN)
            self.screen.blit(txt, (5, 5))
            pygame.display.flip()
            self.clock.tick(30)

    def game_over(self):
        global SCORE
        self.screen.fill(BLUE)
        txt = self.font2.render("GAME OVER! ["+str(SCORE)+"] SCORES!", True, RED)
        txt_center = (
            SCREEN_WIDTH/2 - txt.get_width() // 2,
            SCREEN_HEIGHT/2 - txt.get_height() // 2
        )

        txt2 = self.font.render("Press <Space> to Replay", True, GREEN)
        txt2_center = (
            SCREEN_WIDTH/2 - txt2.get_width() // 2,
            SCREEN_HEIGHT/2 + 30
        )

        clouds_decor = pygame.sprite.Group()
        clouds_decor.add(Cloud())
        clouds_decor.add(Cloud())
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_SPACE:
                        self.replay = True
                        running = False
                elif event.type == QUIT:
                    running = False
                elif event.type == self.ADDCLOUD:
                    new_cloud = Cloud()
                    clouds_decor.add(new_cloud)

            clouds_decor.update()
            self.screen.fill(BLUE)

            self.screen.blit(txt, txt_center)
            self.screen.blit(txt2, txt2_center)
            for entity in clouds_decor:
                self.screen.blit(entity.surf, entity.rect)

            pygame.display.flip()
            self.clock.tick(30)

    def ck_sv_highest_score(self):
        global SCORE
        if SCORE > self.highest_score:
            self.highest_score = SCORE
            database = open(os.path.join("srcs",".database.txt"), 'w+')
            database.write(str(SCORE))
            database.close()

    def get_highest_score(self):
        try:
            database = open(os.path.join("srcs",".database.txt"), 'r')
        except (OSError, IOError) as e:
            database = open(os.path.join("srcs",".database.txt"), 'w+')
            database.write('0')

        try:
            highest_score = int(database.readline())
        except ValueError:
            highest_score = 0
        database.close()
        return highest_score


if __name__ == '__main__':
    t = Game()
