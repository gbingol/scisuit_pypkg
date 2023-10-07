import ctypes as _ct
from typing import Iterable as _Iterable

from .._ctypeslib import pltDLL as _pltDLL

import scisuit.plot.defs as _defs
import scisuit.plot.gdi as _gdi






def bar(
	height:_Iterable, 
	labels:list[str]=None, 
	style:str = _defs.CLUSTER,
	fill:_gdi.Brush=None, 
	line:_gdi.Pen=None):
	"""
	Plots bar chart

	## Input
	height: Numeric data \n
	labels: Category labels \n
	style: CLUSTER, STACKED or PERCENTSTK
	"""
	return _pltDLL.c_plot_bar((),	{
			"height":height, 
    			"labels":labels, 
			"style":style, 
			"fill":vars(fill) if fill != None else None, 
			"line":vars(line) if line != None else None})




def barh(
	width:_Iterable, 
	labels:list[str]=None, 
	style:str=_defs.CLUSTER,
	fill:_gdi.Brush=None, 
	line:_gdi.Pen=None):
	"""
	Plots horizontal bar chart

	## Input
	width : Numeric data \n
	labels : Category labels \n
	style: CLUSTER, STACKED or PERCENTSTK
	"""
	return _pltDLL.c_plot_barh((),{
		"width":width, 
		"labels":labels, 
		"style":style, 
		"fill":vars(fill) if fill != None else None, 
		"line":vars(line) if line != None else None})





#-----------------------------------------------------------------------------------

def boxplot(
	data:_Iterable, 
	label:str=None, 
	fill:_gdi.Brush=None, 
	line:_gdi.Pen=None):
	"""
	Plots box-whisker chart.

	## Input
	data : Data to be plotted \n
	label: Name of the series
	"""
	return _pltDLL.c_plot_boxplot((), {
		"data":data, 
		"name":label, 
		"fill":vars(fill) if fill != None else None, 
		"line":vars(line) if line != None else None})





#-----------------------------------------------------------------------------------

def histogram(
		data:_Iterable, 
		mode:str=_defs.HIST_FREQUENCY, 
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
	return _pltDLL.c_plot_histogram((),
			    {"data":data, "mode":mode, "cumulative":cumulative, 
				"breaks":breaks, "fill":fill, "line":line})





#-----------------------------------------------------------------------------------

def line(
	y:_Iterable, 
	labels:list=None, 
	label:str=None, 
	type=_defs.CLUSTER, 
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
	return _pltDLL.c_plot_line((),
			 {"y":y, "labels":labels, "name":label, "type":type, "marker":marker, "line":line})





#-----------------------------------------------------------------------------------


def pie(
	data:_Iterable, 
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
	return _pltDLL.c_plot_pie((),
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
	return _pltDLL.c_plot_psychrometry((),{'Tdb':Tdb, 'RH':RH, 'P':P})




#-----------------------------------------------------------------------------------


def qqnorm(
		data:_Iterable, 
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
		return _pltDLL.c_plot_qqnorm((),
			{"data":data, "name": label, "show":show, "line":line, "marker":marker} )





def qqplot(
		x:_Iterable,
		y:_Iterable,
		marker=None):
	"""
	Plots quantile-quantile chart using two data-sets (x,y)

	## Input
	x, y: Data
	"""
	return _pltDLL.c_plot_qqplot((),
			{"x":x, "y":y, "marker":marker})





#-----------------------------------------------------------------------------------

import numpy as _np

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
	return _pltDLL.c_plot_quiver((),
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



def scatter(
		x:_Iterable,
		y:_Iterable,  
		label:str=None, 
		smooth:bool=False, 
		bubble:dict=None, 
		marker=_defs.Marker(), 
		line:dict=None, 
		trendline:_defs.Trendline=None):
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
	assert isinstance(x, _Iterable), "x must be iterable object"
	assert isinstance(y, _Iterable), "y must be iterable object"
	assert len(x) == len(y), "x and y must have same lengths"

	if isinstance(trendline, _defs.Trendline):
		trendline=vars(trendline)

	return _pltDLL.c_plot_scatter((), 
		{"x":x, "y":y , "name":label, "smooth":smooth, 
		"bubble":bubble, 
		"marker":vars(marker) if marker!=None else None, 
		"line":line, 
		"trendline":trendline})


def plot(
	x:_Iterable,
	y:_Iterable,  
	label:str=None, 
	color:str = None,
	width:int = 1,
	style:int = _gdi.Pen.STYLE.SOLID,
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
	line_ = _defs.Pen(color=color, width=width, style=style)
	return scatter(
		x=x, 
		y=y, 
		label=label, 
		smooth=smooth, 
		marker=None, 
		line={"color": line_.color, "width":line_.width, "style":line_.style})

	