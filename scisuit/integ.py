import numbers as _numbers
import types as _types
from typing import Iterable

from ctypes import py_object, c_double, c_int
from ._ctypeslib import pydll as _pydll




_pydll.c_integ_simpson.argtypes = [py_object, py_object]
_pydll.c_integ_simpson.restype = py_object

_pydll.c_integ_romberg.argtypes = [py_object, c_double, c_double, c_double, c_int]
_pydll.c_integ_romberg.restype = py_object

_pydll.c_integ_fixed_quad.argtypes = [py_object, c_double, c_double, c_int]
_pydll.c_integ_fixed_quad.restype = py_object





#--------------------------------------------------


def trapz(
		x:Iterable[_numbers.Real], 
		y:Iterable[_numbers.Real])->_numbers.Real:
	"""Computes the area using trapezoidal algorithm"""
	len_x, len_y = len(x), len(y)
	assert len_x == len_y, "x and y must be of same size."

	retval = 0.0
	for i in range(len_x-1):
		a, b = x[i], x[i + 1]
		f_a, f_b = y[i], y[i + 1]

		if b < a:
			raise ValueError("|X(i+1)-X(i)|>1E-5 expected.")

		retval += float(b - a) * float(f_a + f_b) / 2.0

	return retval




def cumtrapz(
		x:Iterable[_numbers.Real], 
		y:Iterable[_numbers.Real])->list[_numbers.Real]:
	"""Computes the left-tailed cumulative area"""
	val = 0.0
	retList =[0.0]

	for i in range(len(x)-1):
		a, b = x[i], x[i + 1]

		if b < a:
			raise ValueError("|X(i+1)-X(i)|>1E-5 expected.")

		temp = (y[i] + y[i + 1])/2.0
		val += float(b - a) * float(temp)

		retList.append(val)
	
	return retList



#------------------------------------------------

def simpson(
		x:Iterable[_numbers.Real], 
		y:Iterable[_numbers.Real])->float:
	"""Uses simpson's method (1/3 and 3/8)"""

	return _pydll.c_integ_simpson(x, y)



#------------------------------------------------

def romberg(f:_types.FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100)->float:
	"""
	Romberg integration

	#Input:
	f: Univariate function 
	a, b: limits of integration (b>a) 
	tol: tolerance for error 
	maxiter: Maximum number of iterations
	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"
	assert isinstance(tol, _numbers.Real), "tol must be real number"
	assert isinstance(maxiter, _numbers.Integral), "maxiter must be int"

	return _pydll.c_integ_romberg(
		f, 
		c_double(a), 
		c_double(b), 
		c_double(tol), 
		c_int(maxiter))



#------------------------------------------------

def fixed_quad(f:_types.FunctionType, 
	a:float, 
	b:float, 
	n:int=5)->float:
	"""
	Computes definite integral using fixed-order Gaussian quadrature.

	#Input:
	f: Univariate function \n
	a, b: limits of integration (b>a) \n
	n: Order of quadrature integration (2<=n<=6)
	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"
	assert isinstance(n, _numbers.Integral), "n must be int"

	return _pydll.c_integ_fixed_quad(
		f, 
		c_double(a), 
		c_double(b),  
		c_int(n))