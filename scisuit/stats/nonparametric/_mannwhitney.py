import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p, c_bool
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_nonparam_mannwhitney.argtypes = [py_object, py_object, c_double, c_bool, c_double, c_char_p]
_pydll.c_stat_nonparam_mannwhitney.restype = py_object





@dataclass
class test_mannwhitney_Result:
	acl: None|float
	ci:None|tuple[float, float]
	pvalue:float
	U:float
	W:float
	median_xy:tuple[float, float]

	def __str__(self):
		s = "Wilcoxon Signed Rank Test \n"
		s += f"Medians: x={self.median_xy[0]}, y={self.median_xy[1]} \n"
		s += f"p-value = {self.pvalue} \n \n"
		s += f"U-statistics = {self.U} \n"
		s += f"W-statistics = {self.W} \n"
		if self.ci != None:
			s += f"Achieved Conf (%) = {self.acl*100} \n"
			s += f"CI = ({self.ci[0]}, {self.ci[1]})"
		return s


def test_mannwhitney(
		x:Iterable, 
		y:Iterable,
		md = 0.0,  
		confint=True,
		alternative="two.sided", 
		conflevel=0.95)->test_mannwhitney_Result:
	"""
	returns Mann-Whitney test class.  

	x, y: Samples  
	md: Hypothesized difference between x and y  
	confint: Should compute confidence intervals?  
	alternative: "two.sided", "less", "greater"   
	conflevel:	Confidence level, [0,1]  
	"""

	assert conflevel>0.0 or conflevel<1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"
	assert isinstance(y, Iterable), "x must be Iterable"
	assert isinstance(md, numbers.Real), "md must be real number"
	assert isinstance(confint, bool), "confint must be bool"
	assert isinstance(alternative, str), "alternative must be str"

	assert alternative in ["two.sided", "less", "greater"], "alternative must be two.sided, less or greater"

	dct =  _pydll.c_stat_nonparam_mannwhitney(
		x, 
		y,
		c_double(md), 
		c_bool(confint), 
		c_double(conflevel), 
		c_char_p(alternative.encode()))
	
	return test_mannwhitney_Result(
		acl=dct["acl"] if confint else None,
		ci=(dct["ci_first"], dct["ci_second"]) if confint else None,
		pvalue=dct["pvalue"],
		U=dct["statistics_u"],
		W=dct["statistics_w"],
		median_xy=(dct["median_x"], dct["median_y"]))
	

 