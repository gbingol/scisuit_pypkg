import numbers
from dataclasses import dataclass
from itertools import accumulate

from ctypes import py_object, c_bool
from ..._ctypeslib import pydll as _pydll

from ...util import to_table
from ... import settings

_pydll.c_stat_test_multivariate_cronbach.argtypes = [py_object, c_bool]
_pydll.c_stat_test_multivariate_cronbach.restype = py_object

_pydll.c_stat_test_multivariate_itemanal_squaredmultcorrel.argtypes = [py_object]
_pydll.c_stat_test_multivariate_itemanal_squaredmultcorrel.restype = py_object

_pydll.c_stat_test_multivariate_itemanal_adjtotalcorrel.argtypes = [py_object]
_pydll.c_stat_test_multivariate_itemanal_adjtotalcorrel.restype = py_object



@dataclass
class cronbach_Result:
	_labels: list[str]
	omitted: list[float]
	alpha: float
	
	
	def __OmittedItems(self):
		s = "Omitted Items \n"

		data = []
		for i, lbl in enumerate(self._labels):
			data.append([lbl, self.omitted[i]])
		
		s += to_table(data)
		return s


	def __str__(self):
		s = "Cronbach's Alpha \n"
		s += str(round(self.alpha, settings.NDIGITS)) + "\n"
		s += "\n"
		s += self.__OmittedItems()

		return s
		


def cronbach(
		Items:list[list[numbers.Real]], 
		labels:list[str] = [], 
		standardize = False)->cronbach_Result:
	"""
	Computes Cronbach's Alpha  

	---
	Items: The data section - each sublist is considered as a column of a table  
	labels: The labels of the items  
	standardize: Should standardize items' data  
	"""
	dct = _pydll.c_stat_test_multivariate_cronbach(Items, c_bool(standardize))

	ListLabels = ["Item " + str(i+1) for i in range(len(Items))] if len(labels) == 0 else labels
	assert len(ListLabels) == len(Items), "if provided labels length must be equal to number of items"
		
	return cronbach_Result(
		alpha=dct["alpha"], 
		omitted=dct["omitted"], 
		_labels = ListLabels)




def squaredmultcorrel(Items:list[list[numbers.Real]])->list[numbers.Real]:
	"""
	Computes Squared Multiple Correlations for all omitted items  

	Items: The data section - each sublist is considered as a column of a table  
	
	---
	returns a list of omitted items in the given order with the `Items` data
	"""
	return _pydll.c_stat_test_multivariate_itemanal_squaredmultcorrel(Items)



def adjtotalcorrel(Items:list[list[numbers.Real]])->list[numbers.Real]:
	"""
	Computes Item Adjusted Total Correlations for all omitted items  

	Items: The data section - each sublist is considered as a column of a table  
	
	---
	returns a list of omitted items in the given order with the `Items` data
	"""
	return _pydll.c_stat_test_multivariate_itemanal_adjtotalcorrel(Items)