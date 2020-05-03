import random

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