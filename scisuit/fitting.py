from ._ctypeslib import core as _core
import ctypes as _ct
import numbers as _numbers
from numpy.polynomial import polynomial as _Polynomial


__all__ = ['linearinterp', 'lagrange', 'spline', 'expfit', 'logfit', 'logistfit', 'polyfit', 'powfit']



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
	
	m,n=0, 0
	m = (y2 - y1) / (x2 - x1)
	n = y2 - m * x2

	return m * xval + n





def lagrange(x, y, val:float)->float:
	"""
	Constructs lagrange polynomial from x,y to compute the given value.

	## Inputs:
	x, y: list/ndarray \n
	val: value in the range of x whose corresponding y value is wish to be known.
	"""
	assert issubclass(val, _numbers.Real)

	return _core.c_fit_lagrange(x, y, _ct.c_double(val))


def spline(x, y)->list:
	"""
	Constructs natural cubic spline polynomials from x, y

	## Inputs:
	x, y: list/ndarray

	## Return:
	Returns a 2D Python list, where each sub-list contains exactly 3 entries: \n
	1) List of coefficients of the cubic polynomial,
	2) Lower bound,
	3) Upper bound.
	"""
	return _core.c_fit_spline(x, y)



def expfit(x, y, intercept=None)->list:
	"""
	Fits x,y to the equation y = a*exp(b*x) \n
	return list is [a, b]

	## Inputs:
	x, y: list/ndarray \n
	intercept: None or float

	## Note:
	If intercept is not provided both a, b are computed. \n
	If intercept is given then a=intercept and b is computed accordingly.
	"""
	if(intercept!=None):
		assert issubclass(intercept, _numbers.Real)

	return _core.c_fit_expfit(x, y, intercept)


def logfit(x, y)->list:
	"""
	Fits x,y to the equation y = a*ln(x) + b \n
	return list is [a, b]

	## Inputs:
	x, y: list/ndarray
	"""

	return _core.c_fit_logfit(x, y)


def logistfit(x, y, limit = None)->list:
	"""
	Fits x,y to the equation y = L / (1 + exp(b0 + b1*x)) \n
	return list is [L, b0, b1] or [b0, b1]

	## Inputs:
	x, y: list/ndarray \n
	limit: None or float
	"""
	if(limit!=None):
		assert issubclass(limit, _numbers.Real)

	return _core.c_fit_logistfit(x, y, limit)


def polyfit(x, y, deg)->tuple:
	"""
	uses NumPy's polynomial fitting (numpy.polynomial.polynomial.polyfit) \n
	returns (coefficients, residuals)

	## Inputs:
	x, y: list/ndarray

	"""
	coeffs, stats = _Polynomial.polyfit(x=x, y=y, deg=deg)
	return coeffs, stats[0]


def powfit(x, y)->list:
	"""
	Fits x,y to the equation y = a*x^n
	returns [a, n]

	## Inputs:
	x, y: list/ndarray
	"""
	return _core.c_fit_powfit(x,y)

