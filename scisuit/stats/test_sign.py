import math
import numpy as np

from dataclasses import dataclass

from .distributions import pbinom, pnorm


__all__ = ['test_sign', 'test_sign_Result', 'CI_Result']




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
	xvec = np.sort(xvec)

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
		prob=lower,
		CILow = min(CI_a, CI_b),
		CIHigh = max(CI_a, CI_b))
	

	CI_a = xvec[upper_pos]
	CI_b = xvec[len(xvec) - upper_pos - 1]

	upperRes = CI_Result(
		pos = upper_pos,
		prob = upper,
		CILow = min(CI_a, CI_b),
		CIHigh = max(CI_a, CI_b))

	return lowerRes, upperRes





def test_sign(x, md, y=None, alternative="two.sided", conflevel=0.95):
	"""
	
	## Return
	p-value and a test_sign_Result class. \n

	## Input
	x: Sample \n
	y: Second sample \n
	md: Median of the population tested by the null hypothesis \n
	alternative: "two.sided", "less", "greater" \n
	conflevel:	Confidence level, [0,1]
	"""

	NORMALAPPROX = 12

	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, list) or type(x)==np.ndarray, "x must be list/ndarray"

	XX, YY = x, y
	if isinstance(x, list):
		XX = np.asfarray(x)
	
	assert np.issubdtype(XX.dtype, np.number), "x must contain only numbers"
	
	xvec = XX

	if y != None:
		assert isinstance(y, list) or type(y)==np.ndarray, "y must be list/ndarray"
		if isinstance(y, list):
			YY = np.asfarray(y)

		assert np.issubdtype(YY.dtype, np.number), "y must contain only numbers"
		xvec = XX - YY
	
	NGreater = len(np.argwhere(xvec>md))

	EqIndex = np.where(xvec == md)
	NEqual = len(EqIndex)
	xvec = np.delete(xvec, EqIndex)

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

	interpolated = CI_Result(pos=-1, prob=conflevel, CILow=0.0, CIHigh=0.0)
	if alternative == "two.sided" or alternative == "notequal":
		x1, x2 = Lower.prob, Upper.prob

		interpolated.CILow = np.interp(conflevel, [x1, x2], [Lower.CILow, Upper.CILow] )
		interpolated.CIHigh = np.interp(conflevel, [x1, x2], [Lower.CIHigh, Upper.CIHigh])
	
	elif alternative == "greater":
		interpolated.CILow = np.interp(conflevel, [Lower.prob, Upper.prob], [Lower.CILow, Upper.CILow])
		interpolated.CIHigh = math.inf
	
	elif alternative == "less":
		interpolated.CILow = -math.inf
		interpolated.CIHigh = np.interp(conflevel, [Lower.prob, Upper.prob], [Lower.CIHigh, Upper.CIHigh])
	
	else:
		raise ValueError("Values for 'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")

	result = test_sign_Result(
		lower= Lower,
		interpolated=interpolated,
		upper = Upper)
	
	return pvalue, result

