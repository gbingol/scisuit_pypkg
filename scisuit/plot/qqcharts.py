import numpy as _np
from typing import Iterable as _Iterable
from ..stats import qnorm
from .charts import scatter
from .chartelems import Marker
from ..util import minmax
from ..fitting import approx

def _ComputeQuantiles(X:_Iterable)->_Iterable:
	lenX = len(X)
	Quantiles = [0.0]*lenX

	a = 0.375 if lenX <= 10 else 0.5
	Percentile = lambda Order: (Order - a)/(lenX + 1.0 - 2*a)
	
	i=1
	for j in range(lenX):
		Percent = Percentile(i)
		Quantiles[j] = qnorm(Percent)
		i += 1
	
	return Quantiles



def qqnorm(
		data:_Iterable, 
		label:str=None, 
		show=True, 
		marker:str|Marker=None,
		**kwargs):
	"""
	Normal Quantile-quantile chart \n
	x-axis="Theoretical Quantiles" \n  
	y-axis="Sample Quantiles" \n

	## Input:
	data: Data \n
	show: Whether to show theoretical line or not 
	"""
	assert isinstance(data, _Iterable), "'data' must be iterable"
	if label!=None:
		assert isinstance(label, str), "'label' must be string"
	
	assert isinstance(show, bool), "'show' must be bool"

	_mark = marker or Marker()
	assert isinstance(_mark, str|Marker), "marker must be str|Marker"
	if isinstance(_mark, str):
		_mark = Marker(style=marker, size=kwargs.get("markersize") or 5)
	

	Quantiles = _ComputeQuantiles(data)

	if show:		
		MinQ, MaxQ = minmax(Quantiles)

		#Extend the line by 10% in both directions
		MinQ = MinQ*1.1
		MaxQ = MaxQ*1.1

		lwidth = (kwargs.get("lw") or kwargs.get("linewidth")) or 2
		scatter(x=(MinQ, MaxQ), y=(MinQ, MaxQ), marker=None, lw=lwidth, **kwargs)

	scatter(x=Quantiles, y=_np.sort(data), label=label, marker=marker)





def qqplot(x:_Iterable, y:_Iterable, **kwargs):
	"""
	Plots quantile-quantile chart using two data-sets (x,y)

	## Input
	x, y: Data
	"""
	assert isinstance(x, _Iterable), "'x' must be iterable"
	assert isinstance(y, _Iterable), "'y' must be iterable"

	xx = _np.array(x)
	xx.sort()

	yy = _np.array(y)
	yy.sort()

	lenX, lenY = len(xx), len(yy)

	if lenX != lenY:
		InterpData = yy if lenY>lenX else xx
		xdata = _np.arange(1, len(InterpData)+1)

		InterpPoints = approx(xdata, InterpData, min(lenX, lenY))

		if lenY>lenX:
			yy=InterpPoints[1]
		else:
			xx=InterpPoints[1]
	
	_style = kwargs.get("marker") or "c"
	_size = kwargs.get("markersize") or 5
	marker = Marker(style=_style, size=_size, **kwargs)

	scatter(x=xx, y=yy, marker=marker)


