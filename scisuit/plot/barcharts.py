import numpy as np
from typing import Iterable as _Iterable
from random import randint

from .gdi import rect
from .charts import canvas, ylim, set_xticks
from ..util import NiceNumbers, minmax





def bar(x, height, width=0.8, bottom=0.0, color = None, **kwargs):
	"""
	`x:` The x coordinates of the bars or category
	`height:` The height of the bars.
	`width:` The width of the bars.
	`bottom:` The y coordinate of the bottom side of the bars.
	"""
	assert isinstance(bottom, float|int|_Iterable)
	if isinstance(bottom, _Iterable):
		nums = [i for i in bottom if isinstance(i, float|int)]
		assert len(nums) == len(height), "if bottom is Iterable, its length must be equal to 'height's length"
	
	pos = np.array(x)
	X_HasStr = False
	if isinstance(pos[0], str):
		pos = list(range(len(x)))
		X_HasStr = True
	
	arr = np.array(height)

	_Min = np.min(bottom) if isinstance(bottom, _Iterable) else bottom
	_Max = np.max(arr + np.array(bottom) if isinstance(bottom, _Iterable) else arr + bottom)

	PrevMin, PrevMax = ylim()
	_Min = min(_Min, PrevMin)
	_Max = max(_Max, PrevMax)

	niceY = NiceNumbers(_Min, _Max)
	canvas(
		x=[-width, len(x)], 
		y=niceY.minmax, 
		vgrid=kwargs.get("vgrid") or False,
		hgrid=kwargs.get("hgrid") if kwargs.get("hgrid")!=None else True,
		haxis=kwargs.get("haxis") if kwargs.get("haxis")!=None else True,
		vaxis=kwargs.get("vaxis") if kwargs.get("vaxis")!=None else True
		)


	_Color = color or kwargs.get("fc") or kwargs.get("facecolor")
	if _Color == None:
		_Color = [randint(0, 255), randint(0, 255), randint(0, 255)]


	for i in range(len(height)):
		_bottom = bottom if isinstance(bottom, float|int) else bottom[i]
		_xcord = pos[i]-width/2 if X_HasStr else pos[i]
		xy = [_xcord, _bottom]

		kwargs["hatch"] = kwargs.get("hatch") or "solid"
		kwargs["facecolor"] = kwargs["fc"] = _Color if (isinstance(_Color, str) or isinstance(_Color[0], float|int)) else _Color[i]

		rect(xy=xy, width=width, height=height[i], **kwargs)
	
	if X_HasStr:
		set_xticks(pos, x)



