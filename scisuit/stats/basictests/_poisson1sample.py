import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_essential_correlation.argtypes = [py_object, py_object, c_double, c_char_p]
_pydll.c_stat_essential_correlation.restype = py_object





@dataclass
class test_poisson1sample_Result:
	_method:str
	pvalue: float | None
	zvalue: float | None
	mean: float
	ci : tuple[float, float]
	N: int
	TotalOccurences: int

	def __str__(self):
		s = "One Sample Poisson Test (" + self._method + ") \n"
		s += f"N = {self.N}, Total Occurences = {self.TotalOccurences} \n"
		s += f"Mean = {self.mean} \n"
		s += f"CI = ({self.ci[0]}, {self.ci[1]})"

		if self.pvalue != None:
			s += "\n"
			s += f"p-value = {self.pvalue}"
			if self.zvalue != None:
				s += f", z-value = {self.zvalue}"
		return s

def test_poisson1sample(
		sample: Iterable[int] | None,
		frequency: Iterable[int] | None,
		samplesize: int | None,
		totaloccur: int | None,
		length = 1,
		hypotest = False,
		hyporate = 0.0,
		conflevel = 0.95,
		method = "normal",
		alternative = "two.sided")->test_poisson1sample_Result:
	"""
	Either sample (optionally frequency) or samplesize and totaloccur must be provided.  

	sample: Sample data  
	frequency: (Optional) Number of occurences  
	SampleSize: Size of the sample  
	totaloccur: Number of total occurences (generally sample size [i] * frequency [i])

	----
	length: Length of observation (time, area, etc.)  
	hypotest: Should perform hypothesis test
	hyporate: Hypothesis rate
	conflevel: Confidence level, [0,1]  
	method: "normal" or "exact"
	alternative: "two.sided", "less" or "greater"
	"""

	assert conflevel>0.0 or conflevel<1.0, "conflevel must be in range (0, 1)"
	assert isinstance(sample, Iterable | None), "sample must be Iterable|None"
	assert isinstance(frequency, Iterable | None), "frequency be Iterable|None"
	assert isinstance(samplesize, int|None), "samplesize must be int|None"
	assert isinstance(totaloccur, int|None), "totaloccur must be int|None"


	assert isinstance(length, float) and length>0, "length must be float and >0"
	assert isinstance(hypotest, bool), "hypotest must be bool"
	assert isinstance(hyporate, float) and hyporate>0, "hyporate must be float and >0"
	assert isinstance(method, str), "method must be str"
	assert isinstance(alternative, str), "alternative must be str"

	assert method in ["normal", "exact"], "method must be 'normal' or 'exact'"
	assert alternative in ["two.sided", "less", "r"], "alternative must be 'two.sided', 'less' or 'greater'"

	retObj =  _pydll.c_stat_essential_correlation(x, y, c_double(conflevel), c_char_p(method.encode()))

	return cortest_Result(coeff=retObj[0], ci=(retObj[1], retObj[2]))

