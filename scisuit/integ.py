import ctypes as _ct
import math as _math
import numbers as _numbers
import types as _types
from typing import Iterable

import numpy as _np

from ._ctypeslib import pydll as _pydll




def cumtrapz(
		x:Iterable, 
		y:Iterable)->list:
	"""Computes the left-tailed cumulative area"""
	val = 0.0
	retList =[0.0]

	for i in range(len(x)-1):
		a, b = x[i], x[i + 1]

		if _math.isclose(b, a, abs_tol = 1E-5) or b < a:
			raise ValueError("|X(i+1)-X(i)|>1E-5 expected.")

		temp = (y[i] + y[i + 1])/2.0
		val += (b - a) * temp

		retList.append(val)
	
	return retList



#------------------------------------------------

def simpson(
		x:Iterable, 
		y:Iterable)->float:
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
		_ct.c_double(a), 
		_ct.c_double(b), 
		_ct.c_double(tol), 
		_ct.c_int(maxiter))



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
		_ct.c_double(a), 
		_ct.c_double(b),  
		_ct.c_int(n))