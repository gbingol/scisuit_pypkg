import scisuit.plot.gdi as _gdi


class Trendline:
	"""
	A class to define Trendline properties

	## Input:
	style: "linear", "poly", "exp", "log","pow" (Use STYLE class) \n
	degree: 2, >=2 expected when type is polynomial \n
	intercept: number expected \n
	line: line properties
	"""
	def __init__(
		self, 
		style:str= "linear",
		degree:int=2, 
		intercept:float=None, 
		line:_gdi.Pen = _gdi.Pen(color=None, width=1, style=102), #PEN_LONGDASH
		label:str = None,
		show_stats:bool = False,
		show_equation:bool=False
		) -> None:

		self._style = style
		self._degree = degree
		self._intercept = intercept
		self._label = style if label == None else label
		self._line = vars(line) if line != None else None
		self._show_stats = show_stats
		self._show_equation = show_equation


	def __iter__(self):
		return iter([
			("style",self._style),
			("degree", self._degree),
			("intercept", self._intercept),
			("label", self._label),
			("line", dict(self._line) if self._line != None else None),
			("show_stats", self._show_stats),
			("show_equation", self._show_equation)
		])



class Marker:
	"""
	A class to define marker properties

	## Input:
	style: "c", "s", "t", "x" (Use STYLE class)  \n	
	size: 5 #>0 expected \n
	fill: if specified, RGB "255 255 0" \n
	"""
	def __init__(
		self,
		style:str = "c",
		size:int = 5 ,
		fill:_gdi.Brush = None,
		line:_gdi.Pen = None) -> None:

		assert style!=None,"'style' cannot be None"
		self._style = style
		self._size = size
		self._fill = vars(fill) if fill != None else None
		self._line = vars(line) if line != None else None
	
	def __iter__(self):
		return iter([
			("style",self._style),
			("size", self._size),
			("fill", dict(self._fill) if self._fill != None else None),
			("line", dict(self._line) if self._line != None else None)
		])