# #cellular automata to generate cavelike structures
# cells should be self aware

import random


global once
once = False

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

	@property
	def living_neighbors(self):
	
		living_neighbors = [n for n in set(self.neighbors) if n.alive]
		return living_neighbors



class Map:

	def __init__(self,size=10):

		self.g    = []
		for y in range(0,size):
			self.g.append([])
			for x in range(0,size):
				self.g[y].append([Tile(self,x,y)])

	def __iter__(self):

		for y in self.g:
			for x in y:
				yield x[0]

	def __repr__(self):

		rtrn = ''
		for y in self.g:
			for x in y:
				rtrn+=x[0].attr['wall'] and '%' or ' '
			rtrn+='\n'
		return rtrn

	def __call__(self,x,y):
		exists = 0 <= y <= len(self.g) - 1 and 0 <=  x <= len(self.g) - 1
		return exists and self.g[y][x][0] or False

class LivingGrid(Map):

	def __init__(self,size=10):

		Map.__init__(self,size)
		self.g    = []
		for y in range(0,size):
			self.g.append([])
			for x in range(0,size):
				self.g[y].append([Cell(self,x,y)])

	def __repr__(self):

		rtrn = ''
		for y in self.g:
			for x in y:
				rtrn+=x[0].alive and '%' or '.'
			rtrn+='\n'
		return rtrn

	def __gt__(self,other_grid):
		if len(self.g) <= len(other_grid.g):
			for c in self:
				if c.alive:
					other_grid(c.x,c.y).attr['wall']=True
				else:
					other_grid(c.x,c.y).attr['wall']=False

	def spawn(self,chance=.5):
		for c in self:
			c.spawn(chance)

	def assign_living_neighbors(self):
		for c in self:
			c.assign_total_living_neighbors()

	def force_walls(self):
		for z in range(0,len(self.g)):
			self(0,z).alive = True
			self(len(self.g)-1,z).alive = True
			self(z,0).alive = True
			self(z,len(self.g)-1).alive = True
		
	def cycle(self,live_limit=4,die_limit=4):
		self.force_walls()
		self.assign_living_neighbors()
		for c in self:
			if c.total_living_neighbors < die_limit:
				c.alive = False
			if c.total_living_neighbors > live_limit:
				c.alive = True
		
grid = Map(50)
cell_grid = LivingGrid(50)
cell_grid.spawn(.475)
cell_grid.cycle()
cell_grid.cycle(6,3)
cell_grid.cycle(4,3)
cell_grid.cycle(5,3)
cell_grid > grid
print(grid)