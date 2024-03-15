import ctypes as _ct
import numbers
from typing import Iterable as _Iterable

from .._ctypeslib import pydll as _pydll
from .gdiobj import Pen, Brush
from .chartelems import Marker

from ..app import App as _App


_app = _App()





def bar(
	height:_Iterable, 
	labels:_Iterable, 
	stacked = False, 
	**kwargs):
	"""
	Plots bar chart

	## Input
	height: Numeric data \n
	labels: Category labels \n
	stacked: if True stacked bar chart, otherwise clustered
	"""
	
	assert isinstance(height, _Iterable), "'height' must be iterable"
	assert isinstance(labels, _Iterable), "'labels' must be iterable"

	assert isinstance(stacked, bool), "'stacked' must be bool" 
	assert len(labels)>=2, "at least 2 labels expected"
	assert len(labels) == len(height), "len(labels) == len(height) expected"
	
	return _pydll.c_plot_bar((), {
			"height":height, 
			"labels":labels, 
			"style": "c" if not stacked else "s", 
			"fill":dict(Brush(kwargs)), 
			"line":dict(Pen(kwargs))})


#-----------------------------------------------------------------------------------


def barh(
	width:_Iterable, 
	labels:_Iterable, 
	stacked = False,
	**kwargs):
	"""
	Plots horizontal bar chart

	## Input
	width : Numeric data \n
	labels : Category labels \n
	stacked: if True stacked chart, otherwise clustered
	"""
	
	assert isinstance(width, _Iterable), "'width' must be iterable"
	assert isinstance(labels, _Iterable), "'labels' must be iterable"

	assert isinstance(stacked, bool), "'stacked' must be bool" 
	assert len(labels)>=2, "at least 2 labels expected"
	assert len(labels) == len(width), "len(labels) == len(width) expected"
	
	return _pydll.c_plot_barh((),{
		"width":width, 
		"labels":labels, 
		"style":"c" if not stacked else "s",  
		"fill":dict(Brush(kwargs)), 
		"line":dict(Pen(kwargs))})





#-----------------------------------------------------------------------------------

