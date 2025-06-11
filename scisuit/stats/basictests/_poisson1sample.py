import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p, c_bool
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_essential_poisson1sample.argtypes = [
							py_object, #sample
							py_object, #frequency
							py_object, #samplesize
							py_object, #totaloccur
							c_double,  #length
							c_bool, #hypotest
							c_double, #hyporate
							c_double, #conflevel
							c_char_p, #method
							c_char_p] #alternative
_pydll.c_stat_essential_poisson1sample.restype = py_object





@dataclass
class test_poisson1sample_Result:
	_alternative: str
	_method:str
	_hypotest:bool
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
		if self._alternative == "two.sided":
			s += f"CI = ({self.ci[0]}, {self.ci[1]})"
		else:
			s += f"CI = {max(self.ci[0],self.ci[1])}" #either one is 0.0

		if self._hypotest:
			s += "\n"
			s += f"p-value = {self.pvalue}"
			if self._method == "normal":
				s += f", z-value = {self.zvalue}"
		return s




def test_poisson1sample(
		sample: Iterable[int] | None = None,
		frequency: Iterable[int] | None = None,
		samplesize: int | None = None,
		totaloccur: int | None = None,
		length:numbers.Real = 1,
		hypotest = False,
		hyporate:numbers.Real = 0.0,
		conflevel:float = 0.95,
		method = "normal",
		alternative = "two.sided")->test_poisson1sample_Result:
	"""
	Either sample (optionally frequency) or summarized data must be provided.  

	----
	Samples known  
	sample: Sample data  
	frequency: (Optional) Number of occurences  

	----
	Summarized Data  
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

	SamplesKnown = sample != None
	SummarizedData = samplesize != None and totaloccur != None

	assert SamplesKnown or SummarizedData, "Either sample (and optionally frequency) or summarized data must be provided"

	if SamplesKnown:
		assert SummarizedData == False, "if sample is not None, then samplesize and totaloccur must be None"
	
	if SummarizedData:
		assert sample == None and frequency == None, "if samplesize is not None, then sample and frequency must be None"


	assert isinstance(conflevel, float) and (conflevel>0.0 or conflevel<1.0), "conflevel must be in range (0, 1)"
	assert isinstance(sample, Iterable | None), "sample must be Iterable|None"
	assert isinstance(frequency, Iterable | None), "frequency be Iterable|None"
	assert isinstance(samplesize, int|None), "samplesize must be int|None"
	assert isinstance(totaloccur, int|None), "totaloccur must be int|None"


	assert isinstance(length, numbers.Real) and length>0, "length must be Real and >0"
	assert isinstance(hypotest, bool), "hypotest must be bool"
	if hypotest:
		assert isinstance(hyporate, numbers.Real) and hyporate>0, "hyporate must be Real and >0"
	assert isinstance(method, str), "method must be str"
	assert isinstance(alternative, str), "alternative must be str"

	assert method in ["normal", "exact"], "method must be 'normal' or 'exact'"
	assert alternative in ["two.sided", "less", "greater"], "alternative must be 'two.sided', 'less' or 'greater'"

	dct =  _pydll.c_stat_essential_poisson1sample(
				sample,
	 			frequency,
				samplesize,
				totaloccur,
				c_double(length),
				c_bool(hypotest),
				c_double(hyporate),
				c_double(conflevel), 
				c_char_p(method.encode()),
				c_char_p(alternative.encode()))

	return test_poisson1sample_Result(
			_alternative = alternative,
			_method = method,
			_hypotest = hypotest,
			pvalue=dct["pvalue"],
			zvalue=dct["zvalue"],
			ci = (dct["CI_lower"], dct["CI_upper"]),
			mean=dct["mean"],
			N=dct["N"],
			TotalOccurences=dct["TotalOccurences"])

