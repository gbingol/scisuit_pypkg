import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p, c_bool
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_nonparam_kruskalwallis.argtypes = [py_object, py_object]
_pydll.c_stat_nonparam_kruskalwallis.restype = py_object





@dataclass
class test_kruskal_Result:
	acl: None|float
	ci:None|tuple[float, float]
	pvalue:float
	U:float
	W:float
	median_xy:tuple[float, float]

	def __str__(self):
		s = "Kruskal-Wallis Test \n"
		s += f"Medians: x={self.median_xy[0]}, y={self.median_xy[1]} \n"
		s += f"p-value = {self.pvalue} \n \n"
		s += f"U-statistics = {self.U} \n"
		s += f"W-statistics = {self.W} \n"
		if self.ci != None:
			s += f"Achieved Conf (%) = {self.acl*100} \n"
			s += f"CI = ({self.ci[0]}, {self.ci[1]})"
		return s


def test_kruskal(
		responses:Iterable, 
		groups:Iterable)->test_kruskal_Result:
	"""
	returns Kruskal-Wallis test result class.  

	responses: All responses
	groups	: groups to which each response belongs
	"""

	assert isinstance(responses, Iterable), "x must be Iterable"
	assert isinstance(groups, Iterable), "x must be Iterable"

	dct =  _pydll.c_stat_nonparam_mannwhitney(groups, responses)
	
	return test_kruskal_Result(
		acl=dct["acl"] if confint else None,
		ci=(dct["ci_first"], dct["ci_second"]) if confint else None,
		pvalue=dct["pvalue"],
		U=dct["statistics_u"],
		W=dct["statistics_w"],
		median_xy=(dct["median_x"], dct["median_y"]))
	

 