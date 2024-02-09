import ctypes as _ct
from .._ctypeslib import pydll as _pydll
from ..app import App as _App



_app = _App()




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
		_ct.c_char(nrows), 
		_ct.c_char(ncols))



def subplot(row:int, col:int, nrows:int = 1, ncols:int = 1)->None:
	"""
	Must be called after the window is partitioned (by layout) to select a cell from the partition. \n

	row: row position of the cell (must be less than partition's number of rows),
	col: column position of the cell (must be less than partition's number of columns),
	nrows: number of rows the cell should span (default is 1)
	ncols: number of columns the cell should span (default is 1)
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
		_ct.c_char(row), 
		_ct.c_char(col), 
		_ct.c_ubyte(nrows), 
		_ct.c_ubyte(ncols))


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


def show(maximize = False, shared = False):
	"""
	Starts main loop and shows the chart(s) \n
	
	maximize: Whether to show chart as maximized (good for Psychrometric chart) \n
	shared: if there is any other application using a main loop
	"""
	_pydll.c_plot_show(_ct.c_bool(maximize))
	_app.mainloop(shared)