import math
import numbers
from dataclasses import dataclass
from typing import Iterable

import numpy as _np
from ._distributions import pnorm, qnorm




@dataclass
class test_z_Result:
	pvalue:float
	SE:float 
	stdev:float 
	mean: float 
	zcritical:float 
	CI_upper: float
	CI_lower: float
	N:int
	alternative:str

	def __str__(self)->str:
		s = f"N={self.N}, mean={self.mean}, Z={self.zcritical} \n"
		s += f"p-value = {self.pvalue} ({self.alternative}) \n"
		s += f"Confidence interval ({self.CI_lower}, {self.CI_upper}) \n"

		return s


def test_z(
		x:Iterable, 
		sd:numbers.Real, 
		mu:numbers.Real, 
		alternative="two.sided", 
		conflevel=0.95)->test_z_Result:
	"""
	
	## Return
	p-value and test_z_Result class.

	## Input
	x: sample,  ndarray/list 
	sd: Standard deviation of population
	mu: Assumed mean of population
	alternative: "two.sided", "less", "greater"
	conflevel: Confidence level, (0,1)
	"""
	assert conflevel>0.0 or conflevel<1.0, "conflevel must be in range (0, 1)"
	assert sd >= 0, "sd must be >0"
	assert isinstance(x, Iterable), "x must be Iterable"

	XX = x
	if isinstance(x, list):
		XX = _np.asarray(x, dtype=_np.float64)

	assert len(XX)>= 3, "container must have at least 3 elements"
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"

	dim = len(XX)
	xaver = float(_np.mean(XX))
	SE = sd / float(math.sqrt(dim))
	stdeviation = _np.std(XX, ddof =1); #sample's standard deviation

	alpha = 1 - conflevel
	zcritical = float((xaver - mu) / SE)

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
		raise ValueError("'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")
	
	if alternative == "two.sided" or alternative == "notequal":
		CI_upper = xaver - qnorm(alpha / 2.0, 0.0, 1.0) * SE
		CI_lower = xaver + qnorm(alpha / 2.0, 0.0, 1.0) * SE
	
	elif alternative == "greater":
		CI_upper = math.inf
		CI_lower = xaver + qnorm(alpha, 0.0, 1.0) * SE
	
	elif alternative == "less":
		CI_upper = xaver - qnorm(alpha, 0.0, 1.0) * SE
		CI_lower = -math.inf

	return test_z_Result(pvalue=float(pvalue),
			SE = float(SE), 
			stdev = float(stdeviation), 
			N = dim, 
			mean = float(xaver), 
			zcritical = zcritical,
			CI_lower = float(CI_lower),
			CI_upper = float(CI_upper),
			alternative= alternative)