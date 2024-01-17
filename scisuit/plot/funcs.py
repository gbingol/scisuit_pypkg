import ctypes as _ct
from .._ctypeslib import pydll as _pydll
from ..app import App as _App



_app = _App()


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
	Starts main loop and shows the chart(s)
	
	## Input:
	maximize: Whether to show chart as maximized (good for Psychrometric chart) \n
	shared: if there is any other application using a main loop
	"""
	_pydll.c_plot_show(_ct.c_bool(maximize))
	_app.mainloop(shared)