import ctypes as _ct
import numbers
from typing import Iterable as _Iterable

from .._ctypeslib import pydll as _pydll
from ..app import App as _App
from ..settings import START_APP_MAINLOOP


if START_APP_MAINLOOP:
	_app = _App()


def layout(nrows:numbers.Integral, ncols:numbers.Integral)->None:
	"""
	Partitions the current chart window into nrows and ncols \n
	(similar to a matrix with nrows and ncols) \n

	`nrows:` number of rows
	`ncols:` number of columns
	"""
	assert isinstance(nrows, numbers.Integral), "nrows must be integer."
	assert isinstance(ncols, numbers.Integral), "ncols must be integer."

	assert 0<nrows<=255, "0<nrows<=255 expected"
	assert 0<ncols<=255, "0<ncols<=255 expected"

	_pydll.c_plot_layout(
		_ct.c_int(nrows), 
		_ct.c_int(ncols))



def subplot(
		row:numbers.Integral, 
		col:numbers.Integral, 
		nrows:numbers.Integral = 1, 
		ncols:numbers.Integral = 1)->None:
	"""
	Must be called after the window is partitioned (by layout) to select a cell from the partition. \n

	`row:` row position of the cell (must be less than partition's number of rows),
	`col:` column position of the cell (must be less than partition's number of columns),
	`nrows:` number of rows the cell should span 
	`ncols:` number of columns the cell should span 
	"""
	assert isinstance(row, numbers.Integral), "row must be integer."
	assert isinstance(col, numbers.Integral), "col must be integer."
	assert isinstance(nrows, numbers.Integral), "nrows must be integer."
	assert isinstance(ncols, numbers.Integral), "ncols must be integer."

	assert 0 <= row <= 255, "0 <= row <= 255 expected"
	assert 0 <= col <= 255, "0 <= col <= 255 expected"
	assert 0 < nrows <=255, "0 < nrows <=255 expected"
	assert 0 < ncols <=255, "0 < ncols <=255 expected"

	_pydll.c_plot_subplot(
		_ct.c_int(row), 
		_ct.c_int(col), 
		_ct.c_int(nrows), 
		_ct.c_int(ncols))



def figure():
	"""Starts a new plot window"""
	_pydll.c_plot_figure()



def set_figsize(width = 640, height = 480):
	"""
	Adjusts current figure size in pixels. \n
	Must be called right before calling a function that 
	draws a chart (scatter, canvas, ...)

	### Example:
	plt.set_figsize(640, 480) \n
	plt.scatter()
	"""
	assert width>0, "width>0 expected."
	assert height>0, "height>0 expected."
	_pydll.c_plot_set_figsize(_ct.c_ulonglong(width), _ct.c_ulonglong(height))



def savefig(fullpath:str):
	"""Saves the current figure"""
	_pydll.c_plot_savefig(_ct.c_char_p(fullpath.encode()))



def title(label:str):
	"""Creates chart title"""
	assert isinstance(label, str), "label must be of type string."
	_pydll.c_plot_title(_ct.c_char_p(label.encode()))



def xlabel(label:str):
	"""Creates x-axis label"""
	assert isinstance(label, str), "label must be of type string."
	_pydll.c_plot_xlabel(_ct.c_char_p(label.encode()))



def ylabel(label:str):
	"""Creates y-axis label"""
	assert isinstance(label, str), "label must be of type string."
	_pydll.c_plot_ylabel(_ct.c_char_p(label.encode()))



def xlim(
		min:numbers.Real|None = None, 
		max:numbers.Real|None = None)->tuple|None:
	"""
	Sets or gets the x-limits of the current chart
	"""
	assert isinstance(min, numbers.Real|None), "min must be Real|None."
	assert isinstance(max, numbers.Real|None), "max must be Real|None."
	return _pydll.c_plot_axislim(_ct.py_object(min), _ct.py_object(max), _ct.c_char("x".encode()))



