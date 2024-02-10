import dataclasses as _dc


@_dc.dataclass
class Pen:
	color:str = None
	width:int = 1
	style:int= 100 #solid pen


@_dc.dataclass
class Brush:
	color:str = None
	style:int = 100 #solid brush