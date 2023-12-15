import numpy as _np
import math as _math
import numbers as _numbers
from ._ctypeslib import pydll as _pydll
import ctypes as _ct
import types as _types
from typing import Iterable

def trapz(x:list|_np.ndarray, y:list|_np.ndarray)->float:
    """
    Computes area using trapezoidal method and uses Numpy's trapz method.

    ## Input: 
    x, y: list or ndarray
    """
    return _np.trapz(x=x, y=y)



def cumtrapz(x:list|_np.ndarray, y:list|_np.ndarray)->list:
	"""
	Computes the left-tailed cumulative area

	##Input:
	x, y: list or ndarray
	"""
	val = 0.0
	a, b, f_a, f_b = 0.0, 0.0, 0.0, 0.0
	retList =[0.0]

	for i in range(len(x)-1):
		a = x[i]
		b = x[i + 1]

		if _math.isclose(b, a, abs_tol = 1E-5):
			raise ValueError("|X(i+1)-X(i)|<1E-5")

		if (b < a):
			raise ValueError("X(i+1) > X(i) expected.")

		f_a = y[i]
		f_b = y[i + 1]

		val += (b - a) * (f_a + f_b) / 2.0

		retList.append(val)
	
	return retList


def simpson(x:Iterable, y:Iterable)->float:
	"""
	Uses simpson's method (1/3 and 3/8)

	#Input:
	x,y: Iterable
	"""

	return _pydll.c_integ_simpson(x, y)


def romberg(f:_types.FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100)->float:
	"""
	Romberg integration

	#Input:
	f: Univariate function \n
	a, b: limits of integration (b>a) \n
	tol:	tolerance for error \n
	maxiter: Maximum number of iterations
	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"

	return _pydll.c_integ_romberg(
		f, 
		_ct.c_double(a), 
		_ct.c_double(b), 
		_ct.c_double(tol), 
		_ct.c_int(maxiter))


def fixed_quad(f:_types.FunctionType, 
	a:float, 
	b:float, 
	n:int=5)->float:
	"""
	Computes a definite integral using fixed-order Gaussian quadrature.

	#Input:
	f: Univariate function \n
	a, b: limits of integration (b>a) \n
	n: Order of quadrature integration (2<=n<=6)
	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"
	assert isinstance(n, _numbers.Integral, "n must be int")

	return _pydll.c_integ_fixed_quad(
		f, 
		_ct.c_double(a), 
		_ct.c_double(b),  
		_ct.c_int(n))