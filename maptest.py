## testing properties and catching errors in a map class

class Map:

	tiles = [{"kind":"wall","block":True},{"kind":"floor","block":False}]

	def __init__(self):

		##hard coding for first tests

		self.grid = [[[0],[1]],[[2],[3]]]

	def _get_coords(self,x,y):

		try:
			self.grid[x]
			try:
				position = self.grid[x][y]
			except:
				print(y, "out of y range")
		except:
			print(x, 'out of x range')
		return position, position[0]

	def _get_value(self,x,y):

		try:
			pos, value = self._get_coords(x,y)
		except:
			print('could not get',x,y)
		return value

	def _set_value(self,x,y,new_value):

		try:
			pos, old_value = self._get_coords(x,y)
			pos[0] = new_value
		except:
			print('could not get',x,y)


##testing
map = Map()
print(map._get_value(0,0))
map._set_value(0,0,{'alice'})
print(map._get_value(0,0))