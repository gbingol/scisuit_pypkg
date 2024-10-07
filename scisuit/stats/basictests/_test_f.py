import math
from dataclasses import dataclass
from typing import Iterable

import numpy as _np
from .._distributions import pf, qf






@dataclass
class test_f_Result:
	pvalue:float
	Fvalue:float #computed value
	df1:int
	df2:int
	var1:float
	var2:float
	CI_lower:float 
	CI_upper:float
	alternative:str

	def __str__(self):
		s = "    F test for " + self.alternative + "\n"
		s += f"df1={self.df1}, df2={self.df2}, var1={self.var1}, var2={self.var2} \n"
		s += f"F={self.Fvalue} \n"
		s += f"p-value ={self.pvalue} \n"
		s += f"Confidence interval: ({self.CI_lower}, {self.CI_upper})"

		return s



def test_f(
		x:Iterable, 
		y:Iterable, 
		ratio:float = 1.0, 
		alternative:str = "two.sided", 
		conflevel:float = 0.95)->test_f_Result:
	"""
	Performs F test

	## Return
	p-value and test_f_Result class.

	## Input
	x/y: First/second sample
	alternative: "two.sided", "less", "greater"
	ratio: Assumed ratio of variances of the samples
	conflevel: Confidence level, [0,1] 
	"""
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, list) or type(x)==_np.ndarray, "x must be list/ndarray"
	assert isinstance(y, list) or type(y)==_np.ndarray, "y must be list/ndarray"

	xx, yy = x, y
	if isinstance(x, list):
		xx = _np.asarray(x, dtype=_np.float64)

	if isinstance(y, list):
		yy = _np.asarray(y, dtype=_np.float64)
	
	assert _np.issubdtype(xx.dtype, _np.number), "x must contain only numbers"
	assert _np.issubdtype(yy.dtype, _np.number), "y must contain only numbers"

	alpha = 1 - conflevel
	df1, df2 = len(xx) - 1, len(yy) -1 #degrees of freedoms
	
	var1, var2 = _np.var(xx, ddof = 1), _np.var(yy, ddof = 1)
	varRatio = float(var1) / float(var2)

	Fvalue = varRatio / ratio

	pvalue = 0.0
	if alternative == "two.sided" or alternative == "notequal":
		#F distribution is non - symmetric
		a = pf(Fvalue, df1, df2)
		b = 1 - pf(Fvalue, df1, df2)

		c = pf(1 / Fvalue, df1, df2)
		d = 1 - pf(1 / Fvalue, df1, df2)

		pvalue = min(a, b) + min(c, d)

	elif alternative == "greater":
		pvalue = (1 - pf(Fvalue, df1, df2)) #area on the right

	elif alternative == "less":
		pvalue = pf(Fvalue, df1, df2) #area on the left

	else:
		raise ValueError("Values for 'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"");


	CI_lower, CI_upper = None, None
	if alternative == "two.sided" or alternative == "notequal":
		CI1 = varRatio * qf(alpha / 2.0, df1, df2)
		CI2 = varRatio * qf(1 - alpha / 2.0, df1, df2)

		CI_lower = min(CI1, CI2)
		CI_upper = max(CI1, CI2)

	elif alternative == "greater":
		CI_lower = varRatio * qf(alpha, df1, df2)
		CI_upper = math.inf

	elif alternative == "less":
		CI_lower = -math.inf
		CI_upper = varRatio * qf(1 - alpha, df1, df2)
	
	return test_f_Result(
			pvalue=float(pvalue),
			Fvalue= Fvalue, 
			df1=df1,
			df2=df2,
			var1 = float(var1),
			var2 = float(var2),
			CI_lower = float(CI_lower),
			CI_upper = float(CI_upper),
			alternative=alternative)
