import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p, c_bool
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_nonparam_friedman.argtypes = [py_object, py_object, py_object]
_pydll.c_stat_nonparam_friedman.restype = py_object





@dataclass
class test_friedman_Result:
	pvalue:float
	statistic: float
	
	counts:list[int] #counts of each factors
	medians:list[float]

	quantile_25:list[float] 
	quantile_75:list[float]

	#Note that ranksums are ordered in the order of uniqueFactors
	ranksums:list[float]
	uniqueFactors:list[str]

	def __str__(self):
		s = "Friedman Test \n"
		s += f"p-value = {self.pvalue} \n"
		s += f"Statistic = {self.statistic} \n\n"

		s += "{:<10} {:>10} {:>15} {:>15} {:>15} {:>15} \n".format(
			"Factor", "25%", "Median", "75%", "Ranksum", "Count")
		
		for i in range(len(self.uniqueFactors)):
			s += "{:<10} {:>10.2f} {:>15.2f} {:>15.2f} {:>15.2f} {:>15}\n".format(
				self.uniqueFactors[i], 
				self.quantile_25[i],
				self.medians[i],
				self.quantile_75[i],
				self.ranksums[i], 
				self.counts[i])
		return s



def test_friedman(
		responses:Iterable, 
		factors: Iterable,
		groups:Iterable)->test_friedman_Result:
	"""
	returns Friedman test result class.  

	responses: All responses
	factors: Factor level for the response
	groups	: groups to which each response belongs
	"""

	assert isinstance(responses, Iterable), "responses must be Iterable"
	assert isinstance(factors, Iterable), "groups must be Iterable"
	assert isinstance(groups, Iterable), "groups must be Iterable"

	dct =  _pydll.c_stat_nonparam_friedman(responses,factors, groups)
	
	return test_friedman_Result(
		pvalue=dct["pvalue"],
		statistic=dct["statistic"],
		counts=dct["counts"],
		quantile_25=dct["quantile_25"],
		medians=dct["medians"],
		quantile_75=dct["quantile_75"],
		ranksums=dct["ranksums"],
		uniqueFactors=dct["uniqueFactors"])
	

 