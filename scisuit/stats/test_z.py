import math
import numpy as np

from dataclasses import dataclass
from .distributions import pnorm, qnorm



__all__ =['test_z', 'test_z_Result']




@dataclass
class test_z_Result:
	SE:float ; stdev:float 
	mean: float 
	zcritical:float 
	CI_upper: float ; CI_lower: float
	N:int


def test_z(x, sd, mu, alternative="two.sided", conflevel=0.95):
	"""
	
	## Return
	p-value and test_z_Result class. \n

	## Input
	x: sample,  ndarray/list \n
	sd: Standard deviation of population \n
	mu: Assumed mean of population \n
	alternative: "two.sided", "less", "greater" \n
	conflevel: Confidence level, (0,1)
	"""
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert sd >= 0, "sd must be >0"
	assert isinstance(x, list) or type(x)==np.ndarray, "x must be list/ndarray"

	XX = x
	if isinstance(x, list):
		XX = np.asfarray(x)

	assert len(XX)>= 3, "container must have at least 3 elements"
	assert np.issubdtype(XX.dtype, np.number), "x must contain only numbers"

	dim = len(XX)
	xaver = np.mean(XX)
	SE = sd / math.sqrt(dim)
	stdeviation = np.std(XX, ddof =1); #sample's standard deviation

	alpha = 1 - conflevel
	zcritical = (xaver - mu) / SE

	pvalue = 0.0

	if alternative == "two.sided" or alternative == "notequal":
		if zcritical <= 0:
			#area on the left of zcrit + area on the right of positive
			pvalue = pnorm(zcritical, 0.0, 1.0) + (1.0 - pnorm(abs(zcritical), 0.0, 1.0))

		elif zcritical > 0:
			#area on the right of positive zcriticial + area on the left of negative zcriticial
			pvalue = (1.0 - pnorm(zcritical, 0.0, 1.0)) + pnorm(-zcritical, 0.0, 1.0)

		elif alternative == "greater":
			pvalue = (1.0 - pnorm(zcritical, 0.0, 1.0)) #area on the right

		elif alternative == "less":
			pvalue = pnorm(zcritical, 0.0, 1.0) #area on the left

		else:
			raise ValueError("Values for arg 'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")
	
	
	CI_upper = xaver - qnorm(alpha / 2.0, 0.0, 1.0) * SE
	CI_lower = xaver + qnorm(alpha / 2.0, 0.0, 1.0) * SE

	result = test_z_Result(SE = SE, 
			stdev = stdeviation, 
			N = dim, 
			mean = xaver, 
			zcritical = zcritical,
			CI_lower = CI_lower,
			CI_upper = CI_upper)

	return pvalue, result