import ctypes as _ct

from ._ctypeslib import pydll

pydll.c_plot_app.argtypes = []
pydll.c_plot_app.restype = None

pydll.c_plot_mainloop.argtypes = []
pydll.c_plot_mainloop.restype=_ct.c_bool

pydll.c_plot_ismainlooprunning.argtypes = []
pydll.c_plot_ismainlooprunning.restype=_ct.c_bool

pydll.c_plot_exitmainloop.argtypes = []
pydll.c_plot_exitmainloop.restype=_ct.c_bool




class App:
	def __init__(self) -> None:
		"""
		Initiates the GUI application
		"""
		#IMPORTANT: if not set colors/text of plots looks blurry
		_ct.windll.shcore.SetProcessDpiAwareness(True)
		pydll.c_plot_app()
	

	def mainloop(self):
		"""
		Starts the main loop

		returns True if mainloop is started
		"""
		return pydll.c_plot_mainloop()


	def ismainlooprunning(self):
		"""
		Is the main loop initiated by scisuit library running
		"""
		return pydll.c_plot_ismainlooprunning()


	def exitmainloop(self):
		"""
		Exits the main loop inititated by scisuit library and 
		closes all the associated windows. \n

		returns True if main loop is exited.
		"""
		return pydll.c_plot_exitmainloop()