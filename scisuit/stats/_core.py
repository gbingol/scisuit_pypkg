import ctypes as _ct
import math as _math

import numpy as _np

from .._ctypeslib import pydll as _pydll




def kurt(y:_np.ndarray | list):
	"""
	Computes excess kurtosis. \n
	y: ndarray / list.
	"""
	n = len(y)

	assert n >= 4, "list/ndarray must have at least 4 elements"
	assert isinstance(y, list) or isinstance(y, _np.ndarray), "list/ndarray expected"
	
	Arr = y
	if(isinstance(y, list)):
		Arr = _np.asfarray(y)

	avg = _np.mean(Arr)
	stdev = _np.std(Arr, ddof=1)

	s = 0
	for Num in y:
		s += (Num - avg)**4

	Kurt = (s/n)/(stdev)**4 - 3

	return float(Kurt)



def mode(y:_np.ndarray | list)->tuple:
	"""
	Computes mode

	## Example
	arr = np.array([1, 3, 5, 5, 7, 9, 3, 5, 7, 3, 6])
	print(mode(y = arr))
	"""
	n = len(y)

	assert n >= 3, "list/ndarray must have at least 3 elements"
	assert isinstance(y, list) or isinstance(y, _np.ndarray), "list/ndarray expected"
	
	Arr = None
	if(isinstance(y, list)):
		Arr = _np.asarray(y)
	else:
		Arr = _np.array(y)

	values, counts = _np.unique(Arr, return_counts=True)
	if(len(values) == len(Arr)):
		return ([], 0)

	index = _np.argwhere(counts == _np.max(counts))

	return values[index].flatten().tolist(), int(_np.max(counts))




def moveavg(x, y, period=2):
	return _pydll.c_stat_moveavg(x, y, _ct.c_int(period))



class rolling:

	"""
	A class to compute rolling window mean, std, var min, max...

	## Example:
	>>r = rolling(x, y, period=2) \n
	>>r.mean() \n
	>>r.var() \n \n

	OR \n
	
	>>r=rolling(x, y, period=2).mean() \n

	If multiple calls required, prefer the first way for efficiency.

	"""

     
	def __init__(self, x:list, y:list, period:int = 2):
		assert isinstance(x, list) or isinstance(x, _np.ndarray), "x must be of type list/ndarray"
		assert isinstance(y, list) or isinstance(y, _np.ndarray), "y must be of type list/ndarray"
		assert isinstance(period, int), "period must be of type int"

		self._m_X, self._m_Windows = _pydll.c_stat_rolling(x=x, y=y, period=period)
		

	def __compute(self, func)->list:
		"""
		Calls the parameter func on self._m_Windows
		Returns a 1D list containing real numbers
		"""
		retList = []
		for Lst in self._m_Windows:
			retList.append(func(Lst))
		
		return retList
	

	def get(self):
		"""
		When mean, median, min, max member funcs do not meet the purpose.\n
		To process rolling windows data (2D list) manually. n
		get()->(list, 2D list)
		"""
		return self._m_X, self._m_Windows
	

	def mean(self):
		return self.__compute(self.__mean)

	def median(self):
		return self.__compute(self.__median)
	
	def min(self):
		return self.__compute(min)
	
	def max(self):
		return self.__compute(max)

	

	def __mean(self, lst:list):
		return sum(lst)/len(lst)

	def __median(self, arg):
		arr:_np.ndarray = arg

		if isinstance(arg, list):
			arr = _np.asfarray(arg)
		
		return float(_np.median(arr))




def skew(y:_np.ndarray | list):
	"""
	Computes the skewness of a distribution

	## Example
	y = _np.random.standard_normal(1000)
	print(skew(y))
	
	"""
	n = len(y)

	assert n >= 3, "list/ndarray must have at least 3 elements"
	assert isinstance(y, list) or isinstance(y, _np.ndarray), "list/ndarray expected"
	
	Arr = None
	if(isinstance(y, list)):
		Arr = _np.asarray(y)
	else:
		Arr = _np.array(y)
	
	avg, std_p = _np.mean(Arr), _np.std(Arr)

	skew_p = _np.sum((Arr-avg)**3)
	skew_p /= (n * std_p**3.0);

	return _math.sqrt(n * (n - 1)) * skew_p/(n-2)