def boxplot(
	data:_Iterable, 
	label:str = None, 
	**kwargs):
	"""
	Plots box-whisker chart.

	## Input
	data : Data to be plotted \n
	label: Name of the series
	"""
	assert isinstance(data, _Iterable), "'data' must be iterable"
	
	if label != None:
		assert isinstance(label, str), "'label' must be string"

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

	## Input
	data:	Numeric data \n
	density : density histogram if true otherwise frequency.\n
	cumulative : True, cumulative distribution  \n
	breaks : Number of breaks or the break points, int/iterable

	## Note
	If density=True and cumulative=True, then the histogram is 
	normalized so that the cumulative end-value is 1.0
	"""
	assert isinstance(density, bool), "'density' must be bool"
	assert isinstance(cumulative, bool), "'cumulative' must be bool"

	if breaks != None:
		assert isinstance(breaks, int) or isinstance(breaks, _Iterable), "'breaks' must be int/Iterable"
		if isinstance(breaks, int):
			assert breaks>0, "'breaks' if integer, must be >0"
		else:
			Nums = [i for i in breaks if isinstance(i, int) or isinstance(i, float)]
			assert len(Nums)>0, "'breaks' (iterable) do not contain any number"

	return _pydll.c_plot_histogram((), {
			"data":data, 
			"mode":"f" if not density else "d", 
			"cumulative":cumulative , 
			"breaks":breaks, 
			"fill":dict(Brush(kwargs)), 
			"line":dict(Pen(kwargs))})





#-----------------------------------------------------------------------------------

def line(
	y:_Iterable, 
	labels:_Iterable, 
	stacked = False,
	label:str = None,  
	marker:Marker=None, 
	**kwargs):
	"""
	Plots line chart

	## Input:
	y : An iterable containing numeric data \n
	labels : Category labels \n
	stacked: if True stacked chart, otherwise clustered \n
	label: Label of the individual series 
	"""
	assert isinstance(y, _Iterable), "'y' must be iterable"
	assert len(y)>=2, "At least 2 data points expected"

	assert isinstance(stacked, bool), "'stacked' must be bool" 
	assert isinstance(labels, _Iterable), "'labels' must be iterable"
	assert len(labels)>=2, "At least 2 labels expected"

	assert len(y) == len(labels), "len(y) == len(labels) expected"
	
	return _pydll.c_plot_line((), {
			"y":y, 
			"labels":labels, 
			"label":label, 
			"style":"c" if not stacked else "s",  
			"marker":dict(marker) if marker != None else None, 
			"line":dict(Pen(kwargs))})





#-----------------------------------------------------------------------------------


def pie(
	data:_Iterable, 
	labels:_Iterable = None, 
	colors:_Iterable = None, 
	explode:_Iterable|int = None, 
	startangle:int = None):
	"""
	Plots Pie chart

	## Input:
	data : Data of individual slices \n
	labels: Label of individual slices \n
	colors: Color of individual slices \n
	explode: Explosion level \n
	startangle:	Start angle of first slice 
	"""
	assert isinstance(data, _Iterable), "'data' must be iterable"
	Nums = [i for i in data if isinstance(i, int) or isinstance(i, float)]
	assert len(Nums)>=2, "'data' (iterable) must contain at least 2 numeric values"

	if labels != None:
		assert isinstance(labels, _Iterable), "'labels' must be iterable"

	if colors != None:
		assert isinstance(colors, _Iterable), "'colors' must be iterable"

	if startangle != None:
		assert isinstance(startangle, int), "'startangle' must be int"
		assert 0 <startangle< 360, "startangle must be in (0, 360)"

	_Explode = None
	if explode != None:
		assert isinstance(explode, _Iterable) or isinstance(explode, int), "'explode' must be iterable/int"
		if isinstance(explode, int):
			assert 0 < explode <=10, "explode must be in (0, 10]"
			_Explode = explode
		else:
			_Explode = [i for i in explode if 0 < i <=10 and isinstance(i, int)]
			assert len(_Explode)>0, "explode must contain"


	return _pydll.c_plot_pie((), {
				"data":data, 
	 			"labels":labels, 
				"colors":colors, 
     			"explode":_Explode, 
				"startangle":startangle})





#-----------------------------------------------------------------------------------


def psychrometry(Tdb:_Iterable=None, RH:_Iterable=None, P:float|int=101325):
	"""
	Plots psychromety chart.

	## Input
	Tdb: [min, max], minimum and maximum dry-bulb temperatures (Celcius) \n
	RH: A list in increasing order containing the requested relative humidity (%) lines \n
	P: Absolute pressure (Pa)
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

	x, y:	x- and y-data 
	label: Label of the series 
	smooth: Uses smoothing algorith to smooth lines (instead of broken)
	marker: Marker class to specify marker properties

	## Note:
	- To plot lines set `lw` to an int > 0.
	- If marker is None and lw is not set, by default markers will be shown.
	- Customize line with (lw, ls and edgecolor properties)
	- Customize marker with (line properties +  facecolor, hatch)
	"""
	assert isinstance(x, _Iterable), "x must be iterable object"
	assert isinstance(y, _Iterable), "y must be iterable object"
	assert len(x) == len(y), "x and y must have same lengths"

	assert isinstance(smooth, bool), "'smooth' must be bool"

	if label != None:
		assert isinstance(label, str), "'label' must be string"
	
	_mark = marker
	assert isinstance(_mark, str|Marker|None), "marker must be str|Marker"
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




def bubble(
		x:_Iterable,
		y:_Iterable,  
		s:_Iterable,
		color:str|tuple|list = None,
		mode:str = "A",
		scale:int=100,
		label:str=None):
	"""
	Plots bubble chart

	## Input:
	x, y, size:	x- and y- and size data \n
	color: color  \n
	mode: "A" area "W" diameter \n
	scale: size scale (0, 200] \n
	label: Name of the series	
	"""
	assert \
		isinstance(x, _Iterable) and \
		isinstance(y, _Iterable) and \
		isinstance(s, _Iterable), "x, y and s must be iterable objects."

	assert len(x) == len(y) and len(y) == len(s), "x, y and s must have same lengths"

	assert isinstance(mode, str), "'mode' must be string"
	assert isinstance(label, str|None), "'label' must be string"
	assert isinstance(color, None|str|tuple|list), "'color' must be str|tuple|list"

	assert isinstance(scale, int), "'scale' must be int"
	assert 0<scale<200, "'scale' must be in range (0, 200)"

	return _pydll.c_plot_bubble((), {
		"x":x, "y":y , "size":s, "color":color,"mode":mode.lower(), "scale":scale, "label":label})




def canvas(
		xmin:numbers.Real, 
		xmax:numbers.Real,
		ymin:numbers.Real, 
		ymax:numbers.Real):
	"""
	Shows a canvas (an empty chart with axes)

	## Input:
	`xmin, xmax:` horizontal axis bounds \n
	`ymin, ymax:` vertical axis bounds
	"""
	assert isinstance(xmin, numbers.Real), "xmin must be a real number"
	assert isinstance(xmax, numbers.Real), "xmax must be a real number"
	assert isinstance(ymin, numbers.Real), "ymin must be a real number"
	assert isinstance(ymax, numbers.Real), "ymax must be a real number"

	return _pydll.c_plot_canvas((), {"x":[xmin, xmax], "y":[ymin, ymax]})




"""
-----------------------------------------------------------------------------------
-----------------------------------------------------------------------------------
"""



def layout(nrows:int, ncols:int)->None:
	"""
	Partitions the current chart window into nrows and ncols \n
	(similar to a matrix with nrows and ncols) \n

	nrows: number of rows
	ncols: number of columns
	"""
	assert isinstance(nrows, int), "nrows must be integer"
	assert isinstance(ncols, int), "ncols must be integer"

	assert 0<nrows<=255, "0<nrows<=255 expected"
	assert 0<ncols<=255, "0<ncols<=255 expected"

	_pydll.c_plot_layout(
		_ct.c_int(nrows), 
		_ct.c_int(ncols))



def subplot(row:int, col:int, nrows:int = 1, ncols:int = 1)->None:
	"""
	Must be called after the window is partitioned (by layout) to select a cell from the partition. \n

	row: row position of the cell (must be less than partition's number of rows),
	col: column position of the cell (must be less than partition's number of columns),
	nrows: number of rows the cell should span 
	ncols: number of columns the cell should span 
	"""
	assert isinstance(row, int), "row must be integer"
	assert isinstance(col, int), "col must be integer"
	assert isinstance(nrows, int), "nrows must be integer"
	assert isinstance(ncols, int), "ncols must be integer"

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
	_pydll.c_plot_title(label)


def xlabel(label:str):
	"""Create x-axis label"""
	assert isinstance(label, str), "label must be of type string."
	_pydll.c_plot_xlabel(label)


def ylabel(label:str):
	"""Create y-axis label"""
	assert isinstance(label, str), "label must be of type string."
	_pydll.c_plot_ylabel(label)


def legend():
	"""Create legend"""
	_pydll.c_plot_legend()


def show(shared = False):
	"""
	Starts main loop and shows the chart(s) \n
	
	shared: if there is any other application using a main loop
	"""
	_pydll.c_plot_show()
	_app.mainloop(shared)