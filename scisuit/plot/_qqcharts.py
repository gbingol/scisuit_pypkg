from typing import Iterable as _Iterable

import numpy as _np


from ..stats import qnorm
from ..util import minmax
from ._chartelems import Marker
from ._charts import scatter
from ..stats import qnorm


def linearinterp(x1:float, y1:float, x2:float, y2:float, xval:float)->float:
	"""
	Linear interpolation returns y-value in [y1, y2] corresponding to xval.

	x1, y1: First point  
	x2, y2: Second point  
	xval: x-value in [x1, x2] 
	"""

	if(x1 == x2): 
		return y1 
	
	m,n = 0, 0
	m = (y2 - y1) / (x2 - x1)
	n = y2 - m * x2

	return m * xval + n






#-------------------------------------------

def approx(
		x:_np.ndarray, 
		y:_np.ndarray, 
		n=50)->tuple[_np.ndarray, _np.ndarray]:
	"""
	Returns points which linearly interpolate (  
	interpolation takes place at n equally spaced points   
	spanning the interval [min(x), max(x)]).

		
	`x, y:` Numeric vectors giving the coordinates of the points to be interpolated.  
	`n:` Number of equally spaced data points [min(x), min(y)]
	"""
	assert n>1, "n>1 expected"

	v = _np.zeros(n)
	if type(y) == type(None):
		Min, Max = minmax(x)
		strideLen = (Max-Min)/(n-1)
		v[0], v[n-1] = Min, Max
		for i in range(1, len(v)-1):
			v[i] = Min + i * strideLen
		
		return v
	
	assert len(x)==len(y), "x and y must have same lengths"

	"""
	Generate n data points in the interval min(x) and max(x)  
	Note that data points are sorted by nature.
	"""
	XX = approx(x, None, n)

	for i in range(len(x)-1):
		for j in range(n):
			if (x[i] <= XX[j] <= x[i + 1]):
				x1, x2 = x[i], x[i + 1]
				y1, y2 = y[i], y[i + 1]
				v[j] = linearinterp(x1, y1, x2, y2, XX[j])

	return XX, v




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
	Normal Quantile-quantile chart  
	x-axis="Theoretical Quantiles"  
	y-axis="Sample Quantiles"  
    
	## Input:
	data: Data  
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
		#Following R's qqline style
		xmin, xmax = qnorm(0.25), qnorm(0.75)
		ymin, ymax = _np.quantile(list(data), q=0.25), _np.quantile(list(data), q=0.75)

		slope = (ymax-ymin)/(xmax-xmin)
		f = lambda x: slope*(x-xmin) + ymin

		xdatamin, xdatamax = minmax(Quantiles)

		kwargs["lw"] = (kwargs.get("lw") or kwargs.get("linewidth")) or 2
		scatter(x=(xdatamin, xdatamax), y=(f(xdatamin), f(xdatamax)), marker=None, **kwargs)

	scatter(x=Quantiles, y=_np.sort(data), label=label, marker=marker)





def qqplot(
		x:_Iterable, 
		y:_Iterable, 
		**kwargs):
	"""
	Plots quantile-quantile chart using two data-sets (x,y)  
  
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


