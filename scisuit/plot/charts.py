import ctypes as _ct
from typing import Iterable as _Iterable

from .._ctypeslib import pydll as _pydll

import scisuit.plot.defs as _defs
import scisuit.plot.gdi as _gdi






def bar(
	height:_Iterable, 
	labels:_Iterable = None, 
	style:str = "c", #clustered
	fill:_gdi.Brush=None, 
	line:_gdi.Pen=None):
	"""
	Plots bar chart

	## Input
	height: Numeric data \n
	labels: Category labels \n
	style: CLUSTER, STACKED or PERCENTSTK
	"""
	assert isinstance(style, str), "'style' must be string"
	if style.lower() not in ["c", "s", "%"]:
		raise ValueError("'style' must be c, s or %")
	
	if labels != None:
		assert len(labels)>=2, "at least 2 labels expected"
	
	return _pydll.c_plot_bar((), {
			"height":height, 
			"labels":labels, 
			"style":style, 
			"fill":vars(fill) if fill != None else None, 
			"line":vars(line) if line != None else None})


#-----------------------------------------------------------------------------------


def barh(
	width:_Iterable, 
	labels:_Iterable = None, 
	style:str = "c", #cluster
	fill:_gdi.Brush = None, 
	line:_gdi.Pen = None):
	"""
	Plots horizontal bar chart

	## Input
	width : Numeric data \n
	labels : Category labels \n
	style: CLUSTER, STACKED or PERCENTSTK
	"""
	assert isinstance(style, str), "'style' must be string"
	if style.lower() not in ["c", "s", "%"]:
		raise ValueError("'style' must be c, s or %")
	
	if labels != None:
		assert len(labels)>=2, "at least 2 labels expected"
	
	return _pydll.c_plot_barh((),{
		"width":width, 
		"labels":labels, 
		"style":style, 
		"fill":vars(fill) if fill != None else None, 
		"line":vars(line) if line != None else None})





#-----------------------------------------------------------------------------------

def boxplot(
	data:_Iterable, 
	label:str = None, 
	fill:_gdi.Brush = None, 
	line:_gdi.Pen = None):
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
		"fill":vars(fill) if fill != None else None, 
		"line":vars(line) if line != None else None})





#-----------------------------------------------------------------------------------

def histogram(
		data:_Iterable, 
		mode = "f", #frequency 
		cumulative = False, 
		breaks:int|_Iterable = None, 
		fill:_gdi.Brush=None, 
		line:_gdi.Pen=None):
	"""
	Plots histogram

	## Input
	data:	Numeric data \n
	mode : density (d), frequency (f) and relative frequency (r).\n
	cumulative : True, cumulative distribution \n
	breaks : Number of breaks or the break points, int/iterable
	"""
	assert isinstance(mode, str), "'mode' must be string"
	if mode.lower() not in ["d", "f", "r"]:
		raise ValueError("'style' must be c, s or %")
	
	assert isinstance(cumulative, bool), "'cumulative' must be bool"

	if breaks != None:
		assert isinstance(breaks, int) or isinstance(breaks, _Iterable), "'breaks' must be int/Iterable"
		if isinstance(breaks, int):
			assert breaks>0, "'breaks' if integer, must be >0"
		else:
			Nums = [i for i in breaks if isinstance(i, int)]
			assert len(Nums)>0, "'breaks' (iterable) do not contain any integer"

	return _pydll.c_plot_histogram((), {
			"data":data, 
			"mode":mode, 
			"cumulative":cumulative, 
			"breaks":breaks, 
			"fill":vars(fill) if fill != None else None, 
			"line":vars(line) if line != None else None})





#-----------------------------------------------------------------------------------

def line(
	y:_Iterable, 
	labels:_Iterable = None, 
	style:str= "c", #cluster
	label:str = None,  
	marker:_defs.Marker=None, 
	line:_gdi.Pen=None):
	"""
	Plots line chart

	## Input:
	y : An iterable containing numeric data \n
	labels : Category labels \n
	style: CLUSTER, STACKED or PERCENTSTK \n
	label: Label of the individual series 
	"""
	assert isinstance(y, _Iterable), "'y' must be iterable"

	if labels != None:
		assert isinstance(labels, _Iterable), "'labels' must be iterable"
		assert len(labels)>=2, "At least 2 labels expected"

	assert isinstance(style, str), "'style' must be string"
	if style.lower() not in ["c", "s", "%"]:
		raise ValueError("'style' must be c, s or %")
	
	
	return _pydll.c_plot_line((), {
			"y":y, 
			"labels":labels, 
			"label":label, 
			"style":style, 
			"marker":dict(marker) if marker != None else None, 
			"line":vars(line) if line != None else None})





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
	return _pydll.c_plot_pie((),
				{"data":data, "labels":labels, "colors":colors, 
     				"explode":explode, "startangle":startangle})





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


