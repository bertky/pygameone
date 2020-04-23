import pygame

import pygame.locals as pg

import random

## hello world

TILE_SIZE  = 24
MAP_WIDTH  = 60
MAP_HEIGHT = 40

class Tile:

	def __init__(self,g,x,y,attr={}):

		self.g    = g
		self.x    = x
		self.y    = y
		self.attr = attr

	def __repr__(self):

		return "tile:"+str(self.x)+","+str(self.y)+":"+str(self.attr)

	def get_attr(self, attr='nil'):

		value = None

		try:

			value = self.attr[attr]

		except KeyError:

			value = None

		return value

	def set_attr(self, attr='nil', value=False):

		self.attr.update({attr:value})

	def set_attr_rand(self, attr='nil', probability=0.5):

		value = random.random() < probability and True or False

		self.set_attr(attr, value)

		return value

	def neighbor(self,dx=0,dy=0):

		nx, ny = self.x + dx, self.y + dy

		neighbor = self.g(nx,ny)
		
		return neighbor

	def get_neighbors(self, ortho=True, diag=True):

		neighbors = []

		if ortho:

			neighbors += self.get_ortho_neighbors()

		if diag:

			neighbors += self.get_diag_neighbors()

		return neighbors

	def get_ortho_neighbors(self):

		neighbors = []

		for dx in range(-1,2,2):

			for dy in range(-1,2,2):

				neighbors.append(self.neighbor(dx,dy))

		neighbors = [i for i in set(neighbors) if i]

		return neighbors

	def get_diag_neighbors(self):

		neighbors = []

		for dx in range(-1,2,2):

			neighbors.append(self.neighbor(dx,0))

		for dy in range(-1,2,2):

			neighbors.append(self.neighbor(0,dy))

		neighbors = [i for i in set(neighbors) if i]

		return neighbors

	def get_neighbor_attr(self,dx=0,dy=0,attr='nil'):

		neighbor = self.neighbor(dx,dy)
		
		if neighbor:

			neighbor = neighbor.get_attr(attr) and neighbor or False
		
		return neighbor

	def get_neighbors_attr(self,attr='nil',ortho=True,diag=True):

		neighbors_attr = []

		if ortho:

			neighbors_attr += self.get_ortho_neighbors_attr(attr)

		if diag:

			neighbors_attr += self.get_diag_neighbors_attr(attr)

		return neighbors_attr
	
	def get_ortho_neighbors_attr(self,attr='nil'):

		ortho_neighbors = self.get_ortho_neighbors()

		neighbors_attr = [i for i in set(ortho_neighbors) if i.attr[attr]]

		return neighbors_attr
	
	def get_diag_neighbors_attr(self,attr='nil'):

		diag_neighbors = self.get_diag_neighbors()

		neighbors_attr = [i for i in set(diag_neighbors) if i.attr[attr]]

		return neighbors_attr

	def is_all_neighbors_attr(self,attr='nil',ortho=True,diag=True):

		total_neighbors_attr = self.get_neighbors_attr(attr, ortho, diag)

		total_neighbors = self.get_neighbors(ortho, diag)

		all_neighbors_attr = len(total_neighbors) == len(total_neighbors_attr)

		return all_neighbors_attr

	def is_any_neighbor_all_neighbors_attr(self,attr='nil',ortho=True,diag=True):

		neighbors = self.get_neighbors(ortho, diag)

		neighbors_all_neighbors_attr = [tile for tile in set(neighbors) if tile.is_all_neighbors_attr(attr,ortho,diag)]

		return len(neighbors_all_neighbors_attr) > 0

	def is_neighbor_attr_edge(self,dx=0,dy=0,attr='nil',ortho=True,diag=True):

		neighbor = self.neighbor(dx,dy)

		if neighbor:

			neighbor_neighbors = len([i for i in neighbor.get_neighbors(ortho,diag) if i])	

			neighbor_neighbors_attr = len([i for i in neighbor.get_neighbors_attr(attr,ortho,diag) if i])

			edge_neighbors_attr = neighbor_neighbors > neighbor_neighbors_attr

			print(self,dx,dy,neighbor_neighbors,neighbor_neighbors_attr)

		else:

			edge_neighbors_attr = False

		return edge_neighbors_attr

	def set_neighbor_attr_count(self, attr='nil', ortho=True, diag=True):

		attr_name = attr + '_neighbor_count'

		attr_count = len(self.get_neighbors_attr(attr, ortho, diag))

		self.set_attr(attr_name, attr_count)

