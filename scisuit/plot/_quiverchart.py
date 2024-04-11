import numbers

import numpy as _np

from ..util import NiceNumbers
from ._charts import canvas
from .gdi import arrow


def _MinMax(X:_np.ndarray)->tuple[float]:
	_min = X[0]
	_max = X[0]
	for i in range(1, len(X)):
		_min = X[i] if X[i]<_min else _min
		_max = X[i] if X[i]>_max else _max
	
	return _min, _max




def _ComputeScaleFactor(
		X:_np.ndarray, 
		Y:_np.ndarray,
		U:_np.ndarray, 
		V:_np.ndarray)->float:
	minX, maxX = _MinMax(X)
	minY, maxY = _MinMax(Y)

	LenArrows = _np.sqrt(U**2 + V**2)
	MaxLen = _np.max(LenArrows)

	niceX = NiceNumbers(minX, maxX)
	niceY = NiceNumbers(minY, maxY)

	return min(niceX.tickspace, niceY.tickspace)/MaxLen



def quiver(
		X:_np.ndarray, 
		Y:_np.ndarray,
		U:_np.ndarray, 
		V:_np.ndarray,
		scale=None,
		**kwargs)->None:
	
	""""
	Plots quiver chart

	## Input:
	x, y: (x,y) location, 2D ndarray \n
	u, v: length in x and y directions, 2D ndarray \n
	scale: if None automatic scaling takes place otherwise xu = x + u*scale is computed
	"""	
	assert len(X)==len(Y), "X and Y must have same lengths"
	assert len(U) == len(V), "U and V must have same lengths"
	assert len(X) == len(U), "X, Y, U, V must have same lengths"
	assert isinstance(scale, numbers.Real|None), "scale must be float|int|None"

	x, y = X.flatten(), Y.flatten()
	u, v = U.flatten(), V.flatten()

	_scale = scale
	if _scale == None:
		_scale = _ComputeScaleFactor(x, y, u, v)
	
	xu = x + u*_scale
	yv = y + v*_scale

	BndScaledX, BndScaledY = _MinMax(xu), _MinMax(yv)
	BndRawX, BndRawY = _MinMax(x), _MinMax(y)

	_MinX = min(BndScaledX[0], BndRawX[0])
	_MaxX = max(BndScaledX[1], BndRawX[1])
	_MinY = min(BndScaledY[0], BndRawY[0])
	_MaxY = max(BndScaledY[1], BndRawY[1])
	
	niceX = NiceNumbers(_MinX, _MaxX)
	niceY = NiceNumbers(_MinY, _MaxY)
	canvas(niceX.minmax, niceY.minmax)

	for i in range(len(x)):
		arrow(p1=(x[i], y[i]), p2=(xu[i], yv[i]),**kwargs)
	

def dirfield(
		x:_np.ndarray, 
		y:_np.ndarray, 
		slope:_np.ndarray):
	"""
	Plots the direction field for a given function f=dy/dx \n

	## Input
	x, y: 2D numpy array (after using meshgrid) \n
	slope: 2D array resulting from evaluation of f=dy/dx, first order ODE
	"""

	assert isinstance(x, _np.ndarray), "'x' must be ndarray"
	assert isinstance(y, _np.ndarray), "'y' must be ndarray"
	assert isinstance(slope, _np.ndarray), "'slope' must be ndarray"

	# angle of inclination
	t = _np.arctan(slope)

	# xy-components of arrow
	dx = _np.cos(t)
	dy = _np.sin(t); 

	#call quiver to visualize   
	quiver(x, y, dx, dy)

