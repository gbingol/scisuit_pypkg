from .gdiobj import Pen, Brush


class Marker:
	"""
	A class to define marker properties

	## Input:
	`style:` "c", "s", "t", "x"  \n	
	`size:` 5 #>0 expected \n
	`fill:` if specified, RGB "255 255 0" \n
	"""
	def __init__(
		self,
		style:str = "c",
		size:int = 5 ,
		**kwargs) -> None:

		assert isinstance(style, str),"'style' must be string"
		assert isinstance(size, int), "'size' must be integer"
		assert size>0, "size>0 expected"

		self.style = style
		self.size = size
		self.Pen = Pen(kwargs)
		self.Brush = Brush(kwargs)

	
	def __iter__(self):
		return iter([
			("style",self.style),
			("size", self.size),
			("fill", dict(iter(self.Brush))),
			("line", dict(iter(self.Pen)))
		])