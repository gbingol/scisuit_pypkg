import dataclasses as _dc


__PEN_SOLID = 100
__PEN_DOT = 101
__PEN_LONGDASH = 102
__PEN_SHORTDASH = 103
__PEN_DOTDASH = 104
__PEN_TRANSPARENT = 106


@_dc.dataclass
class Pen:
	color:str = None
	width:int = 1
	style:str= "-" #solid pen

	def __post_init__(self):
		if self.color != None:
			assert isinstance(self.color, str), "'color' must be string"

		assert isinstance(self.style, str), "'style' must be str"

		assert isinstance(self.width, int), "'width' must be integer"
		assert self.width>0, "width>0 expected"

		_style1 = ["-",":","---", "--", "-.", "" ]
		_style2 = ["solid","dotted","ldashed", "dashed", "dashdot", "transparent" ]

		index = _style1.index(self.style) if self.style in _style1 else -1
		if index<0:
			indexalter = _style2.index(self.style) if self.style in _style2 else -1
			if indexalter<0:
				raise ValueError(",".join(_style1) + " or " + ",".join(_style2))
			else:
				self.style = _style1[indexalter]
		

	
	