def qqnorm(
		data:_Iterable, 
		label:str=None, 
		show:bool=True, 
		line:_gdi.Pen=None, 
		marker:_defs.Marker=None):
		"""
		Normal Quantile-quantile chart \n
		x-axis="Theoretical Quantiles" \n  
		y-axis="Sample Quantiles" \n

		## Input:
		data: Data \n
		show: Whether to show theoretical line or not 
		"""
		return _pydll.c_plot_qqnorm((),{
			"data":data, 
			"label": label, 
			"show":show, 
			"marker":dict(marker) if marker != None else None, 
			"line":vars(line) if line != None else None})





def qqplot(
		x:_Iterable,
		y:_Iterable,
		marker:_defs.Marker=None):
	"""
	Plots quantile-quantile chart using two data-sets (x,y)

	## Input
	x, y: Data
	"""
	return _pydll.c_plot_qqplot((),{
			"x":x, 
			"y":y,
			"marker":dict(marker) if marker != None else None})





#-----------------------------------------------------------------------------------

import numpy as _np

def quiver(
		x:_np.ndarray, 
		y:_np.ndarray, 
		u:_np.ndarray, 
		v:_np.ndarray, 
		scale:bool=False):
	""""
	Plots quiver chart

	## Input:
	x, y: (x,y) location, 2D ndarray \n
	u, v: length in x and y directions, 2D ndarray \n
	scale: Whether to scale the length of the arrows
	"""
	return _pydll.c_plot_quiver((),{
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
		label:str = None, 
		smooth:bool = False, 
		marker:_defs.Marker = None, 
		line:_gdi.Pen = None, 
		trendline:_defs.Trendline = None):
	"""
	Plot scatter charts

	## Input:
	x, y:	x- and y-data \n
	label: Label of the series \n
	smooth: Uses smoothing algorith to smooth lines (instead of broken)
	"""
	assert isinstance(x, _Iterable), "x must be iterable object"
	assert isinstance(y, _Iterable), "y must be iterable object"
	assert len(x) == len(y), "x and y must have same lengths"

	assert isinstance(smooth, bool), "'smooth' must be bool"

	if label != None:
		assert isinstance(label, str), "'label' must be string"

	return _pydll.c_plot_scatter((), {
		"x":x, 
		"y":y , 
		"name":label, 
		"smooth":smooth, 
		"marker":dict(marker) if marker!=None else None, 
		"line":vars(line) if line!=None else None, 
		"trendline":dict(trendline) if trendline!=None else None})




#convenience function
def plot(
		x:_Iterable, 
		y:_Iterable, 
		label:str=None, 
		color:str = None, 
		width:int = 1,
		style:int = 100, #solid pen
		smooth:bool=False):
	"""
	A convenience function to plot scatter chart without markers (with lines only)

	## Input:
	x, y:	x- and y-data \n
	label: Name of the series \n
	smooth: Smooth lines \n
	color: line color, check Color class \n
	style: line style, use PEN_XXX \n
	width: line width
	"""
	return scatter(
		x=x, 
		y=y, 
		label=label, 
		smooth=smooth, 
		marker=None, 
		line=_gdi.Pen(color=color, width=width, style=style))





def bubble(
		x:_Iterable,
		y:_Iterable,  
		size:_Iterable,
		color:str = None,
		mode:str = "A",
		scale:int=100,
		label:str=None):
	"""
	Plots bubble chart

	## Input:
	x, y, size:	x- and y- and size data \n
	color: color (str) \n
	mode: "A" area "W" diameter \n
	scale: size scale (0, 200] \n
	label: Name of the series	
	"""
	assert \
		isinstance(x, _Iterable) and \
		isinstance(y, _Iterable) and \
		isinstance(size, _Iterable), "x, y and size must be iterable objects."

	assert len(x) == len(y) and len(y) == len(size), "x, y and size must have same lengths"

	assert isinstance(mode, str), "'mode' must be string"
	assert isinstance(label, str), "'label' must be string"
	assert isinstance(color, str), "'color' must be string"

	assert isinstance(scale, int), "'scale' must be int"
	assert 0<scale<200, "'scale' must be in range (0, 200)"

	return _pydll.c_plot_bubble((), {
		"x":x, "y":y , "size":size, "color":color,"mode":mode.lower(), "scale":scale, "label":label})

	