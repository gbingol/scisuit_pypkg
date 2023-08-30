import ctypes as _ct
import numpy as _np

from ..util import parent_path as _parent_path
from .enums import Bar_Type, Line_Type, Histogram_Mode



_path = _parent_path(__file__, level=1) / "scisuit_plotter"
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

pltdll.c_plot_piepie.argtypes = [_ct.py_object, _ct.py_object]
pltdll.c_plot_piepie.restype=_ct.py_object

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



def bar(
	height:list, 
	labels=None, 
	name=None, 
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
	name: Name of the series \n
	type: clustered, stacked and 100% stacked \n
	title: Title of the chart
	"""
	return pltdll.c_plot_bar((),
			{"height":height, "labels":labels, "name":name, "title":title, "type":type, 
    			"fill":fill, "line":line, "hwnd":hwnd})



def barh(
	width:list, 
	labels=None, 
	name=None, 
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
	name: Name of the series \n
	type: clustered, stacked and 100% stacked.\n
	title: Title of the chart
	"""
	return pltdll.c_plot_barh((),
			{"width":width, "labels":labels, "name":name, "title":title, "type":type, 
    			"fill":fill, "line":line, "hwnd":hwnd})



def boxplot(
	data:list|_np.ndarray, 
	name:str=None, 
	title:str=None, 
	fill:dict=None, 
	line:dict=None, 
	hwnd=None):
	"""
	Plots box-whisker chart and returns a window handle.

	## Input
	data : Data to be plotted \n
	name:	Name of the series \n
	title: Title of the chart 
	"""
	return pltdll.c_plot_boxplot((),
			{"data":data, "name":name, "title":title, "fill":fill, "line":line, "hwnd":hwnd})



def histogram(
		data:list|_np.ndarray, 
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



def line(
	y:list|_np.ndarray, 
	labels:list=None, 
	name:str=None, 
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
	name:	Name of the series \n
	type:	clustered, stacked and 100% stacked \n
	title: Title of the chart
	"""
	return pltdll.c_plot_line((),
			 {"y":y, "labels":labels, "name":name, "title":title, 
     			"type":type, "marker":marker, "line":line, "hwnd":hwnd})


def pie(
	data:list|_np.ndarray, 
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



def piepie(
	data:list|_np.ndarray, 
	title:str=None, 
	labels:list=None, 
	groups:list=None, 
	lcolors:list=None, 
	rcolors:list=None, 
	lexplode:list|int=None, 
	rexplode:list|int=None,
	legend=True, 
	hwnd=None):
	"""
	Plots pie pie chart

	## Inputs:
	data : Data of individual slices \n
	title: Title of the chart \n
	labels: Label of individual slices \n
	groups: group membership only containing two unique numbers, i.e. [1, 2, 2, 1] \n
	lcolors: Color of individual slices at the left pie \n
	rcolors: If exists, color of individual slices at the right pie \n
	lexplode: Explosion level of left pie \n
	rexplode: If exists, explosion level of right pie \n
	legend: Whether to show legend or not \n
	"""
	return pltdll.c_plot_piepie((),
			{"data":data, "title":title, "labels":labels, 
       		"groups":groups, "lcolors":lcolors, "rcolors":rcolors, 
			"lexplode":lexplode, "rexplode":rexplode,
			"legend":legend, "hwnd":hwnd})



def psychrometry(Tdb:list=None, RH:list=None, P=101325):
	"""
	Plots psychromety chart.

	## Input
	Tdb: [min, max], minimum and maximum dry-bulb temperatures (Celcius) \n
	RH: A list in increasing order containing the requested relative humidity (%) lines \n
	P: Absolute pressure (Pa)
	"""
	return pltdll.c_plot_psychrometry((),{'Tdb':Tdb, 'RH':RH, 'P':P})



def qqnorm(
		data:list|_np.ndarray,  
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
		x:list|_np.ndarray,
		y:list|_np.ndarray,
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
			{"x":x, "y":y,"u":u, "v":v, "scale":scale, "title":title, "xlab":xlab, "ylab":ylab})



def dirfield(x, y, slope):
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



def scatter(
		y:list|_np.ndarray, 
		x:list|_np.ndarray=None, 
		name:str=None, 
		title:str=None, 
		xlab:str=None, 
		ylab:str=None, 
		smooth:bool=False, 
		bubble:dict=None, 
		marker:dict=None, 
		line:dict=None, 
		trendline:dict=None, 
		hwnd=None):
	"""
	Plot scatter charts and returns a window handle

	## Input:
	x, y:	x- and y-data \n
	name:	Name of the series \n
	title: Title of the chart \n
	xlab:	Label of x-axis \n
	ylab:	Label of y-axis \n
	smooth: Spline algorithm is applied to smooth the line \n
	hwnd:	Window handle. If None, a new window is opened \n 

	Bubble Properties \n
	size:	size data (list), color: color (str), \n
	mode: "A" area "W" diameter, scale: size scale (0, 200]
	"""
	return pltdll.c_plot_scatter((), 
		{'y':y ,"x":x, "name":name, "title":title, "xlab":xlab, "ylab":ylab, "smooth":smooth, 
		"bubble":bubble, "marker":marker, "line":line, "trendline":trendline, "hwnd":hwnd})
