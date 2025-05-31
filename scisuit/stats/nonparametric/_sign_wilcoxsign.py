import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p, c_bool
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_nonparam_signtest.argtypes = [py_object, c_double, c_bool, c_double, c_char_p]
_pydll.c_stat_nonparam_signtest.restype = py_object


_pydll.c_stat_nonparam_wilcox_signedrank.argtypes = [py_object, c_double, c_bool, c_double, c_char_p]
_pydll.c_stat_nonparam_wilcox_signedrank.restype = py_object



""" ****************  Sign-Test *********************** """


@dataclass
class test_sign_Result:
	lower:None|tuple[float, float, float]
	interpolated:None|tuple[float, float]
	upper:None|tuple[float, float, float]
	pvalue:float

	def __str__(self):
		s = "Sign Test \n"
		s += f"p-value = {self.pvalue} \n"
		if self.lower != None:
			s += f"CI for {self.lower[0]*100}% = ({self.lower[1]}, {self.lower[2]}) \n"
			s += f"CI for interpolated = ({self.interpolated[0]}, {self.interpolated[1]}) \n"
			s += f"CI for {self.upper[0]*100}% = ({self.upper[1]}, {self.upper[2]})"
		return s


def test_sign(
		x:Iterable, 
		md:numbers.Real,  
		confint=True,
		alternative="two.sided", 
		conflevel=0.95)->test_sign_Result:
	"""
	returns test_sign_Result class.  

	x: Sample
	md: Median of the population tested by the null hypothesis  
	confint: Should compute confidence intervals?  
	alternative: "two.sided", "less", "greater"   
	conflevel:	Confidence level, [0,1]  
	"""

	assert conflevel>0.0 or conflevel<1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"
	assert isinstance(md, numbers.Real), "md must be real number"
	assert isinstance(confint, bool), "confint must be bool"
	assert isinstance(alternative, str), "alternative must be str"

	assert alternative in ["two.sided", "less", "greater"], "alternative must be two.sided, less or greater"

	dct =  _pydll.c_stat_nonparam_signtest(
		x, 
		c_double(md), 
		c_bool(confint), 
		c_double(conflevel), 
		c_char_p(alternative.encode()))
	
	if confint:
		return test_sign_Result(
			lower=(dct["acl1"], dct["ci1_first"], dct["ci1_second"]),
			upper=(dct["acl2"], dct["ci2_first"], dct["ci2_second"]),
			interpolated=(dct["ici_first"], dct["ici_second"]),
			pvalue=dct["pvalue"])
	
	return test_sign_Result(lower=None, upper=None, interpolated=None, pvalue=dct["pvalue"])





""" ****************  wilcox_signedrank test *********************** """


@dataclass
class test_wilcox_Result:
	acl: None|float
	ci:None|tuple[float, float]
	pvalue:float

	def __str__(self):
		s = "Wilcoxon Signed Rank Test \n"
		s += f"p-value = {self.pvalue} \n"
		if self.ci != None:
			s += f"Achieved Conf (%) = {self.acl*100} \n"
			s += f"CI = ({self.ci[0]}, {self.ci[1]})"
		return s


def test_wilcox(
		x:Iterable, 
		md:numbers.Real,  
		confint=True,
		alternative="two.sided", 
		conflevel=0.95)->test_sign_Result:
	"""
	returns test_sign_Result class.  

	x: Sample
	md: Median of the population tested by the null hypothesis  
	confint: Should compute confidence intervals?  
	alternative: "two.sided", "less", "greater"   
	conflevel:	Confidence level, [0,1]  
	"""

	assert conflevel>0.0 or conflevel<1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"
	assert isinstance(md, numbers.Real), "md must be real number"
	assert isinstance(confint, bool), "confint must be bool"
	assert isinstance(alternative, str), "alternative must be str"

	assert alternative in ["two.sided", "less", "greater"], "alternative must be two.sided, less or greater"

	dct =  _pydll.c_stat_nonparam_wilcox_signedrank(
		x, 
		c_double(md), 
		c_bool(confint), 
		c_double(conflevel), 
		c_char_p(alternative.encode()))
	
	if confint:
		return test_wilcox_Result(
			acl=dct["acl"],
			ci=(dct["ci_first"], dct["ci_second"]),
			pvalue=dct["pvalue"])
	
	return test_wilcox_Result(acl=None, ci=None, pvalue=dct["pvalue"])

