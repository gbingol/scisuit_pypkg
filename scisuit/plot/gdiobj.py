import dataclasses as _dc




class Pen:
	def __init__(self, *args):

		assert isinstance(args[0], dict), "first argument must be dict"

		params:dict = args[0]

		self.color = params.get("edgecolor")
		if self.color != None:
			assert isinstance(self.color, str), "'color' must be string"

		self.style = params.get("linestyle")
		if self.style == None:
			self.style = params.get("ls")
		
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


		self.width = params.get("linewidth")
		if self.width == None:
			self.width = params.get("lw")
		
		if self.width == None:
			self.width = 1
		else:
			assert isinstance(self.width, int), "'width' must be integer"
			assert self.width>0, "width>0 expected"
	
	def __iter__(self):
		return iter([
			("style",self.style),
			("width", self.width),
			("color", self.color)])	




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

		self.color = params.get("facecolor")
		if self.color != None:
			assert isinstance(self.color, str), "'facecolor' must be string"

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
			("color", self.color)])