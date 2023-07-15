import numpy as np
from . import quiver

__all__ =['dirfield']



def dirfield(x, y, slope):
	"""
	Plots the direction field for a given function f=dy/dx \n

	## Input
	x, y: 2D numpy array (after using meshgrid) \n
	slope: 2D array resulting from evaluation of f=dy/dx, first order ODE
	"""

	# angle of inclination
	t = np.arctan(slope)

	# xy-components of arrow
	dx = np.cos(t)
	dy = np.sin(t); 

	#call quiver to visualize   
	quiver(x, y, dx, dy)
