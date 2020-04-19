##second pass at a game of life

##to-do rules here

##need a cell class
##maps have grids
##we're going to make the grid coordinates a property somehow


import random


cell_number = 0

class Cell:

	def __init__(self, grid, x, y):

		self._x 		= x
		self._y 		= y
		self._grid 		= grid

	def neighbor(self,dx=0,dy=0):

		nx = self._x + dx
		ny = self._y + dy

		_cell = self._grid.cell(nx,ny)

		return _cell

	def neighbors(self):

		neighbors = set()
		neighbor = self.neighbor

		for dx in range(-1,2,2):
			for dy in range(-1,2,2):
				cell = neighbor(dx,dy)
				neighbors.add(cell)
		for dx in range(-1,2,2):
			cell = neighbor(dx,0)
			neighbors.add(cell)
		for dy in range(-1,2,2):
			cell = neighbor(0,dy)
			neighbors.add(cell)

		neighbors.discard(False)

		return neighbors


class Automata(Cell):

	def __init__(self, grid, x, y, alive=False):

		Cell.__init__(self, grid, x, y)
		self._alive 			= alive
		self._living_neighbors  = 0

	def check_living_neighbors(self):

		_living_neighbors = 0

		for c in self.neighbors():

			if c.alive:

				_living_neighbors+=1

		self.living_neighbors = _living_neighbors

	@property

	def living_neighbors(self):

		return self._living_neighbors

	@living_neighbors.setter

	def living_neighbors(self, living_neighbors):

		self._living_neighbors = living_neighbors

	@property

	def alive(self):

		return self._alive

	@alive.setter

	def alive(self,alive):

		self._alive = alive


class Grid:

	def __init__(self,size=10, cellType = Cell):

		self._size = size
		self._arrays = []

		for x in range (0,size-1):
			self._arrays.append([])
			for y in range(0,size-1):
				self._arrays[x].append(cellType(self,x,y))

	def cell(self,x,y):
		try:
			_cell = self._arrays[x][y]
		except(IndexError):
			_cell = False
		return _cell

class LifeGrid(Grid):

	def __init__(self,size=10):

		Grid.__init__(self,size,Automata)

	def randomize(self):

		for x in range(0,self._size-1):

			for y in range(0,self._size-1):

				live = random.choice([True,False])

				if live:

					self.cell(x,y).alive = True

				else:

					self.cell(x,y).alive = False

	def cycle(self):

		for y in range(0,self._size-1):

			for x in range(0,self._size-1):
			
				self.cell(x,y).check_living_neighbors()
	
		print(level.debug_output())
		print(level.debug_output(True))
		
		for x in range(0, self._size-1):

			for y in range(0, self._size-1):

				_cell = self.cell(x,y)

				if _cell.alive:

					if _cell.living_neighbors < 5:

						_cell.alive = False;

				else:

					if _cell.living_neighbors > 2:

						_cell.alive = True


	def debug_output(self, neighbor_mode=False):

		output = ''

		for y in range(0,self._size-1):

			for x in range(0,self._size-1):

				##how to actually get the results I want
				#there is definitely a shorter path
				#some sort of filter function in set

				if neighbor_mode:

					cell = self.cell(x,y)
					neighbors = cell.neighbors()
					neighbors = list(neighbors)
					_neighbors = 0
					for l,c in enumerate(neighbors):
						if c.alive:
							_neighbors+=1
					neighbors = _neighbors
					output 	 += str(neighbors)

				else:

					output += self.cell(x,y).alive and '%' or '.'

			output+='\n'

		return output

level = LifeGrid(3)
level.randomize()
level.cycle()