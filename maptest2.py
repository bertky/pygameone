## testing properties and catching errors in a map class

class Map:


	def __init__(self):

		##hard coding for first tests
		#self.grid = [[[0],[1]],[[2],[3]]]
		self.grid = [[{"girl":"alice"},{"girl":"betty"}],[{"girl":"cathyy"},{"girl":"diane"}]]

	def _get_cell(self,x,y):

		try:
			self.grid[x]
			try:
				cell = self.grid[x][y]
			except:
				print(y, "out of y range")
		except:
			print(x, 'out of x range')
		return cell

	def _get_value(self,x,y,key):

		try:
			cell = self._get_cell(x,y)
		except:
			print('could not get',x,y)
		try:
			value = cell.get(key)
		except:
			print("could not get",key,"from",x,y)
		return value

	def _set_value(self,x,y,key,value):

		try:
			cell= self._get_cell(x,y)
		except:
			print('could not get',x,y)
		try:
			cell.update({key:value})
		except:
			print("could not assign",value,"to",key,"at",x,y)


##testing
map = Map()
print(map._get_cell(0,0))
print(map._get_value(0,0,"girl"))
map._set_value(0,0,"girl","erica")
print(map._get_cell(0,0))
