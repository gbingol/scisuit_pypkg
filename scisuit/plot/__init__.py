import ctypes as _ct
from ..util import parent_path as _parent_path


_path = _parent_path(__file__, level=1) / "scisuit_plotter_d"
_plt = _ct.PyDLL(str(_path))


_plt.c_plot_bar.argtypes = [_ct.py_object, _ct.py_object]
_plt.c_plot_bar.restype=_ct.py_object

_plt.c_plot_barh.argtypes = [_ct.py_object, _ct.py_object]
_plt.c_plot_barh.restype=_ct.py_object

_plt.c_plot_scatter.argtypes = [_ct.py_object, _ct.py_object]
_plt.c_plot_scatter.restype=_ct.py_object

_plt.c_plot_psychrometry.argtypes = [_ct.py_object, _ct.py_object]
_plt.c_plot_psychrometry.restype=_ct.py_object

_plt.c_plot_app.argtypes = []
_plt.c_plot_app.restype=_ct.py_object

_plt.c_plot_mainloop.argtypes = [_ct.c_bool]
_plt.c_plot_mainloop.restype=_ct.c_bool

_plt.c_plot_ismainlooprunning.argtypes = []
_plt.c_plot_ismainlooprunning.restype=_ct.c_bool

_plt.c_plot_exitmainloop.argtypes = []
_plt.c_plot_exitmainloop.restype=_ct.c_bool

_plt.c_plot_close.argtypes = [_ct.py_object]
_plt.c_plot_close.restype=_ct.c_bool




def bar(height:list, labels=None, name=None, title=None, type="c", fill=None, line=None, hwnd=None):
	"""
	Plots bar chart

	## Input
	height : Numeric data \n
	labels : Category labels \n
	name:	Name of the series \n
	type:	"c", "s" and "%" for clustered, stacked and 100% stacked, respectively.\n
	title: Title of the chart ← string
	"""
	return _plt.c_plot_bar((),
			{"height":height, "labels":labels, "name":name, "title":title, "type":type, 
    			"fill":fill, "line":line, "hwnd":hwnd})



def barh(width:list, labels=None, name=None, title=None, type="c", fill=None, line=None, hwnd=None):
	"""
	Plots horizontal bar chart

	## Input
	width : Numeric data \n
	labels : Category labels \n
	name:	Name of the series \n
	type:	"c", "s" and "%" for clustered, stacked and 100% stacked, respectively.\n
	title: Title of the chart ← string
	"""
	return _plt.c_plot_barh((),
			{"width":width, "labels":labels, "name":name, "title":title, "type":type, 
    			"fill":fill, "line":line, "hwnd":hwnd})



def scatter(y, x:list=None, name:str=None, title:str=None, 
	    xlab:str=None, ylab:str=None, smooth:bool=False, 
	    bubble:dict=None, 
	    marker:dict=None, line:dict=None, trendline:dict=None, hwnd=None):
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
	mode: "A" area "W" diameter, scale: size scale (0, 200] \n


	"""
	return _plt.c_plot_scatter((), 
		{'y':y ,"x":x, "name":name, "title":title, "xlab":xlab, "ylab":ylab, "smooth":smooth, 
		"bubble":bubble, "marker":marker, "line":line, "trendline":trendline, "hwnd":hwnd})



def psychrometry(Tdb:list=None, RH:list=None, P=101325):
	"""
	Plots psychromety chart.

	## Input
	Tdb: [min, max], minimum and maximum dry-bulb temperatures (Celcius) \n
	RH: A list in increasing order containing the requested relative humidity (%) lines \n
	P: Absolute pressure (Pa)
	"""
	return _plt.c_plot_psychrometry((),{'Tdb':Tdb, 'RH':RH, 'P':P})



def app():
	"""
	Initiates a GUI application
	"""
	#IMPORTANT: if not set colors/text of plots looks blurry
	_ct.windll.shcore.SetProcessDpiAwareness(True)
	return _plt.c_plot_app()


def mainloop(shared=False):
	"""
	Once a GUI application is initiated, starts the main loop \n
	shared: True, if there is any other application using a main loop \n

	returns True if mainloop is started
	"""
	return _plt.c_plot_mainloop(_ct.c_bool(shared))


def ismainlooprunning():
	"""
	Is there any main loop initiated by scisuit plot library running
	"""
	return _plt.c_plot_ismainlooprunning()


def exitmainloop():
	"""
	Exits the main loop inititated by scisuit plot library and 
	closes all the associated windows. \n

	returns True if main loop is exited.
	"""
	return _plt.c_plot_exitmainloop()


def close(hwnd):
	"""
	Closes the window with the given window handle \n
	hwnd: Window handle \n

	returns True if the window is closed
	"""
	return _plt.c_plot_close(hwnd)
	