###############################
## Author: TRAN Quang Toan   ##
## Project Game of Life      ##
## Version 1                 ##
## 13 Apr 2020               ##
###############################

from define import *

def check_valid(nx, ny):
	if nx >= 0 and nx < PX and ny >=0 and ny < PY:
		return True
	return False

def get_neighbour(ar, x, y, n):
	count = 0
	index = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
	for i in index:
		nx, ny = x+i[0], y+i[1]
		if check_valid(nx, ny):
			if ar[nx][ny] == n:
				count += 1
	return count

def rev_rect(p):
	return (p[0] // CELL, p[1] // CELL)
