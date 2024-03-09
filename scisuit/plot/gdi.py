import ctypes as _ct
import dataclasses as _dc
import numbers
import math
from typing import Iterable as _Iterable

from .._ctypeslib import pydll as _pydll
from .gdiobj import Pen, Brush, Font




def text(
		xy:tuple|list, 
		label:str,
		rotation:float = 0.0,
		**kwargs)->None:
	"""
	xy: 	(x, y), top-left,
	label: 	text to be drawn,
	rotation: rotation angle (>0 is counterclockwise; the full angle is 360 degrees)
	color: label color 
	"""
	assert isinstance(xy, tuple) or isinstance(xy, list), "xy must be tuple|list"
	assert isinstance(label, str), "label must be string"
	assert isinstance(rotation, numbers.Real), "rotation must be real number"

	_p1 = [i for i in xy if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers"
	
	_color = kwargs.get("labelcolor") or "0 0 0"
	assert isinstance(_color, str), "color must be str"


	_pydll.c_plot_gdi_text(
			_ct.c_double(xy[0]),
			_ct.c_double(xy[1]),
			_ct.c_char_p(label.encode()),
			_ct.c_double(rotation),
			_ct.c_char_p(_color.encode()),
			dict(Font(kwargs)))



def marker(
		xy:tuple|list, 
		type:str = "c",
		size:int = 5,
		**kwargs)->None:
	"""
	`xy:`	(x, y), centroid,
	`type:`	type of the marker, "c", "t", "r", "x",
	`size:`	size of the marker in pixels
	"""

	assert isinstance(xy, tuple) or isinstance(xy, list), "xy must be tuple|list"
	assert isinstance(type, str), "type must be string"
	assert isinstance(size, int), "size must be int"

	assert 1<size<=100, "1 < size <= 100 expected"

	_p1 = [i for i in xy if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers"

	_pydll.c_plot_gdi_marker(
			_ct.c_double(xy[0]),
			_ct.c_double(xy[1]),
			_ct.c_char_p(type.encode()),
			_ct.c_uint8(size),
			dict(Pen(kwargs)),
			dict(Brush(kwargs)))



def arc(
		center:tuple|list, 
		p1:tuple|list, 
		p2:tuple|list,
		**kwargs)->None:
	"""
	`center:` (x, y) -> center point of arc
	`p1:` (x1, y1) -> start of arc
	`p2:` (x2, y2) -> end of arc

	## Note:
	To be able to plot a circular arc, the plot area must be a square.
	"""


	assert isinstance(center, tuple) or isinstance(center, list), "center must be tuple|list"
	assert isinstance(p1, tuple) or isinstance(p1, list), "p1 must be tuple|list"
	assert isinstance(p2, tuple) or isinstance(p2, list), "p2 must be tuple|list"

	_c = [i for i in center if isinstance(i, numbers.Real)]
	assert len(_c) == 2, "center must contain exactly two real numbers"

	_p1 = [i for i in p1 if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p1 must contain exactly two real numbers"

	_p2 = [i for i in p2 if isinstance(i, numbers.Real)]
	assert len(_p2) == 2, "p2 must contain exactly two real numbers"

	_pydll.c_plot_gdi_arc(
			_ct.c_double(p1[0]),
			_ct.c_double(p1[1]),
			_ct.c_double(p2[0]),
			_ct.c_double(p2[1]),
			_ct.c_double(center[0]),
			_ct.c_double(center[1]),
			dict(Pen(kwargs)),
			dict(Brush(kwargs)))



def arrow(
		p1:tuple|list, 
		p2:tuple|list, 
		angle:numbers.Real = 45, #45 degrees
		length:float = 0.1, #10% length of main-line
		**kwargs)->None:
	"""
	`p1, p2:` (x1, y1), (x2, y2) coordinate of the main-line
	`angle:` angle between the two head-lines
	`length:` ratio of the length of the head-line to the main-line
	"""

	assert isinstance(p1, tuple) or isinstance(p1, list), "p1 must be tuple|list"
	assert isinstance(p2, tuple) or isinstance(p2, list), "p2 must be tuple|list"
	assert isinstance(angle, numbers.Real), "angle must be float"
	assert isinstance(length, float), "length must be float"

	_p1 = [i for i in p1 if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p1 must contain exactly two real numbers"

	_p2 = [i for i in p2 if isinstance(i, numbers.Real)]
	assert len(_p2) == 2, "p2 must contain exactly two real numbers"

	assert 5 < angle <=180, "5 < angle <=180 expected" 
	assert 0.01 < length < 1, "0.01 < length < 1 expected"

	_pydll.c_plot_gdi_arrow(
			_ct.c_double(p1[0]),
			_ct.c_double(p1[1]),
			_ct.c_double(p2[0]),
			_ct.c_double(p2[1]),
			_ct.c_double(angle),
			_ct.c_double(length),
			dict(Pen(kwargs)))



def curve(
		x: _Iterable, 
		y:_Iterable, 
		**kwargs)->None:
	"""
	Draws a smooth curve between (x1, y1), (x2, y2), ..., (xn, yn). 
	The curve is only guaranteed to pass from (x1, y1) and (xn, yn).

	`x:` x values
	`y:` y values
	"""

	assert isinstance(x, _Iterable), "x must be Iterable"
	assert isinstance(y, _Iterable), "y must be Iterable"

	#pre-check
	assert len(x) == len(y), "x and y must have same lengths"

	_x = [i for i in x if isinstance(i, numbers.Real)]
	assert len(_x) >= 3, "x must contain at least 3 real numbers"

	_y = [i for i in y if isinstance(i, numbers.Real)]
	assert len(_y) >= 3, "y must contain at least 3 real numbers"

	#processed-check
	assert len(_x) == len(_y), "x and y must have same lengths"

	_pydll.c_plot_gdi_curve(x, y, dict(Pen(kwargs)))



def ellipse(
		xy:tuple|list, 
		width:numbers.Real, 
		height:numbers.Real, 
		**kwargs)->None:
	"""
	xy:	 	(x, y), center,
	width: 	half width (>0),
	height: half height (>0),
	"""

	assert isinstance(xy, tuple) or isinstance(xy, list), "p must be tuple|list"
	assert isinstance(width, numbers.Real), "width must be real number"
	assert isinstance(height, numbers.Real), "height must be real number"
	

	assert width>0, "width>0 expected"
	assert height>0, "height>0 expected"

	_p1 = [i for i in xy if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers"

	_pydll.c_plot_gdi_ellipse(
			_ct.c_double(xy[0]),
			_ct.c_double(xy[1]),
			_ct.c_double(width),
			_ct.c_double(height),
			dict(Pen(kwargs)),
			dict(Brush(kwargs)))	



def line(
		p1:tuple|list, 
		p2:tuple|list, 
		label:str = "",
		**kwargs)->None:
	"""
	`p1:` (x1, y1)
	`p2:` (x2, y2)
	`label:` a text to be shown along with line

	## Note:
	If label is specified:
	`labeldist:float:` (0, 1) pos = start + labeldist*length
	`labelcolor:str` label color
	"""

	assert isinstance(p1, tuple) or isinstance(p1, list), "p1 must be tuple|list"
	assert isinstance(p2, tuple) or isinstance(p2, list), "p2 must be tuple|list"


	_p1 = [i for i in p1 if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p1 must contain exactly two real numbers"

	_p2 = [i for i in p2 if isinstance(i, numbers.Real)]
	assert len(_p2) == 2, "p2 must contain exactly two real numbers"


	_pydll.c_plot_gdi_line(
			_ct.c_double(p1[0]),
			_ct.c_double(p1[1]),
			_ct.c_double(p2[0]),
			_ct.c_double(p2[1]),
			dict(Pen(kwargs)))
	
	_txt = label.rstrip()
	_txt = _txt.lstrip()

	if _txt != "":
		_labelcolor = kwargs.get("labelcolor") or "0 0 0"
		_labeldist = kwargs.get("labeldist") or 0.45
		assert isinstance(_labeldist, float), "labeldist must be float"
		assert isinstance(_labelcolor, str), "labelcolor must be str"

		dy = p2[1] - p1[1]
		dx = p2[0] - p1[0]
		Slope = math.atan2(dy, dx)

		TL = (
				p1[0] + _labeldist * math.cos(Slope) ,
				p1[1] + _labeldist * math.sin(Slope))

		
		#As of this point slope is in degrees (0, 180) or (0, -180)
		Slope = Slope*180/math.pi

		if Slope<0:
			Slope += 180

		if Slope>90:
			Slope = 90 - Slope
	
		text(TL, label, Slope, **kwargs)



def polygon(
		x: _Iterable, 
		y:_Iterable, 
		**kwargs)->None:
	"""
	Draws a polygon between (x1, y1), (x2, y2), ..., (xn, yn). 
	The first and last points are automatically closed.

	`x:` x values
	`y:` y values
	"""

	assert isinstance(x, _Iterable), "x must be Iterable"
	assert isinstance(y, _Iterable), "y must be Iterable"

	#pre-check
	assert len(x) == len(y), "x and y must have same lengths"

	_x = [i for i in x if isinstance(i, numbers.Real)]
	assert len(_x) >= 3, "x must contain at least 3 real numbers"

	_y = [i for i in y if isinstance(i, numbers.Real)]
	assert len(_y) >= 3, "y must contain at least 3 real numbers"

	#processed-check
	assert len(_x) == len(_y), "x and y must have same lengths"

	_pydll.c_plot_gdi_polygon(
			x, y, 
			dict(Pen(kwargs)), 
			dict(Brush(kwargs)))




def rect(
		xy:tuple|list, 
		width:numbers.Real, 
		height:numbers.Real, 
		**kwargs)->None:
	"""
	xy: 		(x, y), top-left corner of the rectangle,
	width: 	width of rectangle (>0),
	height: height of rectangle (>0),
	pen: 	Pen object to specify width, color, style of boundaries,
	brush: 	Brush object to specify color, style of internal 
	"""	

	assert isinstance(xy, tuple) or isinstance(xy, list), "xy must be tuple|list"
	assert isinstance(width, numbers.Real), "width must be real number"
	assert isinstance(height, numbers.Real), "height must be real number"

	assert width>0, "width>0 expected"
	assert height>0, "height>0 expected"

	_p1 = [i for i in xy if isinstance(i, numbers.Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers"

	_pydll.c_plot_gdi_rect(
			_ct.c_double(xy[0]),
			_ct.c_double(xy[1]),
			_ct.c_double(width),
			_ct.c_double(height),
			dict(Pen(kwargs)),
			dict(Brush(kwargs)))
