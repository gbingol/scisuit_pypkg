from ._gdiobj import Pen, Brush


class Marker:
	"""
	A class to define marker properties

	## Input:
	`style:` "c", "s", "t", "x"  \n	
	"""
	def __init__( self, style="c", size=5, **kwargs) -> None:
		_style = style or "c"
		_size = size or 5

		assert isinstance(_style, str),"'style' must be string"
		assert isinstance(_size, int), "'size' must be integer"
		assert _size>0, "size>0 expected"

		self.style = _style
		self.size = _size
		self.Pen = Pen(kwargs)
		self.Brush = Brush(kwargs)

	
	def __iter__(self):
		return iter([
			("style",self.style),
			("size", self.size),
			("fill", dict(iter(self.Brush))),
			("line", dict(iter(self.Pen)))
		])