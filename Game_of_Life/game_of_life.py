###############################
## Author: TRAN Quang Toan   ##
## Project Game of Life      ##
## Version 1                 ##
## 13 Apr 2020               ##
###############################

import pygame
from define import *
from ft_lib import *

class Board():
	def __init__(self, screen):
		self.screen = screen
		self.init_arena()

	def draw(self):
		for i in range(PX):
			if i % 9 == 0:
				color = GRIS
			else:
				color = GRIS_B
			pygame.draw.line(self.screen, color, (i*CELL, 0), (i*CELL, SCREEN_HEIGHT))
		for i in range(PY):
			if i % 9 == 0:
				color = GRIS
			else:
				color = GRIS_B
			pygame.draw.line(self.screen, color, (0, i*CELL), (SCREEN_WIDTH, i*CELL))

		for y in range(PY):
			for x in range(PX):
				if self.ar[x][y] == 1:
					pygame.draw.rect(self.screen, ORANGE, (x*CELL,y*CELL, CELL, CELL))
					pygame.draw.rect(self.screen, BLACK, (x*CELL+1,y*CELL+1, CELL-2, CELL-2))

	def init_arena(self):
		self.ar = [[ 0 for i in range(PY)] for i in range(PX)]
		self.ar[2][2] = 1
		self.ar[3][2] = 1
		self.ar[4][2] = 1
		self.ar[4][1] = 1
		self.ar[3][0] = 1


	def process(self):
		new_ar = [[ 0 for i in range(PY)] for i in range(PX)]
		for y in range(PY):
			for x in range(PX):
				if self.ar[x][y] == 1:
					nb = get_neighbour(self.ar, x, y, 1)
					if nb == 2 or nb == 3:
						new_ar[x][y] = 1
					else:
						new_ar[x][y] = 0
				else:
					if get_neighbour(self.ar, x, y, 1) == 3:
						new_ar[x][y] = 1
		self.ar = new_ar



class Game():
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.screen.fill(WHITE)
		self.clock = pygame.time.Clock()
		board = Board(self.screen)
		opt = False
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
					if event.key == pygame.K_SPACE:
						opt = True
				if event.type == pygame.MOUSEBUTTONDOWN:
					if pygame.mouse.get_pressed()[0]:
						p = rev_rect(pygame.mouse.get_pos())
						board.ar[p[0]][p[1]] = 1 - board.ar[p[0]][p[1]]
			self.screen.fill(WHITE)
			board.draw()
			if opt:
				board.process()
				pygame.time.delay(200)

			pygame.display.flip()
			self.clock.tick(20)

		pygame.quit()


if __name__ == '__main__':
	Game()

