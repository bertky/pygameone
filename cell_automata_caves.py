# #cellular automata to generate cavelike structures
# cells should be self aware

import random

class Cell:

	def __init__(self,g,v,x,y):

		self.g   = g
		self.v   = v
		self.x   = x
		self.y   = y
		self.l_n = 0

	def __repr__(self):

		return "cell:"+str(self.x)+","+str(self.y)+":"+str(self.v)

	def spawn(self,chance):

		chance = max(0,min(1,chance))
		rnd = random.random()
		if rnd < chance:
			self.v = True

	def neighbor(self,dx,dy):

		nx, ny = self.x + dx, self.y + dy
		neighbor = self.g(nx,ny)
		return neighbor

	def assign_living_neighbors(self):
		walls = 8 - len(self.neighbors)
		self.l_n = len(self.living_neighbors) + walls

	@property
	def living_neighbors(self):
		
		living_neighbors = [n for n in set(self.neighbors) if n.v]
		return living_neighbors

	@property
	def neighbors(self):
		neighbors = []
		for dx in range(-1,2,2):
			for dy in range(-1,2,2):
				neighbors.append(self.neighbor(dx,dy))
		for dx in range(-1,2,2):
			neighbors.append(self.neighbor(dx,0))
		for dy in range(-1,2,2):
			neighbors.append(self.neighbor(0,dy))
		neighbors = [i for i in set(neighbors) if i]
		return neighbors



class Grid:

	def __init__(self,size=10):

		self.g    = []
		for y in range(0,size):
			self.g.append([])
			for x in range(0,size):
				self.g[y].append([Cell(self,False,x,y)])

	def __iter__(self):

		for y in self.g:
			for x in y:
				yield x[0]

	def __repr__(self):

		rtrn = ''
		for y in self.g:
			for x in y:
				rtrn+=x[0].v and '%' or '.'
			rtrn+='\n'
		return rtrn

	def __call__(self,x,y):
		exists = 0 <= y <= len(self.g) - 1 and 0 <=  x <= len(self.g) - 1
		return exists and self.g[y][x][0] or False

	def spawn(self,chance=.5):
		for c in self:
			c.spawn(chance)

	def assign_living_neighbors(self):
		for c in self:
			c.assign_living_neighbors()

	def force_walls(self):
		for z in range(0,len(self.g)):
			self(0,z).v = True
			self(len(self.g)-1,z).v = True
			self(z,0).v = True
			self(z,len(self.g)-1).v = True

	def cycle(self,live_limit=4,die_limit=4):
		#self.force_walls()
		self.assign_living_neighbors()
		for c in self:
			if c.l_n < die_limit:
				c.v = False
			if c.l_n > live_limit:
				c.v = True

grid = Grid(50)
grid.spawn(.45)
print(grid)
grid.cycle(5,3)
print(grid)
grid.cycle(5,3)
print(grid)
grid.cycle()
print(grid)
grid.cycle()
print(grid)
