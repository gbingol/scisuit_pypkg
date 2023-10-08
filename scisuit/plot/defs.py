import dataclasses as _dc
import scisuit.plot.gdi as _gdi
from ..defs import StrEnum as _StrEnum


#BAR Charts and Line Charts
CLUSTER = "c"
STACKED = "s"
PERCENTSTK = "%"

#Histogram Modes
HIST_DENSITY = "d"
HIST_FREQUENCY = "f"
HIST_RELFREQUENCY = "r"



@_dc.dataclass
class Trendline:
	class STYLE(_StrEnum):
		LINEAR = "linear"
		POLY = "poly"
		EXP = "exp"
		LOG = "log"
		POW = "pow"
	"""
	A class to define Trendline properties

	## Input:
	style: "linear", "poly", "exp", "log","pow" (Use STYLE class) \n
	degree: 2, >=2 expected when type is polynomial \n
	intercept: number expected \n
	color: "R G B" format, "255 255 125" \n
	width: >0 expected \n
	style: 100, 101, 102, 103, 104, 106 (default 102)
	"""
	style:str=STYLE.LINEAR
	degree:int = 2
	intercept:float=None
	line:_gdi.Pen = _gdi.Pen(color=None, width=1, style=_gdi.Pen.STYLE.LONGDASH)




class Marker:
	class STYLE:
		CIRCLE = "c"
		TRIANGLE = "t"
		SQUARE = "s"
		XMARKER = "x"
	"""
	A class to define marker properties

	## Input:
	style: "c", "s", "t", "x" (Use STYLE class)  \n	
	size: 5 #>0 expected \n
	fill: if specified, RGB "255 255 0" \n
	"""
	def __init__(
		self,
		style:str = STYLE.CIRCLE,
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