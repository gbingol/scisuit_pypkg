import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p, c_bool
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_nonparam_kruskalwallis.argtypes = [py_object, py_object]
_pydll.c_stat_nonparam_kruskalwallis.restype = py_object





@dataclass
class test_kruskal_Result:
	pvalue:float
	statistic: float
	zvalues: list[float]
	counts: list[int]
	ranks: list[float]
	uniqueFactors: list[str]

	def __str__(self):
		s = "Kruskal-Wallis Test \n"
		s += f"p-value = {self.pvalue} \n"
		s += f"Statistic = {self.statistic} \n\n"

		s += "{:<10} {:>10} {:>15} {:>15} \n".format(
			"Factor", "z-value", "Rank", "Count")
		
		for i in range(len(self.uniqueFactors)):
			s += "{:<10} {:>10.2f} {:>15.2f}  {:>15}\n".format(
				self.uniqueFactors[i], 
				self.zvalues[i], 
				self.ranks[i], 
				self.counts[i])
		return s



def test_kruskal(
		responses:Iterable, 
		groups:Iterable)->test_kruskal_Result:
	"""
	returns Kruskal-Wallis test result class.  

	responses: All responses
	groups	: groups to which each response belongs
	"""

	assert isinstance(responses, Iterable), "responses must be Iterable"
	assert isinstance(groups, Iterable), "groups must be Iterable"

	dct =  _pydll.c_stat_nonparam_kruskalwallis(responses, groups)
	
	return test_kruskal_Result(
		pvalue=dct["pvalue"],
		statistic=dct["statistic"],
		zvalues=dct["zvalues"],
		counts=dct["counts"],
		ranks=dct["ranks"],
		uniqueFactors=dct["uniqueFactors"])
	

 