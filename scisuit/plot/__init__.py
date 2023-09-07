import ctypes as _ct
import numpy as _np
import dataclasses as _dc

from typing import Iterable


from ..util import parent_path as _parent_path
from .enums import Bar_Type, Line_Type, Histogram_Mode


#TODO: Change to release version
_path = _parent_path(__file__, level=1) / "scisuit_plotter_d"
pltdll = _ct.PyDLL(str(_path))


pltdll.c_plot_bar.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_bar.restype=_ct.py_object

pltdll.c_plot_barh.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_barh.restype=_ct.py_object

pltdll.c_plot_boxplot.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_boxplot.restype=_ct.py_object

pltdll.c_plot_histogram.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_histogram.restype=_ct.py_object

pltdll.c_plot_line.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_line.restype=_ct.py_object

pltdll.c_plot_pie.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_pie.restype=_ct.py_object

pltdll.c_plot_psychrometry.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_psychrometry.restype=_ct.py_object

pltdll.c_plot_qqnorm.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_qqnorm.restype=_ct.py_object

pltdll.c_plot_qqplot.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_qqplot.restype=_ct.py_object

pltdll.c_plot_quiver.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_quiver.restype=_ct.py_object

pltdll.c_plot_scatter.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_scatter.restype=_ct.py_object





#-----------------------------------------------------------------------------------

def bar(
	height:Iterable, 
	labels=None, 
	label=None, 
	title=None, 
	type = Bar_Type.CLUSTER,
	fill=None, 
	line=None, 
	hwnd=None):
	"""
	Plots bar chart

	## Input
	height: Numeric data \n
	labels: Category labels \n
	label: Name of the series \n
	type: clustered, stacked and 100% stacked \n
	title: Title of the chart
	"""
	return pltdll.c_plot_bar((),
			{"height":height, "labels":labels, "name":label, "title":title, "type":type, 
    			"fill":fill, "line":line, "hwnd":hwnd})




def barh(
	width:Iterable, 
	labels=None, 
	label=None, 
	title=None, 
	type=Bar_Type.CLUSTER, 
	fill=None, 
	line=None, 
	hwnd=None):
	"""
	Plots horizontal bar chart

	## Input
	width : Numeric data \n
	labels : Category labels \n
	label: Name of the series \n
	type: clustered, stacked and 100% stacked.\n
	title: Title of the chart
	"""
	return pltdll.c_plot_barh((),
			{"width":width, "labels":labels, "name":label, "title":title, "type":type, 
    			"fill":fill, "line":line, "hwnd":hwnd})





#-----------------------------------------------------------------------------------

def boxplot(
	data:Iterable, 
	label:str=None, 
	title:str=None, 
	fill:dict=None, 
	line:dict=None, 
	hwnd=None):
	"""
	Plots box-whisker chart and returns a window handle.

	## Input
	data : Data to be plotted \n
	label: Name of the series \n
	title: Title of the chart 
	"""
	return pltdll.c_plot_boxplot((),
			{"data":data, "name":label, "title":title, "fill":fill, "line":line, "hwnd":hwnd})





#-----------------------------------------------------------------------------------

def histogram(
		data:Iterable, 
		mode:str=Histogram_Mode.FREQUENCY, 
		cumulative=False, 
		breaks = None, 
		title = None,
		fill = None, 
		line = None, 
		hwnd=None):
	"""
	Plots histogram

	## Input
	data:	A variable \n
	mode : density, frequency and relative frequency.\n
	cumulative : True, cumulative distribution \n
	breaks : Number of breaks or the break points, int/ndarray/list\n
	title: Title of the chart
	"""
	return pltdll.c_plot_histogram((),
			    {"data":data, "mode":mode, "cumulative":cumulative, 
				"breaks":breaks, "title":title, "fill":fill, "line":line, "hwnd":hwnd})





#-----------------------------------------------------------------------------------

def line(
	y:Iterable, 
	labels:list=None, 
	label:str=None, 
	title:str=None, 
	type=Line_Type.CLUSTER, 
	marker=None, 
	line=None, 
	hwnd=None):
	"""
	Plots line chart

	## Input:
	y : Numeric data \n
	labels : Category labels \n
	label: Name of the series \n
	type:	clustered, stacked and 100% stacked \n
	title: Title of the chart
	"""
	return pltdll.c_plot_line((),
			 {"y":y, "labels":labels, "name":label, "title":title, 
     			"type":type, "marker":marker, "line":line, "hwnd":hwnd})







#-----------------------------------------------------------------------------------


def pie(
	data:Iterable, 
	title:str=None, 
	labels:list=None, 
	colors:list=None, 
	explode:list|int=None, 
	startangle:int=None, 
	legend=True, 
	hwnd=None):
	"""
	Plots Pie chart

	## Input:
	data : Data of individual slices \n
	title: Title of the chart \n
	labels: Label of individual slices \n
	colors: Color of individual slices \n
	explode: Explosion level \n
	startangle:	Start angle of first slice \n
	legend: Whether to show legend or not
	"""
	return pltdll.c_plot_pie((),
				{"data":data, "title":title, "labels":labels, "colors":colors, 
     				"explode":explode, "startangle":startangle, "legend":legend, "hwnd":hwnd})





#-----------------------------------------------------------------------------------


