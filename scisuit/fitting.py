from dataclasses import dataclass
from numbers import Real
from typing import Iterable

from numpy import ndarray, zeros
from numpy.polynomial import polynomial as _Polynomial
from .util import minmax



from ctypes import py_object, c_double
from ._ctypeslib import pydll as _pydll


_pydll.c_fit_expfit.argtypes = [py_object, py_object, py_object]
_pydll.c_fit_expfit.restype = py_object


_pydll.c_fit_lagrange.argtypes = [py_object, py_object,c_double]
_pydll.c_fit_lagrange.restype = py_object


_pydll.c_fit_logfit.argtypes = [py_object, py_object]
_pydll.c_fit_logfit.restype = py_object


_pydll.c_fit_logistfit.argtypes = [py_object, py_object, py_object]
_pydll.c_fit_logistfit.restype = py_object


_pydll.c_fit_powfit.argtypes = [py_object, py_object]
_pydll.c_fit_powfit.restype = py_object


_pydll.c_fit_spline.argtypes = [py_object, py_object]
_pydll.c_fit_spline.restype = py_object




#-----------------------------------------------------


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





#-------------------------------------------------

def lagrange(
		x:Iterable[Real], 
		y:Iterable[Real], 
		value:float)->float:
	"""Constructs lagrange polynomial from x,y to compute the given value."""
	assert isinstance(value, Real)
	return _pydll.c_fit_lagrange(x, y, c_double(value))





#-------------------------------------


@dataclass
class SplineResult:
	"""
	poly: Numpy polynomial
	lower, upper: lower and upper bounds of the polynomial
	"""
	poly:_Polynomial.Polynomial = None
	lower:float = None
	upper: float = None


def spline(
		x:Iterable[Real], 
		y:Iterable[Real])->list[SplineResult]:
	"""Constructs natural cubic spline polynomials from x, y"""
	lst = _pydll.c_fit_spline(x, y)	
	return  [SplineResult(_Polynomial.Polynomial(l[0]), l[1], l[2]) for l in lst]





#------------------------------------------

@dataclass
class expfitResult:
	a:float = None
	b:float = None

	def __str__(self):
		return f"y = {self.a}*exp({self.b}*x)"
	
def expfit(
		x:Iterable[Real], 
		y:Iterable[Real], 
		intercept:None|float=None)->expfitResult:
	"""
	Fits x,y to the equation y = a*exp(b*x)  
	Returns [a, b]

	## Note:
	- If intercept is not provided both a, b are computed.  
	- If intercept is given then a=intercept and b is computed accordingly.
	"""
	if(intercept!=None):
		assert isinstance(intercept, Real)

	lst = _pydll.c_fit_expfit(x, y, intercept)

	return expfitResult(a=lst[0], b=lst[-1])



#------------------------------------------------


@dataclass
class logfitResult:
	a:float = None
	b: float = None

	def __str__(self):
		sign = "+ " if self.b>0 else "-"
		return f"y = {self.a}*ln(x) {sign} {abs(self.b)}"

def logfit(
		x:Iterable[Real], 
		y:Iterable[Real])->logfitResult:
	"""
	Fits x,y to the equation y = a*ln(x) + b  
	Returns [a, b]
	"""
	lst = _pydll.c_fit_logfit(x, y)
	return logfitResult(a=lst[0], b=lst[-1])




#---------------------------------------------------

@dataclass
class logistfitResult:
	L:float = None
	b0:float = None
	b1:float = None

	def __str__(self):
		return "y = " + str(self.L) + "/" + \
				"(1 + exp(" + \
				str(self.b0) + " + " + str(self.b1) + "x" + "))"

def logistfit(
		x:Iterable[Real], 
		y:Iterable[Real], 
		limit:Real = None)->logistfitResult:
	"""
	Fits to the equation y = L / (1 + exp(b0 + b1*x))  
	Returns either [L, b0, b1] or [b0, b1]

	limit: None or float
	"""
	if(limit!=None):
		assert isinstance(limit, Real)

	lst =  _pydll.c_fit_logistfit(x, y, limit)

	return logistfitResult(
			L= limit if limit!=None else lst[0],
			b0= lst[0] if limit!=None else lst[1],
			b1= lst[-1])




#--------------------------------------

def polyfit(
		x:Iterable[Real], 
		y:Iterable[Real], 
		deg)->tuple:
	"""
	Uses numpy.polynomial.polynomial.polyfit  
	returns (coefficients, residuals)
	"""
	coeffs, stats = _Polynomial.polyfit(x=x, y=y, deg=deg)
	return coeffs, stats[0]




#----------------------------------------------

@dataclass
class powfitResult:
	a:float = None
	n:float = None

	def __str__(self):
		return "y = " + str(self.a) + "*x^" + str(self.n)

def powfit(
		x:Iterable[Real], 
		y:Iterable[Real])->powfitResult:
	"""
	Fits to the equation y = a*x^n  
	Returns [a, n]
	"""
	lst = _pydll.c_fit_powfit(x,y)
	return powfitResult(a=lst[0], n=lst[-1])




#-------------------------------------------

def approx(
		x:ndarray, 
		y:ndarray, 
		n=50)->tuple[ndarray, ndarray]:
	"""
	Returns points which linearly interpolate (  
	interpolation takes place at n equally spaced points   
	spanning the interval [min(x), max(x)]).

		
	`x, y:` Numeric vectors giving the coordinates of the points to be interpolated.  
	`n:` Number of equally spaced data points [min(x), min(y)]
	"""
	assert n>1, "n>1 expected"

	v = zeros(n)
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