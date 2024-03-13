class Pen:
	def __init__(self, *args):

		assert isinstance(args[0], dict), "first argument must be dict"

		params:dict = args[0]

		self.color = params.get("edgecolor") or params.get("ec")
		if self.color != None:
			assert isinstance(self.color, str|tuple|list), "'edgecolor' must be str|tuple|list"
		
		self.alpha = params.get("alpha")
		assert isinstance(self.alpha, None|float|int)

		self.style = params.get("linestyle") or params.get("ls")
		if self.style == None:
			self.style = "-"
		else:
			assert isinstance(self.style, str), "'style' must be str"
		
		_style1 = ["-",":","---", "--", "-.", "" ]
		_style2 = ["solid","dotted","ldashed", "dashed", "dashdot", "none" ]

		index = _style1.index(self.style) if self.style in _style1 else -1
		if index<0:
			index2 = _style2.index(self.style) if self.style in _style2 else -1

			#user has not provided from either style1 or style2, raise error
			if index2<0:
				raise ValueError(",".join(_style1) + " or " + ",".join(_style2))
			else:
				#located from style2, get equivalent style1
				self.style = _style1[index2]


		self.width = params.get("linewidth") or params.get("lw")
		if self.width == None:
			self.width = 1
		else:
			assert isinstance(self.width, int), "'width' must be integer"
			assert self.width>0, "width>0 expected"
	
	def __iter__(self):
		return iter([
			("style",self.style),
			("width", self.width),
			("color", self.color),
			("alpha", self.alpha)])	




__BRUSH_SOLID = 100 #"solid"
__BRUSH_TRANSPARENT = 106 #"none"
__BRUSH_BDIAGHATCH = 111 # "\"
__BRUSH_CROSSDIAGHATCH = 112 #"x"
__BRUSH_FDIAGHATCH = 113 #"/"
__BRUSH_CROSSHATCH = 114 #"+"
__BRUSH_HORIZHATCH =115 #"-"
__BRUSH_VERTHATCH = 116 # |

	
class Brush:
	def __init__(self, *args):
		assert isinstance(args[0], dict), "first argument must be dict"
		params:dict = args[0]

		self.color = params.get("facecolor") or params.get("fc")
		if self.color != None:
			assert isinstance(self.color, str|tuple|list), "'facecolor' must be str|tuple|list"

		self.alpha = params.get("alpha")
		assert isinstance(self.alpha, None|float|int)

		self.style = params.get("hatch")
		if self.style != None:
			assert isinstance(self.style, str), "'hatch' must be str"
		else:
			self.style = "solid"

		_hatches = ["solid", "none", "\\", "x", "/", "+", "-", "|"]
		_codes = [100, 106, 111, 112, 113, 114, 115, 116]

		index = _hatches.index(self.style) if self.style in _hatches else -1
		if index<0:
			raise ValueError("hatch types: " + ",".join(_hatches))
		else:
			self.style = _codes[index] #integer value for wxWidgets
	

	def __iter__(self):
		return iter([
			("style",self.style),
			("color", self.color),
			("alpha", self.alpha)])


class Font:
	def __init__(self, *args):
		assert isinstance(args[0], dict), "first argument must be dict"
		params:dict = args[0]
		
		self.size = params.get("size") or params.get("fontsize")
		if self.size != None:
			assert isinstance(self.size, int), "size or fontsize must be int"
			assert self.size>0, "size>0 expected"
		else:
			self.size = 11
		
		self.facename = params.get("fontname")
		if self.facename != None:
			assert isinstance(self.facename, str), "fontname must be str"
		else:
			self.facename = "Arial"

		self.weight:str = params.get("weight") or params.get("fontweight")
		if self.weight == None:
			self.weight = "normal"
		else:
			_weights = ["normal", "light", "bold", "heavy", "ultrabold"]
			if not self.weight in _weights:
				raise ValueError("weights: " + ",".join(_weights))
		
		self.style = params.get("style") or params.get("fontstyle")
		if self.style == None:
			self.style = "normal"
		else:
			_styles = ["normal", "italic", "oblique"]
			if not self.style in _styles:
				raise ValueError("weights: " + ",".join(_styles))
		
	
	def __iter__(self):
		return iter([
			("style",self.style),
			("facename", self.facename),
			("weight", self.weight),
			("size", self.size)
		])