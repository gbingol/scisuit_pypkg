import ctypes as _ct
from numbers import Real as _Real
from typing import Iterable as _Iterable

from .._ctypeslib import pydll as _pydll
from ._gdiobj import Brush, Font, Pen


def text(
		xy:tuple|list, 
		label:str,
		rotation:float = 0.0,
		hanchor:str = "l",
		vanchor:str = "t",
		**kwargs)->int:
	"""
	xy: (x, y), top-left,
	label: text to be drawn,
	rotation: rotation in degrees (>0 is counter-clockwise)
	hanchor: horizontal anchor, "l", "c" "r" for left, center, right.
	vanchor: vertical anchor, "t", "c", "b" for top, center and bottom
	labelcolor: label color
	"""
	assert isinstance(xy, tuple|list), "xy must be tuple|list."
	assert isinstance(label, str), "label must be string."
	assert isinstance(rotation, _Real), "rotation must be real number."

	_p1 = [i for i in xy if isinstance(i, _Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers."
	
	_color = kwargs.get("labelcolor") or "#000000"
	assert isinstance(_color, str|tuple|list), "color must be str|tuple|list."

	assert isinstance(hanchor, str), "hanchor must be str."
	assert hanchor.upper() in ["L", "C", "R"], "hanchor must be 'l', 'c', 'r' ."

	assert isinstance(vanchor, str), "vanchor must be str"
	assert vanchor.upper() in ["T", "C", "B"], "vanchor must be 't', 'c', 'b' ."

	return _pydll.c_plot_gdi_text(
			_ct.c_double(xy[0]),
			_ct.c_double(xy[1]),
			_ct.c_char_p(label.encode()),
			_ct.c_double(rotation),
			_ct.c_char(hanchor.upper().encode()),
			_ct.c_char(vanchor.upper().encode()),
			_ct.c_char_p(_color.encode()),
			dict(Font(kwargs)))



def marker(
		xy:tuple|list, 
		type:str = "c",
		size:int = 5,
		label:str = "",
		**kwargs)->int:
	"""
	`xy:`	(x, y), centroid,
	`type:`	type of the marker, "c", "t", "r", "x",
	`size:`	size of the marker in pixels
	"""

	assert isinstance(xy, tuple|list), "xy must be tuple|list."
	assert isinstance(type, str), "type must be string."
	assert isinstance(size, int), "size must be int."
	assert isinstance(label, str), "label must be str."

	assert 1<size<=100, "1 < size <= 100 expected."

	_p1 = [i for i in xy if isinstance(i, _Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers."

	return _pydll.c_plot_gdi_marker(
			_ct.c_double(xy[0]),
			_ct.c_double(xy[1]),
			_ct.c_char_p(type.encode()),
			_ct.c_uint8(size),
			_ct.c_char_p(label.strip().encode()),
			dict(Pen(kwargs)),
			dict(Brush(kwargs)))



def arc(
		center:tuple|list, 
		p1:tuple|list, 
		p2:tuple|list,
		label:str = "",
		**kwargs)->int:
	"""
	`center:` (x, y) -> center point of arc
	`p1:` (x1, y1) -> start of arc
	`p2:` (x2, y2) -> end of arc

	## Note:
	- The arc is drawn in a counter-clockwise direction between the start and the end points.
	- To plot a circular arc, the plot area must be a square.
	"""


	assert isinstance(center, tuple|list), "center must be tuple|list."
	assert isinstance(p1, tuple|list), "p1 must be tuple|list."
	assert isinstance(p2, tuple|list), "p2 must be tuple|list."
	assert isinstance(label, str), "label must be str."

	_c = [i for i in center if isinstance(i, _Real)]
	assert len(_c) == 2, "center must contain exactly two real numbers."

	_p1 = [i for i in p1 if isinstance(i, _Real)]
	assert len(_p1) == 2, "p1 must contain exactly two real numbers."

	_p2 = [i for i in p2 if isinstance(i, _Real)]
	assert len(_p2) == 2, "p2 must contain exactly two real numbers."

	return _pydll.c_plot_gdi_arc(
			_ct.c_double(p1[0]),
			_ct.c_double(p1[1]),
			_ct.c_double(p2[0]),
			_ct.c_double(p2[1]),
			_ct.c_double(center[0]),
			_ct.c_double(center[1]),
			_ct.c_char_p(label.strip().encode()),
			dict(Pen(kwargs)),
			dict(Brush(kwargs)))



def arrow(
		p1:tuple|list, 
		p2:tuple|list, 
		angle:_Real = 45, #45 degrees
		length:float = 0.1, #10% length of main-line
		label:str = "",
		**kwargs)->int:
	"""
	`p1, p2:` (x1, y1), (x2, y2) coordinate of the main-line
	`angle:` angle between the two head-lines
	`length:` ratio of the length of the head-line to the main-line
	"""

	assert isinstance(p1, tuple|list), "p1 must be tuple|list."
	assert isinstance(p2, tuple|list), "p2 must be tuple|list."
	assert isinstance(angle, _Real), "angle must be Real."
	assert isinstance(length, float), "length must be float."
	assert isinstance(label, str), "label must be str."

	_p1 = [i for i in p1 if isinstance(i, _Real)]
	assert len(_p1) == 2, "p1 must contain exactly two real numbers."

	_p2 = [i for i in p2 if isinstance(i, _Real)]
	assert len(_p2) == 2, "p2 must contain exactly two real numbers."

	assert 5 < angle <=180, "5 < angle <=180 expected." 
	assert 0.01 < length < 1, "0.01 < length < 1 expected."

	return _pydll.c_plot_gdi_arrow(
			_ct.c_double(p1[0]),
			_ct.c_double(p1[1]),
			_ct.c_double(p2[0]),
			_ct.c_double(p2[1]),
			_ct.c_double(angle),
			_ct.c_double(length),
			_ct.c_char_p(label.strip().encode()),
			dict(Pen(kwargs)))



def curve(
		x: _Iterable, 
		y:_Iterable, 
		label:str = "",
		**kwargs)->int:
	"""
	Draws a smooth curve between (x1, y1), (x2, y2), ..., (xn, yn). 
	The curve is only guaranteed to pass from (x1, y1) and (xn, yn).

	`x:` x values
	`y:` y values
	"""

	assert isinstance(x, _Iterable), "x must be Iterable."
	assert isinstance(y, _Iterable), "y must be Iterable."
	assert isinstance(label, str), "label must be str."

	#pre-check
	assert len(x) == len(y), "x and y must have same lengths."

	_x = [i for i in x if isinstance(i, _Real)]
	assert len(_x) >= 3, "x must contain at least 3 real numbers."

	_y = [i for i in y if isinstance(i, _Real)]
	assert len(_y) >= 3, "y must contain at least 3 real numbers."

	#processed-check
	assert len(_x) == len(_y), "x and y must have same lengths."

	return _pydll.c_plot_gdi_curve(
			x, 
			y, 
			_ct.c_char_p(label.strip().encode()),
			dict(Pen(kwargs)))



def ellipse(
		xy:tuple|list, 
		width:_Real, 
		height:_Real, 
		label:str = "",
		**kwargs)->int:
	"""
	xy:	 	(x, y), center,
	width: 	half width (>0),
	height: half height (>0),
	"""

	assert isinstance(xy, tuple|list), "p must be tuple|list."
	assert isinstance(width, _Real), "width must be real number."
	assert isinstance(height, _Real), "height must be real number."
	assert isinstance(label, str), "label must be str."
	
	assert width>0, "width>0 expected."
	assert height>0, "height>0 expected."

	_p1 = [i for i in xy if isinstance(i, _Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers."

	if kwargs.get("hatch") == None:
		kwargs["hatch"] = "none"

	return _pydll.c_plot_gdi_ellipse(
			_ct.c_double(xy[0]),
			_ct.c_double(xy[1]),
			_ct.c_double(width),
			_ct.c_double(height),
			_ct.c_char_p(label.strip().encode()),
			dict(Pen(kwargs)),
			dict(Brush(kwargs)))	



def line(
		p1:tuple|list, 
		p2:tuple|list, 
		label:str = "",
		**kwargs)->int:
	"""
	`p1:` (x1, y1)
	`p2:` (x2, y2)
	`label:` After stripping, if len(label)>0, it is shown in legend
	"""
	assert isinstance(p1, tuple|list), "p1 must be tuple|list."
	assert isinstance(p2, tuple|list), "p2 must be tuple|list."
	assert isinstance(label, str), "label must be str."

	_p1 = [i for i in p1 if isinstance(i, _Real)]
	assert len(_p1) == 2, "p1 must contain exactly two real numbers."

	_p2 = [i for i in p2 if isinstance(i, _Real)]
	assert len(_p2) == 2, "p2 must contain exactly two real numbers."

	return _pydll.c_plot_gdi_line(
			_ct.c_double(p1[0]),
			_ct.c_double(p1[1]),
			_ct.c_double(p2[0]),
			_ct.c_double(p2[1]),
			_ct.c_char_p(label.strip().encode()),
			dict(Pen(kwargs)))
	


def polygon(
		xy:_Iterable, 
		label:str = "",
		**kwargs)->int:
	"""
	Draws a polygon between (x1, y1), (x2, y2), ..., (xn, yn). 
	The first and last points are automatically closed.

	At least 3 points expected.
	"""

	assert isinstance(xy, _Iterable), "xy must be Iterable."
	assert len(xy)>=3, "x must contain at least 3 Iterables."

	assert isinstance(label, str), "label must be str."
	
	for v in xy:
		assert isinstance(v, _Iterable), "xy must contain Iterables."
		assert len(v) == 2, "Each iterable's length in xy must be exactly equal to 2."
		_x = [i for i in v if isinstance(i, _Real)]
		assert len(_x) == 2, "Each iterable in xy must contain exactly two Real numbers."
	
	x, y = list(zip(*xy))

	return _pydll.c_plot_gdi_polygon(
			x, y, 
			_ct.c_char_p(label.strip().encode()),
			dict(Pen(kwargs)), 
			dict(Brush(kwargs)))




def rect(
		xy:tuple|list, 
		width:_Real, 
		height:_Real, 
		label:str = "",
		**kwargs)->int:
	"""
	xy:	(x, y), bottom-left corner of the rectangle,
	width: 	width of rectangle (>0),
	height: height of rectangle (>0), 
	"""	

	assert isinstance(xy, tuple|list), "xy must be tuple|list."
	assert isinstance(width, _Real), "width must be real number."
	assert isinstance(height, _Real), "height must be real number."
	assert isinstance(label, str), "label must be str."

	assert width>0, "width>0 expected."
	assert height>0, "height>0 expected."

	_p1 = [i for i in xy if isinstance(i, _Real)]
	assert len(_p1) == 2, "p must contain exactly two real numbers."

	kwargs["hatch"] = kwargs.get("hatch") or "none" #make it transparent by default

	return _pydll.c_plot_gdi_rect(
			_ct.c_double(xy[0]),
			_ct.c_double(xy[1]),
			_ct.c_double(width),
			_ct.c_double(height),
			_ct.c_char_p(label.strip().encode()),
			dict(Pen(kwargs)),
			dict(Brush(kwargs)))



def makegroup(
		owner:int, 
		members:_Iterable[int])->None:
	"""
	sets the properties of members based on owner's properties
	
	## Inputs:
	`owner:` A gdi object whose properties will affect members' properties,
	`members:` gdi object(s) whose properties will be synched with owner

	## Note: 
	This function is rather useful (meaningful) if properties will be manipulated at runtime.
	"""
	assert isinstance(owner, int), "owner must be int."

	assert isinstance(members, _Iterable), "members must be Iterable object."
	_target = [i for i in members if isinstance(i, int)]
	assert len(_target) == len(members), "members must contain only int."

	_pydll.c_plot_gdi_makegroup(
		_ct.c_ulonglong(owner), 
		_ct.py_object(set(members)) #unique ids
		)