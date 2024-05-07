import ctypes as _ct
import numbers
from typing import Iterable as _Iterable

from .._ctypeslib import pydll as _pydll

from ._chartelems import Marker
from ._gdiobj import Brush, Pen









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
		binmethod:str = "freedmandiaconis",
		breaks:int|_Iterable = None, 
		**kwargs):
	"""
	Plots histogram

	`data:`	Numeric data
	`density:` density histogram if true otherwise frequency.
	`cumulative:` True, cumulative distribution 
	`binmethod:` freedmandiaconis, rice, sqrt, sturges or scott
	`breaks:` Number of breaks or the break points, int/iterable

	## Note
	- If density=True and cumulative=True, then the histogram is 
	  normalized so that the cumulative end-value is 1.0
	
	- If breaks is specified, then binmethod is not taken into account
	"""
	assert isinstance(density, bool), "'density' must be bool."
	assert isinstance(cumulative, bool), "'cumulative' must be bool."

	assert isinstance(binmethod, str), "binmethod must be str"

	_binmethods = ["freedmandiaconis", "rice", "sqrt", "sturges", "scott"]
	if not binmethod in _binmethods:
		raise ValueError("binmethods: " + str(_binmethods))

	if isinstance(breaks, _Iterable):
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
			"binmethod": binmethod, 
			"breaks":list(breaks) if isinstance(breaks, _Iterable) else breaks, 
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

