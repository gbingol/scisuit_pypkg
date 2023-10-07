import ctypes as _ct
import numpy as _np
import dataclasses as _dc

from typing import Iterable

from ._ctypeslib import pltDLL
from .app import App

from .gdi import Color, Brush, Pen



"""       DEFINITIONS            """


"""
Starts an application
From C++ side c_plot_app function starts an application only once. 
So it is safe to call this many times. 
"""
app = App()



#BAR Charts and Line Charts
CLUSTER = "c"
STACKED = "s"
PERCENTSTK = "%"

#Histogram Modes
HIST_DENSITY = "d"
HIST_FREQUENCY = "f"
HIST_RELFREQUENCY = "r"


#Marker Types
MARKER_CIRCLE = "c"
MARKER_TRIANGLE = "t"
MARKER_SQUARE = "s"
MARKER_XMARKER = "x"




"""            CHARTS                             """

def bar(
	height:Iterable, 
	labels:list[str]=None, 
	style:str = CLUSTER,
	fill=None, 
	line=None):
	"""
	Plots bar chart

	## Input
	height: Numeric data \n
	labels: Category labels \n
	style: CLUSTER, STACKED or PERCENTSTK
	"""
	return pltDLL.c_plot_bar((),
			{"height":height, "labels":labels, "style":style, "fill":fill, "line":line})




def barh(
	width:Iterable, 
	labels:list[str]=None, 
	style:str=CLUSTER,
	fill=None, 
	line=None):
	"""
	Plots horizontal bar chart

	## Input
	width : Numeric data \n
	labels : Category labels \n
	style: CLUSTER, STACKED or PERCENTSTK
	"""
	return pltDLL.c_plot_barh((),
			{"width":width, "labels":labels, "style":style, "fill":fill, "line":line})





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
	return pltDLL.c_plot_boxplot((),
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
	return pltDLL.c_plot_histogram((),
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
	return pltDLL.c_plot_line((),
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
	return pltDLL.c_plot_pie((),
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
	return pltDLL.c_plot_psychrometry((),{'Tdb':Tdb, 'RH':RH, 'P':P})




#-----------------------------------------------------------------------------------


def qqnorm(
		data:Iterable, 
		label:str=None, 
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
		return pltDLL.c_plot_qqnorm((),
			{"data":data, "name": label, "show":show, "line":line, "marker":marker} )





def qqplot(
		x:Iterable,
		y:Iterable,
		marker=None):
	"""
	Plots quantile-quantile chart using two data-sets (x,y)

	## Input
	x, y: Data
	"""
	return pltDLL.c_plot_qqplot((),
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
	return pltDLL.c_plot_quiver((),
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
class MarkerProp:
	"""
	A class to define marker properties

	## Input:
	type: "c", "s", "t", "x" (default "c") \n	
	size: 5 #>0 expected \n
	fill: if specified, RGB "255 255 0" \n
	linewidth: >0 expected \n
	linecolor: if specified, RGB "255 255 0"
	"""
	type:str=MARKER_CIRCLE 
	size:int=5 
	fill:str=None
	linewidth:int = 1
	linecolor:str = None


@_dc.dataclass
class LineProp:
	"""
	A class to define marker properties

	## Input:
	color: if specified, RGB "255 255 0" \n
	width: >0 expected \n
	style: Pen style
	"""
	color:str=None
	width:int = 1
	style:str = Pen.Style.SOLID


@_dc.dataclass
class TrendlineProp:
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
		marker=MarkerProp(), 
		line:dict=None, 
		trendline:TrendlineProp=None):
	"""
	Plot scatter charts

	## Input:
	x, y:	x- and y-data \n
	label: Name of the series \n
	smooth: Smooth lines \n

	Bubble Properties \n
	size:	size data (list), color: color (str), \n
	mode: "A" area "W" diameter, scale: size scale (0, 200]
	"""
	assert isinstance(x, Iterable), "x must be iterable object"
	assert isinstance(y, Iterable), "y must be iterable object"
	assert len(x) == len(y), "x and y must have same lengths"

	if isinstance(trendline, TrendlineProp):
		trendline=vars(trendline)

	return pltDLL.c_plot_scatter((), 
		{"x":x, "y":y , "name":label, "smooth":smooth, 
		"bubble":bubble, 
		"marker":vars(marker) if marker!=None else None, 
		"line":line, 
		"trendline":trendline})


def plot(
	x:Iterable,
	y:Iterable,  
	label:str=None, 
	color:str = None,
	width:int = 1,
	style:int = Pen.Style.SOLID,
	smooth:bool=False):
	"""
	Plot scatter charts

	## Input:
	x, y:	x- and y-data \n
	label: Name of the series \n
	smooth: Smooth lines \n
	color: line color, check Color class \n
	style: line style, use PEN_XXX \n
	width: line width
	"""
	line = LineProp(color=color, width=width, style=style)
	return scatter(x=x, y=y, label=label, smooth=smooth, marker=None, line=vars(line))


#----------------------------------------------------------------------------

def figure():
	"""Start a new plot window"""
	pltDLL.c_plot_figure()


def title(label:str):
	"""Create chart title"""
	assert isinstance(label, str), "label must be of type string."
	pltDLL.c_plot_title(label)


def xlabel(label:str):
	"""Create x-axis label"""
	assert isinstance(label, str), "label must be of type string."
	pltDLL.c_plot_xlabel(label)


def ylabel(label:str):
	"""Create y-axis label"""
	assert isinstance(label, str), "label must be of type string."
	pltDLL.c_plot_ylabel(label)


def legend():
	"""Create legend"""
	pltDLL.c_plot_legend()


def show(maximize = False, shared = False):
	"""
	Starts main loop and shows the chart(s)
	
	## Input:
	maximize: Whether to show chart as maximized (good for Psychrometric chart) \n
	shared: if there is any other application using a main loop
	"""
	pltDLL.c_plot_show(_ct.c_bool(maximize), _ct.c_bool(shared))
	app.mainloop()
	