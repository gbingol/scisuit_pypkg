import numbers
from random import randint
from typing import Iterable as _Iterable

import numpy as np

from ..util import NiceNumbers, minmax
from ._charts import canvas, set_xticks, set_yticks, xlim, ylim
from .gdi import rect, makegroup


def bar(
		x, 
		height, 
		width=0.8, 
		bottom=0.0, 
		color = None, 
		label:str|None = None,
		**kwargs):
	"""
	`x:` The x coordinates of the bars or category
	`height:` The height of the bars.
	`width:` The width of the bars.
	`bottom:` The y coordinate of the bottom side of the bars.
	"""
	assert isinstance(bottom, numbers.Real|_Iterable)
	if isinstance(bottom, _Iterable):
		nums = [i for i in bottom if isinstance(i, numbers.Real)]
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
		vaxis=kwargs.get("vaxis") if kwargs.get("vaxis")!=None else True,
		scale=kwargs.get("scale") if kwargs.get("scale")!=None else False
		)


	_Color = color or kwargs.get("fc") or kwargs.get("facecolor")
	if _Color == None:
		_Color = [randint(0, 255), randint(0, 255), randint(0, 255)]

	ownerid = 0
	members = []
	for i in range(len(height)):
		_bottom = bottom if isinstance(bottom, numbers.Real) else bottom[i]
		_xcord = pos[i]-width/2 if X_HasStr else pos[i]
		xy = [_xcord, _bottom]

		kwargs["hatch"] = kwargs.get("hatch") or "solid"
		kwargs["facecolor"] = kwargs["fc"] = _Color if (isinstance(_Color, str) or isinstance(_Color[0], numbers.Real)) else _Color[i]

		if i==0 and isinstance(label, str):
			ownerid = rect(xy=xy, width=width, height=float(abs(height[i])), label=label, **kwargs)
		else:
			id = rect(xy=xy, width=width, height=float(abs(height[i])), **kwargs)
			members.append(id)
	
	if ownerid>0 and len(members)>0:
		makegroup(owner=ownerid, members=members)	
	
	if X_HasStr:
		set_xticks(pos, x)





def barh(
		y, 
		width, 
		height=0.8, 
		left=0.0, 
		color = None, 
		**kwargs):
	"""
	`y:` The y coordinates of the bars or category
	`height:` The height of the bars.
	`width:` The width of the bars.
	`bottom:` The y coordinate of the bottom side of the bars.
	"""
	assert isinstance(left, numbers.Real|_Iterable)
	if isinstance(left, _Iterable):
		nums = [i for i in left if isinstance(i, numbers.Real)]
		assert len(nums) == len(width), "if left is Iterable, its length must be equal to 'width's length"
	
	pos = np.array(y)
	X_HasStr = False
	if isinstance(pos[0], str):
		pos = list(range(len(y)))
		X_HasStr = True
	
	arr = np.array(width)

	_Min = np.min(left) if isinstance(left, _Iterable) else left
	_Max = np.max(arr + np.array(left) if isinstance(left, _Iterable) else arr + left)

	PrevMin, PrevMax = xlim()
	_Min = min(_Min, PrevMin)
	_Max = max(_Max, PrevMax)

	niceX = NiceNumbers(_Min, _Max)
	canvas(
		y=[-height, len(y)], 
		x=niceX.minmax, 
		hgrid=kwargs.get("hgrid") or False,
		vgrid=kwargs.get("vgrid") if kwargs.get("vgrid")!=None else True,
		haxis=kwargs.get("haxis") if kwargs.get("haxis")!=None else True,
		vaxis=kwargs.get("vaxis") if kwargs.get("vaxis")!=None else True
		)


	_Color = color or kwargs.get("fc") or kwargs.get("facecolor")
	if _Color == None:
		_Color = [randint(0, 255), randint(0, 255), randint(0, 255)]


	for i in range(len(width)):
		_xcoord = left if isinstance(left, numbers.Real) else left[i]
		_ycoord = pos[i]-height/2 if X_HasStr else pos[i]
		xy = [_xcoord, _ycoord]

		kwargs["hatch"] = kwargs.get("hatch") or "solid"
		kwargs["facecolor"] = kwargs["fc"] = _Color if (isinstance(_Color, str) or isinstance(_Color[0], numbers.Real)) else _Color[i]

		rect(xy=xy, width=float(abs(width[i])), height=float(height), **kwargs)
	
	if X_HasStr:
		set_yticks(pos, y)