class Map:

	def __init__(self, width = 10, height = 10):

		self.width 		= width
		self.height 	= height
		self.tilesets 	= {}
		self.floor 		= pygame.surface.Surface(self.get_dimensions())
		self.walls 		= pygame.surface.Surface(self.get_dimensions())
		self.walls.set_colorkey((0,0,0))
		self.objects 	= []
		self.g     		= []
		for y in range(0,height):
			self.g.append([])
			for x in range(0,width):
				self.g[y].append([Tile(self,x,y,{})])

	def __iter__(self):

		for y in self.g:
			for x in y:
				yield x[0]

	def __repr__(self):

		rtrn = ''
		for y in self.g:
			for x in y:
				rtrn+=x[0].attr['wall'] and '%' or x[0].attr['floor'] and '.' or' '
			rtrn+='\n'
		return rtrn

	def __call__(self,x,y):
		exists = 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1
		return exists and self.g[y][x][0] or False

	def add_tileset(self,tileset):

		self.tilesets.update({tileset.name:tileset})

	def get_tileset(self,tileset_name):

		self.tilesets.get(tileset_name)

	def get_dimensions(self):

		return (self.width * TILE_SIZE, self.height * TILE_SIZE)

	def get_tile(self, tile_set, x, y):

		tile = set.tilesets[tile_set].get_tile(x, y)

		return tile

	def rand_attr(self, attr, rand):

		for tile in self:

			tile.set_attr_rand(attr,rand) and 1 or 0

	def get_border_tiles(self):

		border_tiles = []

		print('height,range',range(self.height))

		for y in range(0,self.height):
			
			border_tiles.append(self(0,y))
			border_tiles.append(self(self.width-1,y))

		print('width,range',range(0,self.width))
		
		for x in range(0,self.width): 
			
			border_tiles.append(self(x,0))
			border_tiles.append(self(x,self.height-1))

		return border_tiles

	def set_border_tiles_attr(self,attr,value):

		for tile in [i for i in set(self.get_border_tiles()) if i]:

			tile.set_attr(attr,value)
			print(tile)

	def spawn_life(self, rand=0.5):

		self.rand_attr('alive', rand)

	def life_cycle(self, life_minimum=4, death_maximum=4, force_border=True):

		for tile in self:

			tile.set_neighbor_attr_count('alive')

		for tile in self:

			alive_neighbor_count = tile.get_attr('alive_neighbor_count')

			if alive_neighbor_count > life_minimum:

				tile.set_attr('alive',True)

			if alive_neighbor_count < death_maximum:

				tile.set_attr('alive',False)

		if force_border:

			self.set_border_tiles_attr('alive',True)


	def life_to_tile(self, tileset_name, flavor = 0, cave=False):

		##temporary static tileset

		tileset = self.tilesets['mars']

		for tile in self:

			if tile.get_attr('alive'):

				if tile.is_all_neighbors_attr('alive'):

					tile.set_attr('wall',False)
					tile.set_attr('floor',False)
					tile.set_attr('void',True)
					tile.set_attr('block',True)

				else:

					tile.set_attr('wall',True)
					tile.set_attr('block',True)
					
					##Leave floors under wallls off for now

					#floor = not tile.is_any_neighbor_all_neighbors_attr('alive')
					#if floor:
					#	floor_tile = 17 + random.randrange(0,4)
					#	tile.set_attr('floor',True)
					#	tile.set_attr('floor_tile',tileset(floor_tile,flavor))
			else:
				tile.set_attr('floor',True)
				tile.set_attr('wall',False)
				tile.set_attr('block',False)
				
		for tile in self:

			if tile.get_attr('wall'):
				wall_tile  = 0
				floor_tile = False
				wall_tile  += tile.get_neighbor_attr(0,-1,'wall')    and 1 or 0
				wall_tile  += tile.get_neighbor_attr(1,0,'wall')     and 2 or 0
				wall_tile  += tile.get_neighbor_attr(0,1,'wall')     and 4 or 0
				wall_tile  += tile.get_neighbor_attr(-1,0,'wall')    and 8 or 0
				floor_tile_north 	=  tile.get_neighbor_attr(0,-1,'floor')
				floor_tile_east 	=  tile.get_neighbor_attr(1,0,'floor')
				floor_tile_south 	=  tile.get_neighbor_attr(0,1,'floor')
				floor_tile_west 	=  tile.get_neighbor_attr(-1,0,'floor') 
				floor_tile =  floor_tile_north   and -1 or floor_tile
				floor_tile =  floor_tile_east and -2 or floor_tile
				floor_tile =  floor_tile_south and -3 or floor_tile
				floor_tile =  floor_tile_west  and -4 or floor_tile
				floor_tile =  (floor_tile_north or floor_tile_south) and (floor_tile_west or floor_tile_east) and -5 or floor_tile
				tile.set_attr('wall_tile',tileset(wall_tile,flavor))
				if floor_tile:
					tile.set_attr('floor',True)
					tile.set_attr('floor_tile',tileset(floor_tile,flavor))

			if tile.get_attr('floor'):
				floor_tile = 17 + random.randrange(0,3)
				tile.set_attr('floor_tile',tileset(floor_tile,flavor))

	def render(self):

		for tile in self:
			floor_tile = tile.get_attr('floor_tile')
			wall_tile  = tile.get_attr('wall_tile')
			if floor_tile:
				self.floor.blit(floor_tile,(tile.x*TILE_SIZE, tile.y*TILE_SIZE))
			if wall_tile:
				self.walls.blit(wall_tile,(tile.x*TILE_SIZE, tile.y*TILE_SIZE))

		pygame.display.flip()

