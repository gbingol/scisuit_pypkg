import ctypes as _ct
from .._ctypeslib import pydll as _pydll

import dataclasses as _dc
import numbers



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



def line(p1:tuple, p2:tuple, pen:Pen = Pen("0 0 0", 2))->None:
	"""
	p1: (x1, y1)
	p2: (x2, y2)
	pen: Pen object to specify width, color, style
	"""
	assert isinstance(p1, tuple), "p1 must be tuple"
	assert isinstance(p2, tuple), "p2 must be tuple"

	_p1 = [i for i in p1 if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p1 must contain exactly two real numbers"

	_p2 = [i for i in p2 if isinstance(i, numbers.Real)]
	assert len(_p2) == 2, "p2 must contain exactly two real numbers"

	_pydll.c_plot_gdi_line(
			_ct.c_double(p1[0]),
			_ct.c_double(p1[1]),
			_ct.c_double(p2[0]),
			_ct.c_double(p2[1]),
			vars(pen))


	
	
