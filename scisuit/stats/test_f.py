import numpy as np

from dataclasses import dataclass
from . import pf, qf



__all__ = ['test_f', 'test_f_Result']



@dataclass
class test_f_Result:
	Fcritical:float
	df1:int; df2:int
	var1:float; var2:float
	CI_lower:float; CI_upper:float



def test_f(x, y, alternative:str = "two.sided", ratio:float = 1.0, conflevel:float = 0.95)->tuple:
	"""
	Performs F test

	## Return
	p-value and test_f_Result class. \n

	## Input
	x/y: First/second sample, ndarray/list \n
	alternative: "two.sided", "less", "greater" \n
	ratio: Assumed ratio of variances of the samples \n
	conflevel: Confidence level, [0,1] 
	"""
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, list) or type(x)==np.ndarray, "x must be list/ndarray"
	assert isinstance(y, list) or type(y)==np.ndarray, "y must be list/ndarray"

	XX, YY = x, y
	if isinstance(x, list):
		XX = np.asfarray(x)

	if isinstance(y, list):
		YY = np.asfarray(y)
	
	assert np.issubdtype(XX.dtype, np.number), "x must contain only numbers"
	assert np.issubdtype(YY.dtype, np.number), "y must contain only numbers"

	alpha = 1 - conflevel
	df1, df2 = len(XX) - 1, len(YY) -1 #degrees of freedoms
	
	var1, var2 = np.var(XX, ddof = 1), np.var(YY, ddof = 1)
	varRatio = var1 / var2

	Fcritical = varRatio / ratio

	pvalue = 0.0

	if alternative == "two.sided" or alternative == "notequal":
		#F distribution is non - symmetric
		a = pf(Fcritical, df1, df2)
		b = 1 - pf(Fcritical, df1, df2)

		c = pf(1 / Fcritical, df1, df2)
		d = 1 - pf(1 / Fcritical, df1, df2)

		pvalue = min(a, b) + min(c, d)

	elif alternative == "greater":
		pvalue = (1 - pf(Fcritical, df1, df2)) #area on the right

	elif alternative == "less":
		pvalue = pf(Fcritical, df1, df2) #area on the left

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

	elif alternative == "less":
		CI_upper = varRatio * qf(1 - alpha, df1, df2)
	
	result = test_f_Result(Fcritical= Fcritical, 
			df1=df1,
			df2=df2,
			var1=var1,
			var2=var2,
			CI_lower=CI_lower,
			CI_upper=CI_upper)

	return pvalue, result