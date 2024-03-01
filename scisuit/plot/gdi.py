import ctypes as _ct
from .._ctypeslib import pydll as _pydll

import dataclasses as _dc
import numbers



"""
Not meant to be used outside gdi module.
Constants are already available at __init__
Defined here for clarity
"""
_PEN_SOLID = 100
_BRUSH_TRANSPARENT = 106




@_dc.dataclass
class Pen:
	color:str = None
	width:int = 1
	style:int= _PEN_SOLID

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



@_dc.dataclass
class Font:
	facename:str = "Arial"
	color:str = "0 0 0" #black
	size:int = 11 # 11 points
	italic:bool = False
	bold: bool = False

	def __post_init__(self):
		if self.color != None:
			assert isinstance(self.color, str), "'color' must be string"

		assert isinstance(self.size, int), "'size' must be integer"
		assert self.size>0, "size>0 expected"

		assert isinstance(self.italic, bool), "'italic' must be bool"
		assert isinstance(self.italic, bool), "'italic' must be bool"



def line(p1:tuple, p2:tuple, pen:Pen = Pen("0 0 0", 2))->None:
	"""
	p1: (x1, y1)
	p2: (x2, y2)
	pen: Pen object to specify width, color, style
	"""
	assert isinstance(p1, tuple), "p1 must be tuple"
	assert isinstance(p2, tuple), "p2 must be tuple"
	assert isinstance(pen, Pen), "pen must be Pen object"

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
	

def rect(
		p:tuple, 
		width:numbers.Real, 
		height:numbers.Real, 
		pen:Pen = Pen("0 0 0", 1), 
		brush:Brush = Brush("255 255 255", _BRUSH_TRANSPARENT))->None:
	"""
	p: 		(x, y), top-left corner of the rectangle,
	width: 	width of rectangle (>0),
	height: height of rectangle (>0),
	pen: 	Pen object to specify width, color, style of boundaries,
	brush: 	Brush object to specify color, style of internal 
	"""
	assert isinstance(p, tuple), "p must be tuple"
	assert isinstance(width, numbers.Real), "width must be real number"
	assert isinstance(height, numbers.Real), "height must be real number"
	assert isinstance(pen, Pen), "pen must be Pen object"
	assert isinstance(brush, Brush), "brush must be Brush object"

	assert width>0, "width>0 expected"
	assert height>0, "height>0 expected"

	_p1 = [i for i in p if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers"

	_pydll.c_plot_gdi_rect(
			_ct.c_double(p[0]),
			_ct.c_double(p[1]),
			_ct.c_double(width),
			_ct.c_double(height),
			vars(pen),
			vars(brush))




def ellipse(
		p:tuple, 
		width:numbers.Real, 
		height:numbers.Real, 
		pen:Pen = Pen("0 0 0", 1), 
		brush:Brush = Brush("255 255 255", _BRUSH_TRANSPARENT))->None:
	"""
	p:	 	(x, y), center,
	width: 	half width (>0),
	height: half height (>0),
	pen: 	Pen object to specify width, color, style of boundaries,
	brush: 	Brush object to specify color, style of internal 
	"""
	assert isinstance(p, tuple), "p must be tuple"
	assert isinstance(width, numbers.Real), "width must be real number"
	assert isinstance(height, numbers.Real), "height must be real number"
	assert isinstance(pen, Pen), "pen must be Pen object"
	assert isinstance(brush, Brush), "brush must be Brush object"

	assert width>0, "width>0 expected"
	assert height>0, "height>0 expected"

	_p1 = [i for i in p if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers"

	_pydll.c_plot_gdi_ellipse(
			_ct.c_double(p[0]),
			_ct.c_double(p[1]),
			_ct.c_double(width),
			_ct.c_double(height),
			vars(pen),
			vars(brush))	
	

def text(
		p:tuple, 
		text:str,
		angle:float = 0.0,
		font:Font = Font())->None:
	"""
	p: 		(x, y), top-left,
	text: 	text to be drawn,
	angle: 	rotation angle (>0 is counterclockwise; the full angle is 360 degrees)
	font: 	Font object to specify color, point size, facename, italic, bold 
	"""
	assert isinstance(p, tuple), "p must be tuple"
	assert isinstance(angle, numbers.Real), "angle must be real number"
	assert isinstance(font, Font), "font must be Font object"


	_p1 = [i for i in p if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers"

	_pydll.c_plot_gdi_text(
			_ct.c_double(p[0]),
			_ct.c_double(p[1]),
			_ct.c_char_p(text.encode()),
			_ct.c_double(angle),
			_ct.c_char_p(font.color.encode()),
			vars(font))