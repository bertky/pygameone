import xml.dom.minidom as minidom

## maps .tmx
## need csv and width,height(height could be implicit)
def parse_map(filename)
	map_file 	= file.open(filename)
	map_dom  	= minidom.parse(map_file).firstChild()
	layers   	= map_dom.getElementsByTagName('layer')
	_attr 		= dict(layers[0].attributes)
	dims 		= (str(_attr['width']),str(_attr['height']))
	floor_data  = [int(x) for x in (layers[0].getElementsByTagName('data')[0].firstChild.data.replace('\n','')).split(',')]
	walls_data  = [int(x) for x in (layers[1].getElementsByTagName('data')[0].firstChild.data.replace('\n','')).split(',')]
	floor_map   = []
	walls_map   = []
	for y in range(dims[1]):
		floor_map.append([])
		walls_map.append([])
		for x in range(dims[0]):
			floor_map[y].append(floor_data[i])
			walls_map[y].append(walls_data[i])
	return floor_map, walls_map

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
