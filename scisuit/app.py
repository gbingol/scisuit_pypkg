import ctypes as _ct
from ._ctypeslib import pltDLL

pltDLL.c_plot_app.argtypes = []
pltDLL.c_plot_app.restype = None

pltDLL.c_plot_mainloop.argtypes = [_ct.c_bool]
pltDLL.c_plot_mainloop.restype=_ct.c_bool

pltDLL.c_plot_ismainlooprunning.argtypes = []
pltDLL.c_plot_ismainlooprunning.restype=_ct.c_bool

pltDLL.c_plot_exitmainloop.argtypes = []
pltDLL.c_plot_exitmainloop.restype=_ct.c_bool




class App:
	def __init__(self) -> None:
		"""
		Initiates the GUI application
		"""
		#IMPORTANT: if not set colors/text of plots looks blurry
		_ct.windll.shcore.SetProcessDpiAwareness(True)
		pltDLL.c_plot_app()
	

	def mainloop(self, shared=False):
		"""
		Starts the main loop \n
		shared: True, if there is any other application using a main loop \n

		returns True if mainloop is started
		"""
		return pltDLL.c_plot_mainloop(_ct.c_bool(shared))


	def ismainlooprunning(self):
		"""
		Is the main loop initiated by scisuit library running
		"""
		return pltDLL.c_plot_ismainlooprunning()


	def exitmainloop(self):
		"""
		Exits the main loop inititated by scisuit library and 
		closes all the associated windows. \n

		returns True if main loop is exited.
		"""
		return pltDLL.c_plot_exitmainloop()