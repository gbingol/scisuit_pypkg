import dataclasses as _dc


@_dc.dataclass
class Pen:
	color:str = None
	width:int = 1
	style:int= 100 #solid pen

	def __post_init__(self):
		if self.color != None:
			assert isinstance(self.color, str), "'color' must be string"

		assert isinstance(self.style, int), "'style' must be integer"
		assert self.style>0, "style>0 expected"

		assert isinstance(self.width, int), "'width' must be integer"
		assert self.width>0, "width>0 expected"


@_dc.dataclass
class Brush:
	color:str = None
	style:int = 100 #solid brush

	def __post_init__(self):
		if self.color != None:
			assert isinstance(self.color, str), "'color' must be string"

		assert isinstance(self.style, int), "'style' must be integer"
		assert self.style>0, "style>0 expected"