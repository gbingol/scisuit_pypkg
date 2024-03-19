import numpy as np
from typing import Iterable as _Iterable

from .gdi import rect
from .charts import canvas, ylim
from ..util import NiceNumbers, minmax





def bar(x, height, width=0.8, bottom=0.0):
	"""
	`x:` The x coordinates of the bars
	`height:` The height of the bars.
	`width:` The width of the bars.
	`bottom:` The y coordinate of the bottom side of the bars.
	"""
	
	assert isinstance(bottom, float|int|_Iterable)
	if isinstance(bottom, _Iterable):
		nums = [i for i in bottom if isinstance(i, float|int)]
		assert len(nums) == len(height), "if bottom is Iterable, its length must be equal to 'height's length"

	
	pos = np.array(x)
	X_IsStr = False
	if isinstance(pos[0], str):
		pos = list(range(len(x)))
		X_IsStr = True
	
	arr = np.array(height)
	_x = list(x)
	_x.insert(0, "")
	_x.append("")

	_Min = np.min(bottom) if isinstance(bottom, _Iterable) else bottom
	_Max = np.max(arr + np.array(bottom) if isinstance(bottom, _Iterable) else arr + bottom)

	PrevMin, PrevMax = ylim()
	_Min = min(_Min, PrevMin)
	_Max = max(_Max, PrevMax)

	niceY = NiceNumbers(_Min, _Max)
	canvas(x=_x, y=niceY.minmax, xlabel=True, xs=-1.0)

	for i in range(len(height)):
		_bottom = bottom if isinstance(bottom, float|int) else bottom[i]
		_xcord = pos[i]-width/2 if X_IsStr else pos[i]
		xy = [_xcord, _bottom]

		rect(xy=xy, width=width, height=height[i])



