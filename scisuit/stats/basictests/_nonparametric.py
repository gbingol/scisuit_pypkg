import math
import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_test_nonparam_signtest.argtypes = [py_object, c_double, c_double, c_char_p]
_pydll.c_stat_test_nonparam_signtest.restype = py_object





""" ****************  Sign-Test *********************** """


@dataclass
class test_sign_Result:
	lower:tuple[float, float, float]
	interpolated:tuple[float, float]
	upper:tuple[float, float, float]
	pvalue:float





def test_sign(
		x:Iterable, 
		md:numbers.Real,  
		alternative="two.sided", 
		conflevel=0.95)->tuple[float, test_sign_Result]:
	"""
	returns p-value and a test_sign_Result class.  

	x: Sample
	md: Median of the population tested by the null hypothesis  
	alternative: "two.sided", "less", "greater"   
	conflevel:	Confidence level, [0,1]  
	"""

	assert conflevel>0.0 or conflevel<1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"
	assert isinstance(md, numbers.Real), "md must be real number"
	assert isinstance(alternative, str), "alternative must be str"

	assert alternative in ["two.sided", "less", "greater"], "alternative must be two.sided, less or greater"

	dct =  _pydll.c_stat_test_nonparam_signtest(x, c_double(md), c_double(conflevel), c_char_p(alternative.encode()))

	return test_sign_Result(
		lower=(dct["acl1"], dct["ci1_first"], dct["ci1_second"]),
		upper=(dct["acl2"], dct["ci2_first"], dct["ci2_second"]),
		interpolated=(dct["ici_first"], dct["ici_second"]),
		pvalue=dct["pvalue"])


