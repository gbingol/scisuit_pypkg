import ctypes as _ct
import numpy as _np
import dataclasses as _dc

from typing import Iterable
from enum import Enum

from .util import parent_path as _parent_path


#TODO: Change to release version
_path = _parent_path(__file__) / "scisuit_plotter_d"
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

pltdll.c_plot_figure.argtypes = []
pltdll.c_plot_figure.restype=None

pltdll.c_plot_title.argtypes = [_ct.py_object]
pltdll.c_plot_title.restype=None

pltdll.c_plot_xlabel.argtypes = [_ct.py_object]
pltdll.c_plot_xlabel.restype=None

pltdll.c_plot_ylabel.argtypes = [_ct.py_object]
pltdll.c_plot_ylabel.restype=None

pltdll.c_plot_legend.argtypes = []
pltdll.c_plot_legend.restype=None

pltdll.c_plot_show.argtypes = [_ct.c_bool, _ct.c_bool]
pltdll.c_plot_show.restype=None



"""       DEFINITIONS            """
class StrEnum(str, Enum):
	pass


#BAR Charts and Line Charts
CLUSTER = "c"
STACKED = "s"
PERCENTSTK = "%"

#Histogram Modes
HIST_DENSITY = "d"
HIST_FREQUENCY = "f"
HIST_RELFREQUENCY = "r"

#Pen Styles
PEN_SOLID = 100
PEN_DOT = 101
PEN_LONGDASH = 102
PEN_SHORTDASH = 103
PEN_DOTDASH = 104
PEN_TRANSPARENT = 106


#Brush/Fill Styles
BRUSH_SOLID = 100, 
BRUSH_TRANSPARENT = 106, 
BRUSH_BDIAGHATCH = 111, 
BRUSH_CROSSDIAGHATCH = 112
BRUSH_FDIAGHATCH = 113
BRUSH_CROSSHATCH = 114
BRUSH_HORIZHATCH =115
BRUSH_VERTHATCH = 116


#Marker Types
MARKER_CIRCLE = "c"
MARKER_TRIANGLE = "t"
MARKER_SQUARE = "s"
MARKER_XMARKER = "x"



class Color(StrEnum):
	"""
	Colors with corresponding RGB values
	"""
	AQUA="0 255 255"
	BLUE="0 0 255"
	BLUE_MEDIUM="0 0 205"
	BLUE_ROYAL="65 105 225"
	BLUE_MIDNIGHT="25 25 112"
	BROWN="165 42 42"
	BROWN_SADDLE="139 69 19"
	CHOCOLATE="210 105 30" 
	CRIMSON="220 20 60"
	FUCHSIA="255 0 255"
	GRAY="128 128 128"
	WHITE="255 255 255"
	RED="255 0 0"
	RED_DARK="139 0 0"
	LIME="0 255 0"
	YELLOW="255 255 0"
	SILVER="192 192 192"
	MAROON="128 0 0"
	OLIVE="128 128 0"
	GREEN="0 128 0"
	PURPLE="128 0 128"
	TEAL="0 128 128"
	NAVY="0 0 128" 
	SALMON_DARK="233 150 122"
	SALMON="250 128 114" 
	SALMON_LIGHT="255 160 122"
	ORANGE_RED="255 69 0"
	ORANGE_DARK="255 140 0"
	ORANGE="255 165 0"
	TAN="210 180 140"
	WHEAT="245 222 179"
	ORCHID="218 112 214"
	INDIGO="75 0 130"








"""            CHARTS                             """

def bar(
	height:Iterable, 
	labels=None, 
	label=None, 
	type = CLUSTER,
	fill=None, 
	line=None):
	"""
	Plots bar chart

	## Input
	height: Numeric data \n
	labels: Category labels \n
	label: Name of the series \n
	type: clustered, stacked and 100% stacked
	"""
	return pltdll.c_plot_bar((),
			{"height":height, "labels":labels, "name":label, "type":type, 
    			"fill":fill, "line":line})




def barh(
	width:Iterable, 
	labels=None, 
	label=None, 
	type=CLUSTER, 
	fill=None, 
	line=None):
	"""
	Plots horizontal bar chart

	## Input
	width : Numeric data \n
	labels : Category labels \n
	label: Name of the series \n
	type: clustered, stacked and 100% stacked.
	"""
	return pltdll.c_plot_barh((),
			{"width":width, "labels":labels, "name":label, "type":type, 
    			"fill":fill, "line":line})





#-----------------------------------------------------------------------------------

