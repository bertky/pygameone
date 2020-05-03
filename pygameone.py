import pygame

import pygame.locals as pg

import random

######################################################################
#
#  Expirementing with pygame for a simmple tile based game
#  
#  Tiles have methods for accessing selves and neighbors
#  Maps contains tiles and may be iterated over
#  Maps can play a game of life to generate caverns and assign tiles
#  Tilesets are based on a binary system to set walls from 16 options 
#
######################################################################


TILE_SIZE  = 24
MAP_WIDTH  = 60
MAP_HEIGHT = 40

######################################################################
#
#  The Tile class used to have methods for neighbor access whic have
#  have been moved into the map class itself
#
#  Tiles have tuple for coordinates, a set for flags, and a dict
#
#######################################################################

class Tile:
	def __init__(self,_map,x=0,y=0):
		self.parent = _map
		self.x      = x
		self.y      = y
		self.dict   = {}
	def __repr__(self):
		return "tile:"+str(self.x)+","+str(self.y)+":"+str(self.dict)
	def has_attribute(self,attr):
		return attr in self.dict.keys()
	def get_attribute(self,attr):
		if self.has_attribute(attr):
			return self.dict[attr]
	def set_attribute(self, attr, value):
		self.dict.update({attr:value})
	def chance_set_attribute(self, attr, v1=True, v2=False,p=0.5):
		v = random.random() < p and v1 or v2
		self.set_attribute(attr, v)
	def get_neighbor(self,dx,dy):
		nx, ny = self.x + dx, self.y + dy
		return self.parent(nx,ny)
	def get_neighbors(self, ortho=True, diag=True):
		neighbors = []
		neighbors += ortho and [self.get_neighbor(0,-1),
			self.get_neighbor(1,0),
			self.get_neighbor(0,1),
			self.get_neighbor(-1,0)] or []
		neighbors += diag  and [self.get_neighbor(-1,-1),
			self.get_neighbor(1,-1),
			self.get_neighbor(-1,1),
			self.get_neighbor(1,1,)] or []
		neighbors = set(neighbors)
		neighbors.discard(None)
		return neighbors
	def get_neighbor_with(self,attr,dx,dy):
		neighbor = self.get_neighbor(dx,dy)
		if neighbor:
			return neighbor.get_attribute(attr)
	def get_neighbors_with(self,attr,ortho=True,diag=True):
		neighbors 	= self.get_neighbors(ortho,diag)
		neighbors_r = [x for x in neighbors if x.get_attribute(attr)]
		return neighbors_r
	def get_neighbors_without(self,attr,ortho=True,diag=True):
		neighbors 	= self.get_neighbors(ortho,diag)
		neighbors_r = [x for x in neighbors if not x.get_attribute(attr)]
		return neighbors_r
	def count_neighbors(self,ortho=True,diag=True):
		return len(self.get_neighbors(ortho,diag))
	def count_neighbors_with(self,attr,ortho=True,diag=True):
		return len(self.get_neighbors_with(attr,ortho,diag))
	def count_neighbors_without(self,attr,ortho=True,diag=True):
		return len(self.get_neighbors_without(attr,ortho,diag))
	def is_edge_of(self,attr,ortho=True,diag=True):
		return self.count_neighbors_with(attr,ortho,diag) != self.count_neighbors()
	def is_surrounded_by(self,attr,ortho=True,diag=True):
		return self.count_neighbors_with(attr,ortho,diag) == self.count_neighbors()

########################################################################
# The Map 
# contains all the tiles and can generate caves
# has methods for gathering groups of tiles and filtering them
# includes a cellular automata process to generate caves
# contains a dictionary of tilesets
# should eventually comply in some way with TileD
########################################################################

