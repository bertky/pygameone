import random
class Tile:
	def __init__(self,pos):
		self.pos 	= pos
		self.flags 	= set()
		self.dict  	= dict()
	def has_flag(self,flag):
		return flag in self.flags
	def add_flag(self,flag):
		self.flags.add(flag)
	def del_flag(self,flag):
		self.flags.discard(flag)
	def get_attr(self,attr):
		return self.dict.get(attr)
	def set_attr(self,attr,value):
		self.dict.update({attr:value})
	def __repr__(self):
		return str(self.pos)+str(self.flags)+str(self.dict)
class Tile_Batch:
	def __init__(self,tiles=None):
		self.tiles = set()
		self.add(tiles)
	def __iter__(self):
		for tile in self.tiles:
			yield tile
	def __len__(self):
		return len(self.tiles)
	def __add__(self,tile=False):
		self.add(tile)
	def __sub__(self,tile=False):
		self.subtract(tile)
	def __repr__(self):
		rtrn = ''
		for tile in self:
			rtrn += tile.pos+':'+tile.flags+':'+tile.dict+'\n'
		return rtrn
	def add(self,tile=False):
		if tile:
			if isinstance(tile,Tile):
				self.tiles.add(tile)
			else:
				l = isinstance(tile,list)
				s = isinstance(tile,set)
				t = isinstance(tile,tuple)
				b = isinstance(tile,Tile_Batch)
				if l or s or t or b:
					for member in tile:
						self.add(member)
		self.tiles.discard(None)
	def subtract(self,tile=False):
		if tile:
			if isinstance(tile,Tile):
				self.tiles.pop(tile)
			else:
				l = isinstance(tile,list)
				s = isinstance(tile,set)
				t = isinstance(tile,tuple)
				b = isinstance(tile,Tile_Batch)
				if l or s or t or b:
					for member in tile:
						self.subtract(member)
		self.tiles.discard(None)
	def get_flagged(self,flag='nil'):
		return Tile_Batch([tile for tile in self if tile.has_flag(flag)])
