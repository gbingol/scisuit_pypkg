import ctypes as _ct
from .plot import pltdll

pltdll.c_plot_app.argtypes = []
pltdll.c_plot_app.restype=_ct.py_object

pltdll.c_plot_mainloop.argtypes = [_ct.c_bool]
pltdll.c_plot_mainloop.restype=_ct.c_bool

pltdll.c_plot_ismainlooprunning.argtypes = []
pltdll.c_plot_ismainlooprunning.restype=_ct.c_bool

pltdll.c_plot_exitmainloop.argtypes = []
pltdll.c_plot_exitmainloop.restype=_ct.c_bool

pltdll.c_plot_close.argtypes = [_ct.py_object]
pltdll.c_plot_close.restype=_ct.c_bool



class App:
	def __init__(self) -> None:
		"""
		Initiates the GUI application
		"""
		#IMPORTANT: if not set colors/text of plots looks blurry
		_ct.windll.shcore.SetProcessDpiAwareness(True)
		pltdll.c_plot_app()
	

	def mainloop(self, shared=False):
		"""
		Starts the main loop \n
		shared: True, if there is any other application using a main loop \n

		returns True if mainloop is started
		"""
		return pltdll.c_plot_mainloop(_ct.c_bool(shared))


	def ismainlooprunning(self):
		"""
		Is the main loop initiated by scisuit library running
		"""
		return pltdll.c_plot_ismainlooprunning()


	def exitmainloop(self):
		"""
		Exits the main loop inititated by scisuit library and 
		closes all the associated windows. \n

		returns True if main loop is exited.
		"""
		return pltdll.c_plot_exitmainloop()


	def closewnd(self, hwnd):
		"""
		Closes the window with the given window handle \n
		hwnd: Window handle \n

		returns True if the window is closed
		"""
		return pltdll.c_plot_close(hwnd)