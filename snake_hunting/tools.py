###############################
## Author: TRAN Quang Toan   ##
## Project Game Snake        ##
## Version 1                 ##
## 25 Apr 2020               ##
###############################

def check_position(pos, min1, max1, min2, max2):
    if pos[0] >= min1 and pos[0] <= max1 and pos[1] >= min2 and pos[1] <= max2:
        return True
    return False
