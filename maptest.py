## testing properties and catching errors in a map class

class Map:

	def __init__(self):

		##hard coding for first tests

		self.grid = [[True,False],[False,True]]

	def _get_coords(self,x,y):

		try:
			point = False
			column = self.grid[x]
			try:
				point = column[y]
			except:
				print(y, "out of y range")
		except:
			print(x, 'out of x range')
		return point

##testing
print(map._get_coords(0,0))
print(map._get_coords(0,1))
print(map._get_coords(0,2))
print(map._get_coords(1,0))
print(map._get_coords(1,1))
print(map._get_coords(2,1))