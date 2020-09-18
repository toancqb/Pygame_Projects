from define import *


def check_position(pos, min1, max1, min2, max2):
    if pos[0] >= min1 and pos[0] <= max1 and pos[1] >= min2 and pos[1] <= max2:
        return True
    return False

def fire_bullet(snakes, rect):
    if snakes.head.goto == (0, -SQ_SIZE):
        dxy = (0, -SP_BULLET)
    elif snakes.head.goto == (0, SQ_SIZE):
        dxy = (0, SP_BULLET)
    elif snakes.head.goto == (-SQ_SIZE, 0):
        dxy = (-SP_BULLET, 0)
    else:
        dxy = (SP_BULLET, 0)
    rect[0] += dxy[0]
    rect[1] += dxy[1]
    return rect
    