import pygame

import pygame.locals as pg

import random

## hello world

TILE_SIZE  = 24
MAP_WIDTH  = 60
MAP_HEIGHT = 40

class Tileset:

	def __init__(self):

		image = pygame.image.load('mars.png').convert()

		tiles = []

		for i in range(0, 20):

			rect = (i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
			tiles.append(image.subsurface(rect))

		self.tiles = tiles

class Tile:

	def __init__(self,g,x,y):

		self.g    = g
		self.x    = x
		self.y    = y
		self.attr = {}

	def __repr__(self):

		return "cell:"+str(self.x)+","+str(self.y)+":"+str(self.attr)

	def neighbor(self,dx,dy):

		nx, ny = self.x + dx, self.y + dy
		neighbor = self.g(nx,ny)
		return neighbor

	@property
	def neighbors(self):
		neighbors = self.diag_neighbors + self.ortho_neighbors
		return neighbors

	@property
	def diag_neighbors(self):
		neighbors = []
		for dx in range(-1,2,2):
			neighbors.append(self.neighbor(dx,0))
		for dy in range(-1,2,2):
			neighbors.append(self.neighbor(0,dy))
		neighbors = [i for i in set(neighbors) if i]
		return neighbors

	@property
	def ortho_neighbors(self):
		neighbors = []
		for dx in range(-1,2,2):
			for dy in range(-1,2,2):
				neighbors.append(self.neighbor(dx,dy))
		neighbors = [i for i in set(neighbors) if i]
		return neighbors


class Cell(Tile):

	def __init__(self,g,x,y,a=False):

		Tile.__init__(self,g,x,y)
		self.alive= a
		self.total_living_neighbors = 0

	def __repr__(self):

		return "cell:"+str(self.x)+","+str(self.y)+":"+str(self.alive)

	def assign_total_living_neighbors(self):
		walls = 8 - len(self.neighbors)
		self.total_living_neighbors = len(self.living_neighbors) + walls

	def spawn(self,chance):

		chance = max(0,min(1,chance))
		rnd = random.random()
		if rnd < chance:
			self.alive = True

	def living_neighbor(self,dx,dy):
		living_neighbor = False
		neighbor = self.neighbor(dx,dy)
		if neighbor:
			living_neighbor = neighbor.alive and neighbor or False
		return living_neighbor

	def edge_neighbor(self,dx,dy):
		edge_neighbor = False
		living_neighbor = self.living_neighbor(dx,dy)
		if living_neighbor:
			if len(living_neighbor.living_neighbors) != len(living_neighbor.neighbors):
				edge_neighbor = living_neighbor
		return edge_neighbor
	
	@property
	def living_neighbors(self):
	
		living_neighbors = [n for n in set(self.neighbors) if n.alive]
		return living_neighbors

class Map:

	def __init__(self,width = 10, height = 10):

		self.width = width
		self.height = height
		self.g    = []
		for y in range(0,height):
			self.g.append([])
			for x in range(0,width):
				self.g[y].append([Tile(self,x,y)])

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

class TileMap(Map):

	def __init__(self,width=10,height=10):

		Map.__init__(self, width, height)
		self.tileset = Tileset()
		self.floors = pygame.surface.Surface(self.get_dimensions())
		self.walls = pygame.surface.Surface(self.get_dimensions())
		self.walls.set_colorkey((0,0,0))

	def get_dimensions(self):

		return(self.width * TILE_SIZE, self.height * TILE_SIZE)

	def render(self):

		for t in self:
			if t.attr['floor']:
				if t.attr.get('floor'):
					self.floors.blit(self.tileset.tiles[t.attr['floor']],(t.x * TILE_SIZE, t.y * TILE_SIZE))
			if t.attr['wall']:
				if t.attr.get('wall'):
					self.walls.blit(self.tileset.tiles[t.attr['wall']],(t.x * TILE_SIZE, t.y * TILE_SIZE))
	
		pygame.display.flip()

class LivingGrid(Map):

	def __init__(self,width = 10, height=10):

		Map.__init__(self, width, height)
		self.g    = []
		for y in range(0, height):
			self.g.append([])
			for x in range(0, width):
				self.g[y].append([Cell(self,x,y)])

	def __repr__(self):

		rtrn = ''
		for y in range(0,self.width-1):
			for x in range(0,self.height-1):
				rtrn+=self(x,y).alive and '%' or '.'
			rtrn+='\n'
		return rtrn

	def __gt__(self,other_grid):
		for c in self:
			if c.alive:
				if len(c.neighbors) == len(c.living_neighbors):
					other_grid(c.x,c.y).attr['wall']=False
					other_grid(c.x,c.y).attr['floor']=False
				else:
					tile = 0
					tile += c.edge_neighbor(0,-1) and 1 or 0
					tile += c.edge_neighbor(1,0) and 2 or 0
					tile += c.edge_neighbor(0,1) and 4 or 0
					tile += c.edge_neighbor(-1,0) and 8 or 0
					other_grid(c.x,c.y).attr['wall'] = tile
					other_grid(c.x,c.y).attr['floor']=17+random.randrange(0,3)
			else:
				other_grid(c.x,c.y).attr['wall']=False
				other_grid(c.x,c.y).attr['floor']=17+random.randrange(0,3)

	def spawn(self,chance=.5):
		for c in self:
			c.spawn(chance)

	def assign_living_neighbors(self):
		for c in self:
			c.assign_total_living_neighbors()

	def force_walls(self):
		for x in range(0,self.width):
			self(x,0).alive = True
			self(x,self.height-1).alive = True
		for y in range(0,self.height):
			self(0,y).alive = True
			self(self.width-1,y).alive = True
		
	def cycle(self,live_limit=4,die_limit=4):
		self.force_walls()
		self.assign_living_neighbors()
		for c in self:
			if c.total_living_neighbors < die_limit:
				c.alive = False
			if c.total_living_neighbors > live_limit:
				c.alive = True

pygame.init()
pygame.display.set_mode((TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT))

living_grid = LivingGrid(MAP_WIDTH,MAP_HEIGHT)
tile_map = TileMap(MAP_WIDTH,MAP_HEIGHT)
living_grid.spawn(.35)
living_grid.cycle(3,5)
living_grid.cycle()
living_grid.cycle()
living_grid > tile_map
tile_map.render()



if __name__ == "__main__":
	clock = pygame.time.Clock()
	running = True
	screen = pygame.display.get_surface()
	while running:
		screen.blit(tile_map.floors,(0,0))
		screen.blit(tile_map.walls,(0,0))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pg.QUIT:
				running = False
		clock.tick(20)