class Map:
	def __init__(self, width = 10, height = 10):
		self.width 		= width
		self.height 	= height
		self.tilesets 	= {}
		self.floor 		= pygame.surface.Surface(self.get_dimensions())
		self.walls 		= pygame.surface.Surface(self.get_dimensions())
		self.walls.set_colorkey((0,0,0))
		self.objects 	= []
		self.arrays 	= []
		for y in range(0,height):
			self.arrays.append([])
			for x in range(0,width):
				self.arrays[y].append(Tile(self,x,y))
	def __iter__(self):
		for y in self.arrays:
			for t in y:
				yield t
	def __repr__(self):
		rtrn = ''
		for y in self.arrays:	
			for t in y:
				rtrn+=t.get_attribute('wall') and '%' or t.get_attribute('floor') and '.' or ' '
			rtrn+='\n'
		return rtrn
	def __call__(self,x,y):
		exists = 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1
		if exists:
			return self.arrays[y][x]

		#return exists and self.arrays[y][x] or None
	def add_tileset(self,tileset):
		self.tilesets.update({tileset.name:tileset})
	def get_tileset(self,tileset_name):										
		self.tilesets.get(tileset_name)
	def add_object(self,object,x=0,y=0):
		dst = self(x,y)
		while dst.get_attribute('block'):
			dst = self(random.randrange(0,self.width),random.randrange(0,self.height))
		object.parent 	= self
		object.x 		= dst.x
		object.y 		= dst.y
		self.objects.append(object)

	def get_dimensions(self):
		return (self.width * TILE_SIZE, self.height * TILE_SIZE)
	def randomize_attribute(self, attr, p=0.5):
		for tile in self:
			tile.chance_set_attribute(attr)
	def get_border_tiles(self):
		border_coordinates = ()
		horizontal = (((0,y),(self.width-1,y))  for y in range(self.height))
		vertical   = (((x,0),(x,self.height-1)) for x in range(self.width))
		for pair in horizontal:
			border_coordinates += pair
		for pair in vertical:
			border_coordinates += pair
		border_tiles = []
		for x,y in border_coordinates:
			border_tiles.append(self(x,y))
		return border_tiles
	def set_border_tiles_attribute(self,attr,value):
		for tile in self.get_border_tiles():
			tile.set_attribute(attr,value)
	def life_cycle(self, life_minimum=4, death_maximum=4, force_border=True):
		for tile in self:
			tile.set_attribute('alive_neighbor_count',tile.count_neighbors_with('alive'))
		for tile in self:
			alive_neighbor_count = tile.get_attribute('alive_neighbor_count')
			if alive_neighbor_count > life_minimum:
				tile.set_attribute('alive',True)
			if alive_neighbor_count < death_maximum:
				tile.set_attribute('alive',False)
		if force_border:
			self.set_border_tiles_attribute('alive',True)
	def life_to_layout(self):
		for tile in self:
			if tile.get_attribute('alive'):
				if tile.is_surrounded_by('alive'):
					tile.set_attribute('wall',False)
					tile.set_attribute('block',True)
				else:
					tile.set_attribute('wall',True)
					tile.set_attribute('block',True)
			else:
				tile.set_attribute('floor',True)
				tile.set_attribute('block',False)
	def decorate_layout(self,tileset,flavor=0):
		for tile in self:
			x = tile.x
			y = tile.y
			if tile.get_attribute('wall'):
				wall_tile  			= 0
				floor_tile 			= False
				wall_tile  			+= tile.get_neighbor_with('wall',0,-1) 	and 1 or 0
				wall_tile  			+= tile.get_neighbor_with('wall',1,0) 	and 2 or 0
				wall_tile  			+= tile.get_neighbor_with('wall',0,1) 	and 4 or 0
				wall_tile  			+= tile.get_neighbor_with('wall',-1,0) 	and 8 or 0
				floor_tile 			=  tile.get_neighbor_with('floor',0,-1) and -1 or floor_tile
				floor_tile 			=  tile.get_neighbor_with('floor',1,0) 	and -2 or floor_tile
				floor_tile 			=  tile.get_neighbor_with('floor',0,1) 	and -3 or floor_tile
				floor_tile 			=  tile.get_neighbor_with('floor',-1,0) and -4 or floor_tile
				floor_tile 			=  tile.count_neighbors_with('floor',diag=False)>1 and -5 or floor_tile
				tile.set_attribute('wall_tile',tileset(wall_tile,flavor))
				if floor_tile:
					tile.set_attribute('floor_tile',tileset(floor_tile,flavor))
			elif tile.get_attribute('floor'):
				floor_tile = 20 - random.randrange(1,4)
				tile.set_attribute('floor_tile',tileset(floor_tile,flavor))
	def render(self):
		print(self)
		for tile in self:
			floor_tile = tile.get_attribute('floor_tile')
			wall_tile  = tile.get_attribute('wall_tile')
			if floor_tile:
				self.floor.blit(floor_tile,(tile.x*TILE_SIZE, tile.y*TILE_SIZE))
			if wall_tile:
				self.walls.blit(wall_tile,(tile.x*TILE_SIZE, tile.y*TILE_SIZE))
		pygame.display.flip()