class Tileset:

	def __init__(self,name,cave=False):

		self.name 	= name
		
		self.image 	= pygame.image.load(name+'.png').convert()
		
		self.tiles  = []
		
		self.width 	= self.image.get_width()
		
		self.height = self.image.get_height()

		width_range = range(0, int(self.width/TILE_SIZE))
		
		height_range= range(0, int(self.height/TILE_SIZE))
		
		for y in height_range:
		
			self.tiles.append([])
		
			for x in width_range:
		
				self.tiles[y].append([])
		
				rect = (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
		
				self.tiles[y][x] = self.image.subsurface(rect)

		if cave:

			#west,south,east,north
			cave_tiles = [
			self.image.subsurface((self.width - TILE_SIZE, 	0, 				TILE_SIZE/2,	TILE_SIZE)),
			self.image.subsurface((self.width - TILE_SIZE, 	TILE_SIZE/2, 	TILE_SIZE,		TILE_SIZE/2)),
			self.image.subsurface((self.width - TILE_SIZE/2,0, 				TILE_SIZE/2,	TILE_SIZE)),
			self.image.subsurface((self.width - TILE_SIZE,	0,				TILE_SIZE,		TILE_SIZE/2))]
			for tile in cave_tiles:
				self.tiles[0].append(tile)

	def __call__(self,x,y):

		try:
		
			row = self.tiles[y]
		
			try:
		
				tile = self.tiles[y][x]
		
			except IndexError:
		
				tile = self.tiles[0][0]
		
		except IndexError:
		
			tile = self.tiles[0][0]

		return tile

pygame.init()

pygame.display.set_mode((TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT))

mars = Tileset('mars',cave=True)
level = Map(MAP_WIDTH,MAP_HEIGHT)
level.add_tileset(mars)
level.spawn_life(0.45)
print(level(0,0),level(0,0))
level.life_cycle()
print(level(0,0),level(0,0))
level.life_cycle()
level.life_cycle()
level.life_cycle()
level.life_to_tile('mars')
level.render()


if __name__ == "__main__":
	clock = pygame.time.Clock()
	running = True
	screen = pygame.display.get_surface()
	while running:
		screen.blit(level.floor,(0,0))
		screen.blit(level.walls,(0,0))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pg.QUIT:
				running = False
		clock.tick(20)