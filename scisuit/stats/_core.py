import ctypes as _ct
import math as _math

import numpy as _np
from typing import Iterable 
from numbers import Real

from .._ctypeslib import pydll as _pydll




def kurt(y:Iterable)->float:
	"""
	Computes excess kurtosis.
	"""
	n = len(y)

	assert n >= 4, "y must have at least 4 elements"
	assert isinstance(y, Iterable), "Iterable object expected"
	
	Arr = _np.asarray(y, dtype=_np.float64)

	avg = _np.mean(Arr)
	stdev = _np.std(Arr, ddof=1)

	s = 0
	for Num in y:
		s += (Num - avg)**4

	Kurt = (s/n)/(stdev)**4 - 3

	return float(Kurt)



def mode(y:Iterable)->tuple[list[Real], int]:
	"""
	Computes mode

	Returns the most frequently occuring number(s) and 
	the number of times it occurs.
	"""
	n = len(y)

	assert n >= 3, "y must have at least 3 elements"
	assert isinstance(y, Iterable), "Iterable object expected"
	
	Arr = _np.asarray(y)

	values, counts = _np.unique(Arr, return_counts=True)
	if(len(values) == len(Arr)):
		return ([], 0)

	index = _np.argwhere(counts == _np.max(counts))

	return values[index].flatten().tolist(), int(_np.max(counts))




class rolling:

	"""
	A class to compute rolling window mean, std, var min, max...

	## Example:
	>> r = rolling(x, y, period=2) \n
	>> r.mean() \n
	>> r.var() 
	"""

     
	def __init__(
			self, 
			x:Iterable, 
			y:Iterable, 
			period:int = 2):
		assert isinstance(x, Iterable), "x must be of type Iterable"
		assert isinstance(y, Iterable), "y must be of type Iterable"
		assert isinstance(period, int), "period must be of type int"

		self._m_X, self._m_Windows = _pydll.c_stat_rolling(_ct.py_object(x), _ct.py_object(y), _ct.c_int(period))
		

	def mean(self)->list[Real]:
		"""computes mean"""
		return self.__compute(self.__mean)

	def median(self)->list[Real]:
		"""computes median"""
		return self.__compute(self.__median)
	
	def min(self)->list[Real]:
		"""computes minimum"""
		return self.__compute(min)
	
	def max(self)->list[Real]:
		"""computes maximum"""
		return self.__compute(max)
	

	def __compute(self, func)->list:
		"""
		Calls the parameter func on self._m_Windows
		Returns a 1D list containing real numbers
		"""
		return [func(v) for v in self._m_Windows]

	
	def __mean(self, lst:list):
		return sum(lst)/len(lst)

	def __median(self, arg:Iterable):
		arr = _np.asarray(arg, dtype=_np.float64)
		return float(_np.median(arr))


def moveavg(x, y, period=2)->tuple[list[Real], list[Real]]:
	"""
	Computes the moving average, similar to rolling.mean()
	returns corresponding x and mean values
	"""
	c = rolling(x,y, period)
	return x[period-1:], c.mean()





def skew(y:Iterable)->float:
	"""
	Computes the skewness of a distribution
	"""
	n = len(y)

	assert n >= 3, "y must have at least 3 elements"
	assert isinstance(y, Iterable), "Iterable object expected"
	
	Arr = _np.asarray(y)
	
	avg, std_p = float(_np.mean(Arr)), float(_np.std(Arr))

	skew_p = float(_np.sum((Arr-avg)**3))
	skew_p /= float(n * std_p**3.0)

	return _math.sqrt(n * (n - 1)) * skew_p/(n-2)