def ylim(
		min:numbers.Real|None = None, 
		max:numbers.Real|None = None)->tuple|None:
	"""
	Sets or gets the y-limits of the current chart
	"""
	assert isinstance(min, numbers.Real|None), "min must be Real|None."
	assert isinstance(max, numbers.Real|None), "max must be Real|None."
	return _pydll.c_plot_axislim(_ct.py_object(min), _ct.py_object(max), _ct.c_char("y".encode()))



def set_xticks(
		ticks:_Iterable, 
		labels=None, 
		align="center", 
		pos="bottom")->None:
	"""
	Sets the x-ticks and optionally labels
	`align:` "center", "left"
	`pos:` "top", "bottom"
	"""
	assert isinstance(ticks, _Iterable), "ticks must be Iterable object."
	
	assert isinstance(align, str), "align must be str."
	assert isinstance(pos, str), "pos must be str."

	assert align in ["center", "left"], "align: center or left."
	assert pos in ["top", "bottom"], "pos: top or bottom."

	_pydll.c_plot_set_xticks(
				_ct.py_object(ticks), 
				_ct.py_object(labels),
				_ct.c_char_p(align.encode()),
				_ct.c_char_p(pos.encode()))


def set_yticks(
		ticks:_Iterable, 
		labels=None, 
		align="center", 
		pos="left")->None:
	"""
	Sets the x-ticks and optionally labels.
	`align:` "center", "top", "bottom"
	`pos:` "left", "right"
	"""
	assert isinstance(ticks, _Iterable), "ticks must be Iterable object."

	assert isinstance(align, str), "align must be str."
	assert isinstance(pos, str), "pos must be str."

	assert align in ["center", "top", "bottom"], "align: center, top or bottom."
	assert pos in ["left", "right"], "pos: left or right."

	_pydll.c_plot_set_yticks(
				_ct.py_object(ticks), 
				_ct.py_object(labels),
				_ct.c_char_p(align.encode()),
				_ct.c_char_p(pos.encode()))
	


def set_xposition(position:numbers.Real)->None:
	"""
	Sets x-axis position
	`position:` A valid position within limits of y-axis
	"""
	assert isinstance(position, numbers.Real), "position must be Real."
	_pydll.c_plot_set_axispos(_ct.c_double(position), _ct.c_char("x".encode()))



def set_yposition(position:numbers.Real)->None:
	"""
	Sets y-axis position
	`position:` A valid position within limits of x-axis
	"""
	assert isinstance(position, numbers.Real), "position must be Real."
	_pydll.c_plot_set_axispos(_ct.c_double(position), _ct.c_char("y".encode()))



def xscale(value:str)->None:
	"""
	Sets x-axis scale
	`value:` "linear", "log"
	"""
	if not value in ["linear", "log"]:
		raise ValueError("value must be 'linear'', 'log'")
	
	_pydll.c_plot_axisscale(_ct.c_char_p(value.encode()), _ct.c_char("x".encode()))



def yscale(value:str)->None:
	"""
	Sets y-axis scale
	`value:` "linear", "log"
	"""
	if not value in ["linear", "log"]:
		raise ValueError("value must be 'linear'', 'log'")
	
	_pydll.c_plot_axisscale(_ct.c_char_p(value.encode()), _ct.c_char("y".encode()))



def legend(
		nrows:int|None = None, 
		ncols:int|None = None)->None:
	"""Create legend"""
	if nrows != None:
		assert isinstance(nrows, int), "nrows must be int."
		assert nrows>0, "nrows=None or >0 expected."
	if ncols != None:
		assert isinstance(ncols, int), "ncols must be int."
		assert ncols>0, "ncols=None or >0 expected."

	_pydll.c_plot_legend(_ct.py_object(nrows), _ct.py_object(ncols))



def show(antialiasing=False)->None:
	"""
	If configured starts the main loop.  
	Shows the chart(s)
	"""
	_pydll.c_plot_show(_ct.c_bool(antialiasing))

	if START_APP_MAINLOOP:
		_app.mainloop()