#####################################################################
# Tilesets create subsurfaces from an image to use as tiles
# if 'cave' flag is set then they create 4 partial tiles
# these are used for walls which leave floor partially exposed
#

class Tileset:
	def __init__(self,name,cave=False):
		self.name 	= name
		self.image 	= pygame.image.load(name+'.png').convert()
		self.tiles  = []
		self.objects= []
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
	def __call__(self,x=0,y=0):
		tile = self.tiles[y][x]
		return tile

####################
# Objects contain their own rendering surface
# objects can render themselvse
# they are contained in the map object

class Object:
	def __init__(self,name,tile):
		self.name   = name
		self.parent = False
		self.tile   = tile
		self.image  = pygame.surface.Surface((TILE_SIZE,TILE_SIZE))
		self.image.set_colorkey((0,0,0))
		self.x 		= False
		self.y 		= False
		self.attr   = {}
		self.render()
	def __repr__(self):
		print(self.name,'@(',self.x,',',self.y,')')
	def render(self):
		self.image.blit(self.tile,(0,0))
		pygame.display.flip()

class Chest(Object):

	def __init__(self,name):

		self.closed = objects(4,0)
		self.opened = objects(5,0)
		Object.__init__(self,name,objects(4,0))
		self.open = False

	def toggle(self):
		self.open = not self.open
		self.tile = self.open and objects(5,0) or objects(4,0)
		self.render()


pygame.init()
pygame.display.set_mode((TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT))
mars 	= Tileset('mars',cave=True)
objects = Tileset('objects')
actors 	= Tileset('starguys')
level 	= Map(MAP_WIDTH,MAP_HEIGHT)
level.add_tileset(mars)
level.randomize_attribute('alive')
level.life_cycle()
level.life_cycle()
level.life_cycle()
level.life_to_layout()
level.decorate_layout(mars)
level.render()
crates=(Object('crate',objects(0,0)),
	Object('crate',objects(0,0)),
	Object('crate',objects(0,0)),
	Object('crate',objects(0,0)),
	Object('crate',objects(0,0)),
	Object('crate',objects(0,0)),
	Object('crate',objects(0,0)))
crystals=(Object('crystal',objects(1,0)),
	Object('crystal',objects(1,0)),
	Object('crystal',objects(1,0)),
	Object('crystal',objects(1,0)),
	Object('crystal',objects(1,0)),
	Object('crystal',objects(1,0)),
	Object('crystal',objects(1,0)))
chest = Chest('ammo crate')

for obstacle in crates:
	level.add_object(obstacle)
for obstacle in crystals:
	level.add_object(obstacle)
level.add_object(chest)

if __name__ == "__main__":
	clock = pygame.time.Clock()
	running = True
	screen = pygame.display.get_surface()
	while running:
		screen.blit(level.floor,(0,0))
		screen.blit(level.walls,(0,0))
		screen.blit(crystals[1].image,(0,0))
		for object in level.objects:
			screen.blit(object.image,(object.x * TILE_SIZE, object.y * TILE_SIZE))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pg.QUIT:
				running = False
		clock.tick(20)