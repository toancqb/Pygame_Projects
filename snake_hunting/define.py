import os.path
import pygame.image
import pygame.transform

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_0,
    K_w,
    K_s,
    K_a,
    K_d,
    K_l,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
)

SQ_SIZE = 17
NX = 40 # 25 50
NY = 40
SCREEN_WIDTH = SQ_SIZE * NX
SCREEN_HEIGHT = SQ_SIZE * NY
GAME_SPEED = 10
BULLET_SPEED = 25
SP_BULLET = 20

Head_Right = pygame.image.load(os.path.join("srcs", "snake_right.png"))
Head_Right = pygame.transform.scale(Head_Right, (SQ_SIZE, SQ_SIZE))
Head_Up = pygame.image.load(os.path.join("srcs", "snake_up.png"))
Head_Up = pygame.transform.scale(Head_Up, (SQ_SIZE, SQ_SIZE))
Head_Down = pygame.image.load(os.path.join("srcs", "snake_down.png"))
Head_Down = pygame.transform.scale(Head_Down, (SQ_SIZE, SQ_SIZE))
Head_Left = pygame.image.load(os.path.join("srcs", "snake_left.png"))
Head_Left = pygame.transform.scale(Head_Left, (SQ_SIZE, SQ_SIZE))

Head_Right_1 = pygame.image.load(os.path.join("srcs", "snake_right_1.png"))
Head_Right_1 = pygame.transform.scale(Head_Right_1, (SQ_SIZE, SQ_SIZE))
Head_Up_1 = pygame.image.load(os.path.join("srcs", "snake_up_1.png"))
Head_Up_1 = pygame.transform.scale(Head_Up_1, (SQ_SIZE, SQ_SIZE))
Head_Down_1 = pygame.image.load(os.path.join("srcs", "snake_down_1.png"))
Head_Down_1 = pygame.transform.scale(Head_Down_1, (SQ_SIZE, SQ_SIZE))
Head_Left_1 = pygame.image.load(os.path.join("srcs", "snake_left_1.png"))
Head_Left_1 = pygame.transform.scale(Head_Left_1, (SQ_SIZE, SQ_SIZE))

Body = pygame.image.load(os.path.join("srcs", "body.png"))
Body = pygame.transform.scale(Body, (SQ_SIZE, SQ_SIZE))

BLACK = (0, 0, 0)
ORANGE = (181, 101, 29)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (135, 206, 250)
RED = (255, 0, 0)
RED_B = (255, 102, 102)
RED_P = (255, 51, 51)
GRIS_BRIGHT = (192, 192, 192)
GRIS = (128, 128, 128)
BLUE_D = (0, 76, 153)
