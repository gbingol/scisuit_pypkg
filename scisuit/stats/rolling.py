from .._ctypeslib import coreDLL as _core

import numpy as np


__all__ = ['rolling']


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
		assert isinstance(x, list) or isinstance(x, np.ndarray), "x must be of type list/ndarray"
		assert isinstance(y, list) or isinstance(y, np.ndarray), "y must be of type list/ndarray"
		assert isinstance(period, int), "period must be of type int"

		self._m_X, self._m_Windows = _core.c_stat_rolling(x=x, y=y, period=period)
		

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
		arr:np.ndarray = arg

		if isinstance(arg, list):
			arr = np.asfarray(arg)
		
		return float(np.median(arr))


	