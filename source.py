import pygame

import pygame.locals as pg

import random

## hello world

class Tileset:

	def __init__(self):

		image = pygame.image.load('tileset.png').convert()

		tiles = []

		for i in range(0, 19):

			rect = (i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
			tiles.append(image.subsurface(rect))

		self.tiles = tiles

		## to begin, tiles zero for floor and four for wall


class Map:

	def __init__(self, tileset, map_width, map_height):

		self.tileset = tileset

		self.width   = map_width

		self.height  = map_height or map_width

		grid = []

		for x in range(0,map_width):
			
			column = []
			
			grid.append(column)
			
			for y in range(0,map_height):

				## for the first run we will only have walls and not-walls

				tile = random.choice([True,False])

				column.append(tile)

		self.grid = grid

		self.image = pygame.display.get_surface()


		for x, column in enumerate(self.grid):
			for y, p in enumerate(column):
				if self.grid[x][y]:
					self.image.blit(self.tileset.tiles[4],(x*24,y*24))
				else:
					self.image.blit(self.tileset.tiles[0],(x*24,y*24))
		pygame.display.flip()


	#this is done out of order

	def get_dimensions():

		return(self.width * TILE_SIZE, self.height * TILE_SIZE)

TILE_SIZE = 24

pygame.init()
pygame.display.set_mode((960,960))

tileset = Tileset()
level   = Map(tileset,49,40)

debug_string = ''


if __name__ == "__main__":
	clock = pygame.time.Clock()
	running = True
##	for y in range(0,level.height):
##		for x in range(0,level.width):
##			if level.grid[x][y]==True:
##				debug_string = debug_string + 'X'
##			else:
##				debug_string = debug_string + 'O'
##		debug_string = debug_string + '\n'
##	print(debug_string)
	screen = pygame.display.get_surface()
	while running:
		screen.blit(level.image,(0,0))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pg.QUIT:
				running = False
		clock.tick(15)