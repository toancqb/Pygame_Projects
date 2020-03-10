
import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
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
SCORE = 0
GREEN = (0, 128, 0)
BLUE = (135, 206, 250)
RED = (255, 0, 0)


class Player(pygame.sprite.Sprite):
    move_up_sound = None
    move_down_sound = None
    def __init__(self, move_up_sound, move_down_sound, ):
        super(Player, self).__init__()
        self.move_up_sound = move_up_sound
        self.move_down_sound = move_down_sound
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -PLAYER_SPEED)
            self.move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, PLAYER_SPEED)
            self.move_down_sound.play()
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
        self.surf = pygame.image.load("missile.png").convert()
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

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.surf = pygame.image.load("boss.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH/2, SCREEN_WIDTH),
                0,
            )
        )
        self.speed = random.randint(ENEMY_SPEED_MAX/2, ENEMY_SPEED_MAX)

    def update(self):
        global SCORE
        self.rect.move_ip(-self.speed, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE = SCORE + 10
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
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

class Game():

    def __init__(self):

        # Load and play background music
        # Sound source: http://ccmixter.org/files/Apoxode/59262
        # License: https://creativecommons.org/licenses/by/3.0/
        pygame.mixer.init()
        pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
        pygame.mixer.music.play(loops=-1)
        # Load all sound files
        # Sound sources: Jon Fincher
        move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
        move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
        collision_sound = pygame.mixer.Sound("Collision.ogg")

        pygame.init()
        font = pygame.font.SysFont("comicsansms", 40)

        self.clock = pygame.time.Clock()


        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

        ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(ADDENEMY, 250)

        ADDBOSS = pygame.USEREVENT + 2
        pygame.time.set_timer(ADDBOSS, 5000)

        self.ADDCLOUD = pygame.USEREVENT + 3
        pygame.time.set_timer(self.ADDCLOUD, 2000)

        self.menu()

        player = Player(move_up_sound, move_down_sound)
        # Create groups to hold enemy sprites, cloud sprites, and all sprites
        # - enemies is used for collision detection and position updates
        # - clouds is used for position updates
        # - all_sprites is used for rendering
        enemies = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
                elif event.type == ADDENEMY:
                    new_enemy = Enemy()
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
                elif event.type == ADDBOSS:
                    new_boss = Boss()
                    enemies.add(new_boss)
                    all_sprites.add(new_boss)
                elif event.type == self.ADDCLOUD:
                    new_cloud = Cloud()
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

            pressed_keys = pygame.key.get_pressed()

            player.update(pressed_keys)
            enemies.update()
            clouds.update()

            self.screen.fill(BLUE)

            #screen.blit(player.surf, player.rect)
            for entity in all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            if pygame.sprite.spritecollideany(player, enemies):
                move_up_sound.stop()
                move_down_sound.stop()
                collision_sound.play()
                player.kill()
                running = False

            txt = font.render("SCORE "+str(SCORE), True, GREEN)
            self.screen.blit(txt, (5, 5))
            pygame.display.flip()
            self.clock.tick(30)


        self.game_over()

        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()

    def menu(self):
        font2 = pygame.font.SysFont("comicsansms", 72)
        font3 = pygame.font.SysFont("comicsansms", 40)
        self.screen.fill(BLUE)

        txt = font2.render("-=Airplane Missile Game=-", True, RED)
        txt_center = (
            SCREEN_WIDTH/2 - txt.get_width() // 2,
            SCREEN_HEIGHT/2 - txt.get_height() // 2
        )

        txt2 = font3.render("Press <Space> to Play", True, GREEN)
        txt2_center = (
            SCREEN_WIDTH/2 - txt2.get_width() // 2,
            SCREEN_HEIGHT/2 + 30
        )

        clouds_decor = pygame.sprite.Group()
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


    def game_over(self):
        font2 = pygame.font.SysFont("comicsansms", 72)
        self.screen.fill(BLUE)
        txt = font2.render("GAME OVER! "+str(SCORE)+" SCORES!", True, RED)
        txt_center = (
            SCREEN_WIDTH/2 - txt.get_width() // 2,
            SCREEN_HEIGHT/2 - txt.get_height() // 2
        )
        clouds_decor = pygame.sprite.Group()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
                elif event.type == self.ADDCLOUD:
                    new_cloud = Cloud()
                    clouds_decor.add(new_cloud)

            clouds_decor.update()
            self.screen.fill(BLUE)

            self.screen.blit(txt, txt_center)

            for entity in clouds_decor:
                self.screen.blit(entity.surf, entity.rect)

            pygame.display.flip()
            self.clock.tick(30)


if __name__ == '__main__':
    t = Game()