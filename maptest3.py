## testing properties and catching errors in a map class
import random

class Cell:

	def __init__(self):

		self.alive = True

		self.neighbors = 0

	def _get_alive(self):

		return self.alive

	def _set_alive(self,b):

		self.alive = b

class Map:

	def __init__(self, size):

		self.size = size

		self.grid = []

		for i in range(0,size):

			self.grid.append([])

			for j in range(0,size):

				self.grid[i].append(Cell())

	def _get_cell(self,x,y):

		if 0 <= x <= self.size and 0 <= y <= self.size:

			return self.grid[x][y]

	def _assign_cell_neighbors(self,x,y):

		cell = self._get_cell(x,y)

		cell.neighbors = 0

		for dx in range(-1,2,2):
			
			nx = x + dx
			
			if 0 <= nx < self.size:

				new_neighbor = self._get_cell(nx,y)._get_alive()

				if new_neighbor:

					cell.neighbors+=1

		for dy in range(-1,2,2):
			
			ny = y + dy
			
			if 0 <= ny < self.size:

				new_neighbor = self._get_cell(x,ny)._get_alive()

				if new_neighbor:

					cell.neighbors+=1

	def _assign_grid_neighbors(self):

		for x in range(0, self.size):

			for y in range(0, self.size):

				self._assign_cell_neighbors(x,y)

	def _erode_grid(self):

		for x in range(0, self.size):

			for y in range(0, self.size):

				cell = self._get_cell(x,y)

				living = cell._get_alive()

				neighbors = cell.neighbors

				if not living and neighbors > 2:

					cell._set_alive(True)

				if living and neighbors < 2:

					cell._set_alive(False)

	def _solidify_grid(self):

		for x in range(0, self.size):

			for y in range(0, self.size):

				cell = self._get_cell(x,y)

				living = cell._get_alive()

				neighbors = cell.neighbors

				if not living and neighbors >= 3:

					cell._set_alive(True)

	def grid_cycle(self):

		self._assign_grid_neighbors()

		self._erode_grid()

		print(self.output())

		self._assign_grid_neighbors()

		self._solidify_grid()

		print(self.output())

	def randomize(self):

		for x in range(0,self.size):

			for y in range(0,self.size):

				cell = self._get_cell(x,y)

				life = random.choice([True,False])

				if life:

					cell._set_alive(True)

				else:

					cell._set_alive(False)

		self._assign_grid_neighbors()

	def output(self):

		output = ''

		for x in range(0,self.size):

			for y in range(0,self.size):

				if self._get_cell(x,y)._get_alive():

					output+='%'

				else:

					output+=' '

			output+='\n'

		return output

	def output_neighbors(self):

		output = ''

		for x in range(0,self.size):

			for y in range(0,self.size):

				output+=str(self._get_cell(x,y).neighbors)

			output+='\n'

		return output

level = Map(32)
level.randomize()
level.grid_cycle()
level.grid_cycle()
level.grid_cycle()