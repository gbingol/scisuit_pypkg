import ctypes as _ct
import numbers
from typing import Iterable as _Iterable

from .._ctypeslib import pydll as _pydll
from ..app import App as _App
from ._chartelems import Marker
from ._gdiobj import Brush, Pen



_app = _App()





#-----------------------------------------------------------------------------------

def boxplot(
	data:_Iterable, 
	label:str|None = None, 
	**kwargs):
	"""
	Plots box-whisker chart.

	`data:` Data to be plotted 
	`label:` Name of the series
	"""
	assert isinstance(data, _Iterable), "'data' must be iterable."
	
	if label != None:
		assert isinstance(label, str), "'label' must be string."

	return _pydll.c_plot_boxplot((), {
		"data":data, 
		"name":label, 
		"fill":dict(Brush(kwargs)), 
		"line":dict(Pen(kwargs))})





#-----------------------------------------------------------------------------------

def hist(
		data:_Iterable, 
		density = False, #frequency 
		cumulative = False, 
		breaks:int|_Iterable = None, 
		**kwargs):
	"""
	Plots histogram

	`data:`	Numeric data
	`density:` density histogram if true otherwise frequency.
	`cumulative:` True, cumulative distribution 
	`breaks:` Number of breaks or the break points, int/iterable

	## Note
	If density=True and cumulative=True, then the histogram is 
	normalized so that the cumulative end-value is 1.0
	"""
	assert isinstance(density, bool), "'density' must be bool."
	assert isinstance(cumulative, bool), "'cumulative' must be bool."

	if breaks != None:
		assert isinstance(breaks, int) or isinstance(breaks, _Iterable), "'breaks' must be int/Iterable."
		if isinstance(breaks, int):
			assert breaks>0, "'breaks' if integer, must be >0."
		else:
			Nums = [i for i in breaks if isinstance(i, int) or isinstance(i, float)]
			assert len(Nums)>0, "'breaks' (iterable) do not contain any number."

	return _pydll.c_plot_histogram((), {
			"data":data, 
			"mode":"f" if not density else "d", 
			"cumulative":cumulative , 
			"breaks":breaks, 
			"fill":dict(Brush(kwargs)), 
			"line":dict(Pen(kwargs))})





#-----------------------------------------------------------------------------------


def psychrometry(
		Tdb:_Iterable=None, 
		RH:_Iterable=None, 
		P:numbers.Real=101325.0):
	"""
	Plots psychromety chart.

	`Tdb:` [min, max], minimum and maximum dry-bulb temperatures (Celcius) 
	`RH:` A list in increasing order containing the requested relative humidity (%) lines 
	`P:` Absolute pressure (Pa)
	"""
	return _pydll.c_plot_psychrometry((),{'Tdb':Tdb, 'RH':RH, 'P':P})




#-----------------------------------------------------------------------------------

def scatter(
		x:_Iterable,
		y:_Iterable,  
		label:str = None, 
		smooth:bool = False, 
		marker:str|Marker = None,
		**kwargs):
	"""
	Plot scatter charts

	`x, y:`	x- and y-data 
	`label:` Label of the series 
	`smooth:` Uses smoothing algorith to smooth lines (instead of broken)
	`marker:` Marker class to specify marker properties

	## Note:
	- To plot lines set `lw` to an int > 0.
	- If marker is None and lw is not set, by default markers will be shown.
	- Customize line with (lw, ls and edgecolor properties)
	- Customize marker with (line properties +  facecolor, hatch)
	"""
	assert isinstance(x, _Iterable), "x must be iterable object."
	assert isinstance(y, _Iterable), "y must be iterable object."
	assert len(x) == len(y), "x and y must have same lengths."

	assert isinstance(smooth, bool), "'smooth' must be bool."

	if label != None:
		assert isinstance(label, str), "'label' must be string."
	
	_mark = marker
	assert isinstance(_mark, str|Marker|None), "marker must be str|Marker."
	if isinstance(_mark, str):
		_mark = None if \
						(_mark.isspace() or len(_mark)==0) else \
						Marker(style=marker, size=kwargs.get("markersize") or 5)

	return _pydll.c_plot_scatter((), 
	{
		"x":x, 
		"y":y , 
		"name":label, 
		"smooth":smooth, 
		"marker": dict(_mark) if _mark!=None else None, 
		"line":dict(Pen(kwargs)) if (kwargs.get("lw") != None or kwargs.get("linewidth") != None) else None
	})




def canvas(
		x:_Iterable|None, 
		y:_Iterable|None,
		haxis = True,
		vaxis = True,
		hgrid = True,
		vgrid = True,
		scale = False):
	"""
	Shows a canvas (an empty chart with axes and gridlines)

	`x:` horizontal axis bounds 
	`y:` vertical axis bounds
	`haxis, vaxis:` Show horizontal and vertical axes
	`hgrid, vgrid:` Show horizontal and vertical gridlines
	`scale:` Should the chart automatically scale its limits
	"""

	assert isinstance(x, _Iterable|None), "x must be Iterable|None."
	assert isinstance(y, _Iterable|None), "y must be Iterable|None."
	assert isinstance(scale, bool), "scale must be bool."

	if scale == False:
		assert isinstance(x, _Iterable), "x must be Iterable."
		assert len(x) ==2, "x must contain exactly two numbers."
		assert isinstance(x[0], numbers.Real), "xmin must be a real number."
		assert isinstance(x[1], numbers.Real), "xmax must be a real number."

		assert isinstance(y, _Iterable), "y must be Iterable."
		assert len(y) ==2, "y must contain exactly two numbers."
		assert isinstance(y[0], numbers.Real), "ymin must be a real number."
		assert isinstance(y[1], numbers.Real), "ymax must be a real number."
	
	assert isinstance(haxis, bool), "haxis must be bool."
	assert isinstance(vaxis, bool), "vaxis must be bool."
	assert isinstance(hgrid, bool), "hgrid must be bool."
	assert isinstance(vgrid, bool), "vgrid must be bool."

	return _pydll.c_plot_canvas(
					_ct.py_object(x), 
					_ct.py_object(y),
					haxis, vaxis,
					hgrid, vgrid,
					scale)




"""-----------------------------------------------------------------------------------
-----------------------------------------------------------------------------------"""

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
	"""Start a new plot window"""
	_pydll.c_plot_figure()



def title(label:str):
	"""Create chart title"""
	assert isinstance(label, str), "label must be of type string."
	_pydll.c_plot_title(_ct.c_char_p(label.encode()))



def xlabel(label:str):
	"""Create x-axis label"""
	assert isinstance(label, str), "label must be of type string."
	_pydll.c_plot_xlabel(_ct.c_char_p(label.encode()))



def ylabel(label:str):
	"""Create y-axis label"""
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



def show(shared = False)->None:
	"""
	Starts main loop and shows the chart(s) \n
	`shared:` if there is any other application using a main loop
	"""
	_pydll.c_plot_show()
	_app.mainloop(shared)