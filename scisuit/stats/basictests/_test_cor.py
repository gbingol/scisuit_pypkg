import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_essential_correlation.argtypes = [py_object, py_object, c_double, c_char_p]
_pydll.c_stat_essential_correlation.restype = py_object





@dataclass
class cortest_Result:
	coeff: float
	ci:tuple[float, float]

	def __str__(self):
		s = f"Correlation coefficient = {self.coeff} \n"
		s += f"CI = ({self.ci[0]}, {self.ci[1]})"
		return s

def cor_test(
		x:Iterable, 
		y:Iterable,
		conflevel=0.95,
		method="pearson")->cortest_Result:
	"""
	returns coefficient and confidence interval.  

	x, y: x and y data  
	conflevel:	Confidence level, [0,1]  
	method: correlation method, "pearson" or "spearman"
	"""

	assert conflevel>0.0 or conflevel<1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"
	assert isinstance(y, Iterable), "ymust be Iterable"
	assert isinstance(method, str), "method must be str"

	assert method in ["pearson", "spearman"], "method must be 'pearson' or 'spearman'"

	retObj =  _pydll.c_stat_essential_correlation(x, y, c_double(conflevel), c_char_p(method.encode()))

	return cortest_Result(coeff=retObj[0], ci=(retObj[1], retObj[2]))


