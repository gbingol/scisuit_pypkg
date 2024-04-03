import ctypes as _ct
import dataclasses as _dc
import numbers as _numbers
from typing import Iterable

import numpy as _np
from numpy.polynomial import polynomial as _Polynomial

from ._ctypeslib import pydll as _pydll
from .util import minmax



__all__ = [
	'approx',
	'linearinterp', 
	'lagrange', 
	'spline', 
	'expfit', 
	'logfit', 
	'logistfit', 
	'polyfit', 
	'powfit', 
	'SplineResult']




def linearinterp(x1:float, y1:float, x2:float, y2:float, xval:float)->float:
	"""
	Linear interpolation

	## Inputs:
	x1, y1: First point \n
	x2, y2: Second point \n
	xval: x-value in [x1, x2] 

	## Returns:
	y-value in [y1, y2] corresponding to xval
	"""

	if(x1 == x2): 
		return y1 
	
	m,n = 0, 0
	m = (y2 - y1) / (x2 - x1)
	n = y2 - m * x2

	return m * xval + n





def lagrange(
		x:Iterable, 
		y:Iterable, 
		value:float)->float:
	"""
	Constructs lagrange polynomial from x,y to compute the given value.
	"""
	assert issubclass(value, _numbers.Real)

	return _pydll.c_fit_lagrange(x, y, _ct.c_double(value))


########################################################################################


@_dc.dataclass
class SplineResult:
	"""
	poly: Numpy polynomial
	lower, upper: lower and upper bounds of the polynomial
	"""
	poly:_Polynomial.Polynomial = None
	lower:float = None
	upper: float = None


def spline(x:Iterable, y:Iterable)->list[SplineResult]:
	"""
	Constructs natural cubic spline polynomials from x, y
	"""
	lst = _pydll.c_fit_spline(x, y)
	
	return  [SplineResult(_Polynomial.Polynomial(l[0]), l[1], l[2]) for l in lst]


########################################################################################


def expfit(
		x:Iterable, 
		y:Iterable, 
		intercept:None|float=None)->list:
	"""
	Fits x,y to the equation y = a*exp(b*x) \n
	Returns [a, b]

	## Note:
	If intercept is not provided both a, b are computed. \n
	If intercept is given then a=intercept and b is computed accordingly.
	"""
	if(intercept!=None):
		assert issubclass(intercept, _numbers.Real)

	return _pydll.c_fit_expfit(x, y, intercept)


def logfit(x:Iterable, y:Iterable)->list:
	"""
	Fits x,y to the equation y = a*ln(x) + b \n
	Returns [a, b]
	"""

	return _pydll.c_fit_logfit(x, y)


def logistfit(x:Iterable, y:Iterable, limit = None)->list:
	"""
	Fits to the equation y = L / (1 + exp(b0 + b1*x)) \n
	Returns either [L, b0, b1] or [b0, b1]

	## Inputs:
	limit: None or float
	"""
	if(limit!=None):
		assert issubclass(limit, _numbers.Real)

	return _pydll.c_fit_logistfit(x, y, limit)


def polyfit(x:Iterable, y:Iterable, deg)->tuple:
	"""
	Uses numpy.polynomial.polynomial.polyfit
	returns (coefficients, residuals)
	"""
	coeffs, stats = _Polynomial.polyfit(x=x, y=y, deg=deg)
	return coeffs, stats[0]


def powfit(x:Iterable, y:Iterable)->list[float]:
	"""
	Fits to the equation y = a*x^n \n
	Returns [a, n]
	"""
	return _pydll.c_fit_powfit(x,y)




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