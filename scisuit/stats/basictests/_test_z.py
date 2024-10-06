import math
from numbers import Real
from dataclasses import dataclass
from typing import Iterable

import numpy as _np
from .._distributions import pnorm, qnorm




@dataclass
class test_z1_Result:
	pvalue:float
	SE:float 
	stdev:float 
	mean: float 
	zvalue:float 
	CI_upper: float
	CI_lower: float
	N:int
	alternative:str

	def __str__(self)->str:
		s = f"N={self.N}, mean={self.mean}, Z={self.zvalue} \n"
		s += f"p-value = {self.pvalue} ({self.alternative}) \n"
		s += f"Confidence interval ({self.CI_lower}, {self.CI_upper}) \n"

		return s



def test_z1(
		x:Iterable, 
		sd:Real, 
		mu:Real, 
		alternative="two.sided", 
		conflevel=0.95)->test_z1_Result:
	"""
	
	## Return
	test_z1_Result class.

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
	stderr = sd / float(math.sqrt(dim))
	stdeviation = _np.std(XX, ddof =1); #sample's standard deviation

	alpha = 1 - conflevel
	zvalue = float((xaver - mu) / stderr)

	pvalue = 0.0

	if alternative == "two.sided" or alternative == "notequal":
		if zvalue <= 0:
			#area on the left of zcrit + area on the right of positive
			pvalue = pnorm(zvalue, 0.0, 1.0) + (1.0 - pnorm(abs(zvalue), 0.0, 1.0))

		elif zvalue > 0:
			#area on the right of positive zcriticial + area on the left of negative zcriticial
			pvalue = (1.0 - pnorm(zvalue, 0.0, 1.0)) + pnorm(-zvalue, 0.0, 1.0)

	elif alternative == "greater":
		pvalue = (1.0 - pnorm(zvalue, 0.0, 1.0)) #area on the right

	elif alternative == "less":
		pvalue = pnorm(zcritical, 0.0, 1.0) #area on the left

	else:
		raise ValueError("'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")
	
	if alternative == "two.sided" or alternative == "notequal":
		CI_upper = xaver - qnorm(alpha / 2.0, 0.0, 1.0) * stderr
		CI_lower = xaver + qnorm(alpha / 2.0, 0.0, 1.0) * stderr
	
	elif alternative == "greater":
		CI_upper = math.inf
		CI_lower = xaver + qnorm(alpha, 0.0, 1.0) * stderr
	
	elif alternative == "less":
		CI_upper = xaver - qnorm(alpha, 0.0, 1.0) * stderr
		CI_lower = -math.inf

	return test_z1_Result(pvalue=float(pvalue),
			SE = float(stderr), 
			stdev = float(stdeviation), 
			N = dim, 
			mean = float(xaver), 
			zvalue = zvalue,
			CI_lower = float(CI_lower),
			CI_upper = float(CI_upper),
			alternative= alternative)



#---------------------------------------------------------------------------
#---------------------------------------------------------------------------



@dataclass
class test_z2_Result:
	pvalue:float
	SE:float 
	stdev1:float 
	stdev2:float 
	mean1: float 
	mean2: float
	zvalue:float 
	CI_upper: float
	CI_lower: float
	n1:int
	n2:int
	alternative:str

	def __str__(self)->str:
		s = "    Two sample z-test    \n"
		s += f"n1={self.n1}, n2={self.n2}, mean1={self.mean1}, mean2={self.mean2} \n"
		s += f"Z={self.zvalue} \n"
		s += f"p-value = {self.pvalue} ({self.alternative}) \n"
		s += f"Confidence interval ({self.CI_lower}, {self.CI_upper}) \n"

		return s



def test_z2(
		x:Iterable, 
		y: Iterable,
		sd1:Real, 
		sd2: Real,
		mu:Real, 
		alternative="two.sided", 
		conflevel=0.95)->test_z2_Result:
	"""
	returns test_z2_Result class.

	---
	x, y: Iterable, 
	sd1, sd2: Standard deviation of population
	mu: Assumed difference between means of populations
	alternative: "two.sided", "less", "greater"
	conflevel: Confidence level, (0,1)
	"""
	assert conflevel>0.0 or conflevel<1.0, "conflevel must be in range (0, 1)"
	assert sd1 > 0 and sd2>0, "sd1 and sd2 must be >0"
	assert isinstance(x, Iterable), "x must be Iterable"
	assert isinstance(y, Iterable), "y must be Iterable"
	assert isinstance(mu, Real), "mu1 must be Real"

	xx = x
	if isinstance(x, list):
		xx = _np.asarray(x, dtype=_np.float64)
	
	yy = y
	if isinstance(y, list):
		yy = _np.asarray(y, dtype=_np.float64)

	assert len(xx)>= 3, "x must have at least 3 elements"
	assert len(yy)>= 3, "y must have at least 3 elements"
	assert _np.issubdtype(xx.dtype, _np.number), "x must contain only numbers"
	assert _np.issubdtype(yy.dtype, _np.number), "y must contain only numbers"

	n1, n2 = len(xx), len(yy)
	xaver, yaver = float(_np.mean(xx)), float(_np.mean(yy))
	stdev1, stdev2 = float(_np.std(xx, ddof =1)), float(_np.std(yy, ddof =1)) 
	stderr = math.sqrt(sd1**2/n1 + sd2**2/n2)

	alpha = 1 - conflevel
	zvalue = (xaver - yaver - mu) / stderr

	pvalue = 0.0

	if alternative == "two.sided" or alternative == "notequal":
		if zvalue <= 0:
			#area on the left of zcrit + area on the right of positive
			pvalue = pnorm(zvalue, 0.0, 1.0) + (1.0 - pnorm(abs(zvalue), 0.0, 1.0))

		elif zvalue > 0:
			#area on the right of positive zcriticial + area on the left of negative zcriticial
			pvalue = (1.0 - pnorm(zvalue, 0.0, 1.0)) + pnorm(-zvalue, 0.0, 1.0)

	elif alternative == "greater":
		pvalue = (1.0 - pnorm(zvalue, 0.0, 1.0)) #area on the right

	elif alternative == "less":
		pvalue = pnorm(zvalue, 0.0, 1.0) #area on the left

	else:
		raise ValueError("'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")
	

	if alternative == "two.sided" or alternative == "notequal":
		CI_upper = (xaver - yaver) - qnorm(alpha / 2.0, 0.0, 1.0) * stderr
		CI_lower = (xaver - yaver) + qnorm(alpha / 2.0, 0.0, 1.0) * stderr
	
	elif alternative == "greater":
		CI_upper = math.inf
		CI_lower = (xaver - yaver) + qnorm(alpha, 0.0, 1.0) * stderr
	
	elif alternative == "less":
		CI_upper = (xaver - yaver) - qnorm(alpha, 0.0, 1.0) * stderr
		CI_lower = -math.inf


	return test_z2_Result(pvalue=float(pvalue),
			SE=stderr, 
			stdev1=stdev1,
			stdev2=stdev2,
			n1=n1, 
			n2=n2,
			mean1=xaver, 
			mean2=yaver,
			zvalue = zvalue,
			CI_lower = float(CI_lower),
			CI_upper = float(CI_upper),
			alternative= alternative)



#-------------------------------------------------------------------------
#---------------------------------------------------------------------------


def test_z(
	x:Iterable, 
	sd1:Real, 
	mu:Real, 
	y:Iterable = None,
	sd2: Real = None,
	alternative="two.sided", 
	conflevel=0.95)->test_z1_Result | test_z2_Result:
	"""
	x, y: Iterable   
	sd1, sd2: Standard deviations of populations   
	mu: Assumed difference between means of populations   
	alternative: "two.sided", "less", "greater"   
	conflevel: Confidence level, (0,1)   
	"""

	if y != None:
		return test_z2(x=x, y=y, sd1=sd1, sd2=sd2, mu=mu, alternative=alternative, conflevel=conflevel)
	
	return test_z1(x=x, sd=sd1, mu=mu, alternative=alternative, conflevel=conflevel)