class Map:
	def __init__(self, dims):
		self.dims  	= dims
		self.flags 	= set()
		self.dict  	= dict()
		self.tiles 	= []
		for row in range(dims[1]):
			self.tiles.append([])
			for x in range(dims[0]):
				self.tiles[row].append(Tile((x,row)))
	def __call__(self, pos=(0,0),delta=(0,0),flag):
		x,y 	= pos
		dx,dy 	= delta
		nx,ny 	= x+dx,y+dy
		if 0 <= nx <= self.dims[0]-1 and 0 <= ny <= self.dims[1] -1:
			if not flag:
				return self.tiles[ny][nx]
			else
				tile = self.tiles[ny][nx]
				if tile.has_flag(flag):
					return tile

	def __repr__(self):
		rtrn=''
		for y in range(self.dims[1]):
			for x in range(self.dims[0]):
				tile 	= self((x,y))
				adj 	= tile.get_attr('adj_alive')
				rtrn 	+= str(adj)
			rtrn = rtrn + '\n'
		for y in range(self.dims[1]):
			for x in range(self.dims[0]):
				tile 	= self((x,y))
				alive 	= tile.has_flag('alive')
				rtrn 	+= alive and '$' or '.'
			rtrn = rtrn + '\n'
		for y in range(self.dims[1]):
			for x in range(self.dims[0]):
				tile 	= self((x,y))
				wall 	= tile.has_flag('wall')
				floor   = tile.has_flag('floor')
				rtrn 	+= wall and '%' or floor and '-' or ' '
			rtrn = rtrn + '\n'
		return rtrn
	def __iter__(self):
		for row in self.tiles:
			for entry in row:
				yield entry
	def has_flag(self,flag):
		return flag in self.flags
	def add_flag(self,flag):
		self.flags.add(flag)
	def del_flag(self,flag):
		self.flags.discard(flag)
	def border(self,pos=(0,0),dims=(10,10)):
		border  = Tile_Batch() 
		x,y 	= pos
		mw,mh 	= self.dims
		w,h 	= dims
		x = max(0,(min(x,mw-1)))
		y = max(0,(min(y,mh-1)))
		w = max(1,(min(w,mw-x-1)))
		h = max(1,(min(h,mh-y-1)))
		for i in range(w):
			border + self((x+i,y))
			border + self((x+i,y+h))
		for i in range(h):
			border + self((x,y+i))
			border + self((x+w,y+i))
		return border
	def adj_tiles(self,pos=(0,0),ortho=True,diag=True,flag=False):
		adj = Tile_Batch()
		if ortho:
			adj.add(self(pos,(0,-1)))
			adj.add(self(pos,(1,0)))
			adj.add(self(pos,(0,1)))
			adj.add(self(pos,(-1,0)))
		if diag:
			adj.add(self(pos,(-1,-1)))
			adj.add(self(pos,(1,-1)))
			adj.add(self(pos,(-1,1)))
			adj.add(self(pos,(1,1)))
		if flag:
			adj = Tile_Batch([tile for tile in adj if tile.has_flag(flag)])
		return adj
	def white_noise(self,flag='nil',p=0.5):
		for tile in self:
			if random.random() < p:
				tile.add_flag(flag)
	def cycle(self,death=4,life=4,p=0.5):
		if not self.has_flag('alive'):
			self.add_flag('alive')
			self.white_noise('alive',p)
			border = self.border((0,0),self.dims)
			for tile in border:
				tile.add_flag('alive')
		for tile in self:
			adj_alive = len(self.adj_tiles(tile.pos,flag='alive'))
			adj_tiles = len(self.adj_tiles(tile.pos))
			adj_edges = 8 - adj_tiles
			tile.set_attr('adj_alive',adj_alive + adj_edges)
		for tile in self:
			adj_alive = tile.get_attr('adj_alive')
			if tile.has_flag('alive'):
				if adj_alive < death:
					tile.del_flag('alive')
			else:
				if adj_alive > life:
					tile.add_flag('alive')
	def to_cavern(self):
		for tile in self:
			if tile.has_flag('alive'):
				adj_alive = len(self.adj_tiles(tile.pos,flag='alive'))
				adj_tiles = len(self.adj_tiles(tile.pos))
				if adj_alive != adj_tiles:
					tile.add_flag('wall')
			else:
				tile.add_flag('floor')
		for tile in self:
			if tile.has_flag('wall'):
				gid = 1
				gid += self(tile.pos,(0,-1)) 	and 1 or 0
				gid += self(tile.pos,(1,0)) 	and 2 or 0
				gid += self(tile.pos,(0,1))		and 4 or 0
				gid += self(tile.pos,(-1,0))	and 8 or 0
			

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
class Tileset:
	def __init__(self,filename):
		self.name 		= ''
		self.image 		= False
		self.img_dims 	= (0,0)
		self.set_dims   = (0,0)
		self.tile_dims  = (0,0)
		self.tiles  	= []
		self.parse_tileset(filename)
		self.fill_tiles()
	def __call__(self,i):
		tile = self.tiles[i]
		return tile
	def fill_tiles():
		tw, th = self.tile_dims
		for y in range(set_dims[1]):
			self.tiles.append([])
			for x in range(set_dims[0]):
				self.tiles[y].append([])
				rect = (x*tw, y*th, tw, th)		
				self.tiles.append(self.image.subsurface(rect))
	def parse_tileset(filename)
		set_file 	= file.open(filename+'.tmx')
		set_dom		= minidom.parse()
		set_attr 	= set_dom.getElementsByTagName('tileset').attributes.items()
		img_attr    = set_dom.getElementsByTagName('image').attributes.items()
		set_dict	= dict(set_attr+img_attr)
		self.name    	= set_dict['name']
		self.img        = pygame.image.load(set_dict['source']).convert
		self.img_dims   = (set_dict['width'],set_dict['height'])
		self.set_dims	= (set_dict['width']/set_dict['tilewidth'],set_dict['tilecount']/set_dict['columns'])
		self.tile_dims	= (set_dict['tilewidth'],set_dict['tileheight'])


level = Map((80,40))
level.cycle(p=0.45)
level.cycle()
level.cycle()
level.cycle()
level.cycle()
level.cycle()
level.place_walls()
print(level)