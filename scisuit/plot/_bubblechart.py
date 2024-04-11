import numbers
from typing import Iterable as _Iterable

import numpy as np

from ..util import NiceNumbers, minmax
from ._charts import canvas
from .gdi import marker


def _ComputeAlphas(s:_Iterable)->list[float]:
	"""
	size of the bubble and its alpha are inversely proportional
	e.g., large bubbles have small alphas wherease 
	small bubbles have large alphas
	"""

	Alpha_Min, Alpha_Max = 0.1, 1.75
	Min, Max = minmax(s)

	assert Max>Min, "max > min expected for bubble size"

	Slope = (Alpha_Min - Alpha_Max)/(Max-Min)

	#equation of the line (x: bubble size, y: alpha)
	Alpha = lambda size: Slope*(size-Min) + Alpha_Max

	return [Alpha(i) for i in s]



def _ComputeScaledSizes(s:_Iterable, scale=1.0)->list[float]:
	"""
	Area based computation
	"""
	MINSIZE, MAXSIZE = 5, 50
	xx = np.array(s)
	MaxSize:float = np.max(xx)
	Arr = (xx/MaxSize)**0.5*MAXSIZE*scale
	return Arr.tolist()
	

def bubble(
		x:_Iterable,
		y:_Iterable,  
		s:_Iterable,
		scale:float=1.0,
		color:str|tuple|list = (255, 0, 0),
		label:str=None):
	"""
	Plots bubble chart

	## Input:
	x, y, s:	x- and y- and size data
	color: color
	label: Name (currently not in use)
	"""
	assert \
		isinstance(x, _Iterable) and \
		isinstance(y, _Iterable) and \
		isinstance(s, _Iterable), "x, y and s must be iterable objects."

	assert len(x) == len(y) and len(y) == len(s), "x, y and s must have same lengths"

	assert isinstance(label, str|None), "'label' must be string"
	assert isinstance(color, str|tuple|list), "'color' must be str|tuple|list"

	assert isinstance(scale, numbers.Real), "scale must be Real"
	assert 0<scale<2.0, "scale must be in [0, 2]"


	Alphas = _ComputeAlphas(s)
	Sizes = _ComputeScaledSizes(s, scale)
	MinX, MaxX = minmax(x)
	MinY, MaxY = minmax(y)

	NiceX, NiceY = NiceNumbers(MinX, MaxX), NiceNumbers(MinY, MaxY)

	canvas(
		[NiceX.min - NiceX.tickspace, NiceX.max + NiceX.tickspace], 
		[NiceY.min - NiceY.tickspace, NiceY.max + NiceY.tickspace])
	
	
	"""
	alpha values we use are actually luminiscence values

	If we draw the small bubble before a big bubble even though
	the big bubble has a lower alpha value than the small bubble, 
	the small bubble will not be shown. 
	
	Therefore, we sort in descending order according to bubble sizes and draw 
	the larger ones first.
	"""
	
	Sorted = []
	for i in range(len(x)):
		Sorted.append([x[i], y[i], round(Sizes[i]), Alphas[i]])
	
	#in-place sort (descending order) according to sizes
	Sorted.sort(key=lambda x: x[2], reverse=True)

	for l in Sorted:
		marker(xy=[l[0], l[1]], size=l[2], ec=color, fc=color, alpha=l[3])