def boxplot(
	data:Iterable, 
	label:str=None, 
	fill:dict=None, 
	line:dict=None):
	"""
	Plots box-whisker chart and returns a window handle.

	## Input
	data : Data to be plotted \n
	label: Name of the series
	"""
	return pltdll.c_plot_boxplot((),
			{"data":data, "name":label, "fill":fill, "line":line})





#-----------------------------------------------------------------------------------

def histogram(
		data:Iterable, 
		mode:str=HIST_FREQUENCY, 
		cumulative=False, 
		breaks = None, 
		fill = None, 
		line = None):
	"""
	Plots histogram

	## Input
	data:	A variable \n
	mode : density, frequency and relative frequency.\n
	cumulative : True, cumulative distribution \n
	breaks : Number of breaks or the break points, int/iterable
	"""
	return pltdll.c_plot_histogram((),
			    {"data":data, "mode":mode, "cumulative":cumulative, 
				"breaks":breaks, "fill":fill, "line":line})





#-----------------------------------------------------------------------------------

def line(
	y:Iterable, 
	labels:list=None, 
	label:str=None, 
	type=CLUSTER, 
	marker=None, 
	line=None):
	"""
	Plots line chart

	## Input:
	y : Numeric data \n
	labels : Category labels \n
	label: Name of the series \n
	type:	clustered, stacked and 100% stacked 
	"""
	return pltdll.c_plot_line((),
			 {"y":y, "labels":labels, "name":label, "type":type, "marker":marker, "line":line})





#-----------------------------------------------------------------------------------


def pie(
	data:Iterable, 
	labels:list=None, 
	colors:list=None, 
	explode:list|int=None, 
	startangle:int=None):
	"""
	Plots Pie chart

	## Input:
	data : Data of individual slices \n
	labels: Label of individual slices \n
	colors: Color of individual slices \n
	explode: Explosion level \n
	startangle:	Start angle of first slice 
	"""
	return pltdll.c_plot_pie((),
				{"data":data, "labels":labels, "colors":colors, 
     				"explode":explode, "startangle":startangle})





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
		show=True, 
		line=None, 
		marker=None):
		"""
		Normal Quantile-quantile chart \n
		x-axis="Theoretical Quantiles" \n  
		y-axis="Sample Quantiles" \n

		## Input:
		data: Data \n
		show: Whether to show theoretical line or not 
		"""
		return pltdll.c_plot_qqnorm((),
			{"data":data, "show":show, "line":line, "marker":marker} )





def qqplot(
		x:Iterable,
		y:Iterable,
		marker=None):
	"""
	Plots quantile-quantile chart using two data-sets (x,y)

	## Input
	x, y: Data
	"""
	return pltdll.c_plot_qqplot((),
			{"x":x, "y":y, "marker":marker})





#-----------------------------------------------------------------------------------


def quiver(
		x:_np.ndarray, 
		y:_np.ndarray, 
		u:_np.ndarray, 
		v:_np.ndarray, 
		scale=False):
	""""
	Plots quiver chart

	## Input:
	x, y: (x,y) location, 2D ndarray \n
	u, v: length in x and y directions, 2D ndarray \n
	scale: Whether to scale the length of the arrows
	"""
	return pltdll.c_plot_quiver((),
			{
				"x":x.flatten().tolist(), 
				"y":y.flatten().tolist(),
				"u":u.flatten().tolist(), 
				"v":v.flatten().tolist(), 
				"scale":scale})



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
	type:str=MARKER_CIRCLE 
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
		{"x":x, "y":y , "name":label, "smooth":smooth, 
		"bubble":bubble, "marker":vars(marker), "line":line, "trendline":trendline})





#----------------------------------------------------------------------------

def figure():
	"""Start a new plot window"""
	pltdll.c_plot_figure()


def title(label:str):
	"""Create chart title"""
	assert isinstance(label, str), "label must be of type string."
	pltdll.c_plot_title(label)


def xlabel(label:str):
	"""Create x-axis label"""
	assert isinstance(label, str), "label must be of type string."
	pltdll.c_plot_xlabel(label)


def ylabel(label:str):
	"""Create y-axis label"""
	assert isinstance(label, str), "label must be of type string."
	pltdll.c_plot_ylabel(label)


def legend():
	"""Create legend"""
	pltdll.c_plot_legend()


def show(maximize = False, shared = False, dpiaware = True):
	"""
	Starts main loop and shows the chart
	
	## Input:
	maximize: Whether to show chart as maximized (good for Psychrometric chart) \n
	shared: if there is any other application using a main loop \n
	dpiaware: Show chart dpi aware
	"""
	_ct.windll.shcore.SetProcessDpiAwareness(dpiaware)
	pltdll.c_plot_show(_ct.c_bool(maximize), _ct.c_bool(shared))
	