def psychrometry(Tdb:list=None, RH:list=None, P=101325):
	"""
	Plots psychromety chart.

	## Input
	Tdb: [min, max], minimum and maximum dry-bulb temperatures (Celcius) \n
	RH: A list in increasing order containing the requested relative humidity (%) lines \n
	P: Absolute pressure (Pa)
	"""
	return pltdll.c_plot_psychrometry((),{'Tdb':Tdb, 'RH':RH, 'P':P})




#-----------------------------------------------------------------------------------


def qqnorm(
		data:Iterable,  
		title = "Normal Q-Q Plot", 
		xlab="Theoretical Quantiles",  
		ylab="Sample Quantiles", 
		show=True, 
		line=None, 
		marker=None, 
		hwnd=None):
		"""
		Quantile-quantile chart

		## Input:
		data: Data \n
		title: Title of the chart \n
		xlab: Label of x-axis \n
		ylab: Label of y-axis \n
		show: Whether to show theoretical line or not 
		"""
		return pltdll.c_plot_qqnorm((),
			{"data":data, "title":title, "xlab":xlab, "ylab":ylab, 
			"show":show, "line":line, "marker":marker, "hwnd":hwnd} )





def qqplot(
		x:Iterable,
		y:Iterable,
		title:str = None, 
		xlab:str=None, 
		ylab:str=None, 
		marker=None, 
		hwnd=None):
	"""
	Plots quantile-quantile chart using two data-sets (x,y)

	## Input
	x, y: Data \n
	title: title of the chart \n
	xlab: Label of x-axis \n
	ylab: Label of y-axis
	"""
	return pltdll.c_plot_qqplot((),
			{"x":x, "y":y, "title":title, 
			"xlab":xlab, "ylab":ylab, "marker":marker, "hwnd":hwnd})







#-----------------------------------------------------------------------------------


def quiver(
		x:_np.ndarray, 
		y:_np.ndarray, 
		u:_np.ndarray, 
		v:_np.ndarray, 
		scale=False, 
		title:str = None, 
		xlab:str = None, 
		ylab:str = None):
	""""
	Plots quiver chart

	## Input:
	x, y: (x,y) location, 2D ndarray \n
	u, v: length in x and y directions, 2D ndarray \n
	scale: Whether to scale the length of the arrows \n
	title: Title of the chart \n
	xlab: Label of x-axis \n
	ylab: Label of y-axis
	"""
	return pltdll.c_plot_quiver((),
			{
				"x":x.flatten().tolist(), 
				"y":y.flatten().tolist(),
				"u":u.flatten().tolist(), 
				"v":v.flatten().tolist(), 
				"scale":scale, "title":title, "xlab":xlab, "ylab":ylab})



def dirfield(x:_np.ndarray, y:_np.ndarray, slope:_np.ndarray):
	"""
	Plots the direction field for a given function f=dy/dx \n

	## Input
	x, y: 2D numpy array (after using meshgrid) \n
	slope: 2D array resulting from evaluation of f=dy/dx, first order ODE
	"""

	# angle of inclination
	t = _np.arctan(slope)

	# xy-components of arrow
	dx = _np.cos(t)
	dy = _np.sin(t); 

	#call quiver to visualize   
	quiver(x, y, dx, dy)




#-----------------------------------------------------------------------------------


@_dc.dataclass
class Marker:
	"""
	A class to define marker properties

	## Input:
	type: "c", "s", "t", "x" (default "c") \n	
	size: 5 #>0 expected \n
	fill: if specified, RGB "255 255 0" \n
	linewidth: #>0 expected \n
	linecolor: if specified, RGB "255 255 0"
	"""
	type:str="c" 
	size:int=5 
	fill:str=None
	linewidth:int = 1
	linecolor:str = None


@_dc.dataclass
class Trendline:
	"""
	A class to define Trendline properties

	## Input:
	type: "linear", "poly", "exp", "log","pow" \n
	degree: 2, >=2 expected when type is polynomial \n
	intercept: number expected \n
	color: "R G B" format, "255 255 125" \n
	width: >0 expected \n
	style: 100, 101, 102, 103, 104, 106 (default 102)
	"""
	type:str="linear"
	degree:int=2
	intercept:float=None
	color:str = None
	width:int = 1
	style:int = 102



def scatter(
		x:Iterable,
		y:Iterable,  
		label:str=None, 
		title:str=None, 
		xlab:str=None, 
		ylab:str=None, 
		smooth:bool=False, 
		bubble:dict=None, 
		marker=Marker(), 
		line:dict=None, 
		trendline:Trendline=None):
	"""
	Plot scatter charts

	## Input:
	x, y:	x- and y-data \n
	label: Name of the series \n
	title: Title of the chart \n
	xlab:	Label of x-axis \n
	ylab:	Label of y-axis \n
	smooth: Spline algorithm is applied to smooth the line \n

	Bubble Properties \n
	size:	size data (list), color: color (str), \n
	mode: "A" area "W" diameter, scale: size scale (0, 200]
	"""
	assert isinstance(x, Iterable), "x must be iterable object"
	assert isinstance(y, Iterable), "y must be iterable object"
	assert len(x) == len(y), "x and y must have same lengths"

	if isinstance(trendline, Trendline):
		trendline=vars(trendline)

	return pltdll.c_plot_scatter((), 
		{"x":x, "y":y , "name":label, "title":title, "xlab":xlab, "ylab":ylab, "smooth":smooth, 
		"bubble":bubble, "marker":vars(marker), "line":line, "trendline":trendline})
