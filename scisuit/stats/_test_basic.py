import math
import numbers
from dataclasses import dataclass
from typing import Iterable

import numpy as _np
from ._distributions import pbinom, pf, pnorm, pt, qf, qt




""" *********** F-Test ******************* """

@dataclass
class test_f_Result:
	Fcritical:float
	df1:int; df2:int
	var1:float; var2:float
	CI_lower:float; CI_upper:float



def test_f(
		x:Iterable, 
		y:Iterable, 
		ratio:float = 1.0, 
		alternative:str = "two.sided", 
		conflevel:float = 0.95)->tuple[float, test_f_Result]:
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

	XX, YY = x, y
	if isinstance(x, list):
		XX = _np.asarray(x, dtype=_np.float64)

	if isinstance(y, list):
		YY = _np.asarray(y, dtype=_np.float64)
	
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"
	assert _np.issubdtype(YY.dtype, _np.number), "y must contain only numbers"

	alpha = 1 - conflevel
	df1, df2 = len(XX) - 1, len(YY) -1 #degrees of freedoms
	
	var1, var2 = _np.var(XX, ddof = 1), _np.var(YY, ddof = 1)
	varRatio = float(var1) / float(var2)

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
	
	result = test_f_Result(
			Fcritical= Fcritical, 
			df1=df1,
			df2=df2,
			var1 = float(var1),
			var2 = float(var2),
			CI_lower = float(CI_lower),
			CI_upper = float(CI_upper))

	return pvalue, result







""" ****************  Sign-Test *********************** """

@dataclass
class CI_Result:
	pos:int
	prob:float
	CILow:float; CIHigh:float


@dataclass
class test_sign_Result:
	lower:CI_Result
	interpolated:CI_Result
	upper:CI_Result


def _FindCI(xvec, alternative, ConfLevel):
	xvec = _np.sort(xvec)

	lower, exact, upper = 0.0, 0.0, 0.0
	lower_found, upper_found = False, False
	lower_pos, upper_ps = 0, 0
	prob = 0.0

	NSample = len(xvec)

	for i in range(NSample):
		_pbinom = pbinom(i, NSample, 0.5)

		if alternative == "two.sided" or alternative == "notequal":
			prob = 1 - 2 * _pbinom

		elif alternative == "greater":
			prob = 1 - _pbinom

		elif alternative == "less":
			prob = _pbinom


		if prob >= ConfLevel:
			upper = prob
			upper_found = True

			upper_pos = i

			if (lower_found): 
				break

		else:
			lower = prob
			lower_found = True

			lower_pos = i

			if (upper_found): 
				break

	CI_a = xvec[lower_pos]
	CI_b = xvec[len(xvec) - lower_pos - 1]

	lowerRes = CI_Result(
		pos = lower_pos,
		prob = float(lower),
		CILow = float(min(CI_a, CI_b)),
		CIHigh = float(max(CI_a, CI_b)))
	

	CI_a = xvec[upper_pos]
	CI_b = xvec[len(xvec) - upper_pos - 1]

	upperRes = CI_Result(
		pos = upper_pos,
		prob = float(upper),
		CILow = float(min(CI_a, CI_b)),
		CIHigh = float(max(CI_a, CI_b)))

	return lowerRes, upperRes





def test_sign(
		x:Iterable, 
		md:numbers.Real, 
		y=None, 
		alternative="two.sided", 
		conflevel=0.95)->tuple[float, test_sign_Result]:
	"""
	returns p-value and a test_sign_Result class. \n

	x: Sample
	y: Second sample
	md: Median of the population tested by the null hypothesis
	alternative: "two.sided", "less", "greater" 
	conflevel:	Confidence level, [0,1]
	"""

	NORMALAPPROX = 12

	assert conflevel>0.0 or conflevel<1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"

	XX = _np.asarray(x, dtype=_np.float64)
	
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"
	
	xvec = XX

	if y != None:
		assert isinstance(y, Iterable), "y must be Iterable"
		YY = _np.asarray(y, dtype=_np.float64)

		assert _np.issubdtype(YY.dtype, _np.number), "y must contain only numbers"
		xvec = XX - YY
	
	NGreater = len(_np.argwhere(xvec>md))

	EqIndex = _np.where(xvec == md)
	xvec = _np.delete(xvec, EqIndex)

	pvalue = 0.0

	NSample = len(xvec)

	if NSample < NORMALAPPROX:
		if alternative == "two.sided" or alternative == "notequal":
			n = min(NGreater, NSample - NGreater)

			#B(n, 0.5) is symmetric
			pvalue = 2.0 * pbinom(n, NSample, 0.5)

		elif alternative == "greater":
			pvalue = 1.0 - pbinom(NGreater - 1, NSample, 0.5) #area on the right

		elif alternative == "less":
			pvalue = pbinom(NGreater, NSample, 0.5); #area on the left
	
	else:
		variance = NSample / 4.0
		zvalue = (NGreater - NSample / 2.0) / math.sqrt(variance)

		if alternative == "two.sided" or alternative == "notequal":
			if zvalue <= 0:
				#area on the left + area on the right of positive
				pvalue = pnorm(zvalue, 0.0, 1.0) + (1 - pnorm(-1.0 * zvalue, 0.0, 1.0))
			else:
				#area on the right of positive + area on the left of negative
				pvalue = (1.0 - pnorm(zvalue, 0.0, 1.0)) + pnorm(-zvalue, 0.0, 1.0)
		
		elif alternative == "greater":
			#area on the right
			pvalue = (1.0 - pnorm(zvalue, 0.0, 1.0))

		elif alternative == "less":
			#area on the left
			pvalue = pnorm(zvalue, 0.0, 1.0)

	Lower, Upper = _FindCI(xvec, alternative, conflevel)

	interped = CI_Result(pos=-1, prob=conflevel, CILow=0.0, CIHigh=0.0)
	if alternative == "two.sided" or alternative == "notequal":
		x1, x2 = Lower.prob, Upper.prob

		interped.CILow = float(_np.interp(conflevel, [x1, x2], [Lower.CILow, Upper.CILow] ))
		interped.CIHigh = float(_np.interp(conflevel, [x1, x2], [Lower.CIHigh, Upper.CIHigh]))
	
	elif alternative == "greater":
		interped.CILow = float(_np.interp(conflevel, [Lower.prob, Upper.prob], [Lower.CILow, Upper.CILow]))
		interped.CIHigh = math.inf
	
	elif alternative == "less":
		interped.CILow = -math.inf
		interped.CIHigh = float(_np.interp(conflevel, [Lower.prob, Upper.prob], [Lower.CIHigh, Upper.CIHigh]))
	
	else:
		raise ValueError("Values for 'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")

	result = test_sign_Result(
		lower= Lower,
		interpolated=interped,
		upper = Upper)
	
	return pvalue, result