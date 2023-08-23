"""
BASIC STATISTICAL TESTS:

* Anderson-Darling Normality Test
* F-test
* Sign-Test
* t-tests (1-sample, 2-sample, paired)
* Z-test
"""


import math
import numpy as _np
from .._ctypeslib import coreDLL as _core

from dataclasses import dataclass
from .distributions import pbinom, pf, qf, pt, qt, pnorm, qnorm



__all__ = ['test_norm_ad', 'TestNormRes',
		'test_f', 'test_f_Result', 
		'test_sign', 'test_sign_Result', 'CI_Result',
		'test_t', 'test_t1_result', 'test_t2_result', 'test_tpaired_result', 
		'test_z', 'test_z_Result' ]







""" *********** Anderson-Darling Test ******************* """

@dataclass
class TestNormRes:
	pval:float
	A2:float

def test_norm_ad(x):
	pval, A2 = _core.c_stat_test_norm_ad(x)
	return TestNormRes(pval, A2)









""" *********** F-Test ******************* """

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
	assert isinstance(x, list) or type(x)==_np.ndarray, "x must be list/ndarray"
	assert isinstance(y, list) or type(y)==_np.ndarray, "y must be list/ndarray"

	XX, YY = x, y
	if isinstance(x, list):
		XX = _np.asfarray(x)

	if isinstance(y, list):
		YY = _np.asfarray(y)
	
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"
	assert _np.issubdtype(YY.dtype, _np.number), "y must contain only numbers"

	alpha = 1 - conflevel
	df1, df2 = len(XX) - 1, len(YY) -1 #degrees of freedoms
	
	var1, var2 = _np.var(XX, ddof = 1), _np.var(YY, ddof = 1)
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
	assert isinstance(x, list) or type(x)==_np.ndarray, "x must be list/ndarray"

	XX, YY = x, y
	if isinstance(x, list):
		XX = _np.asfarray(x)
	
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"
	
	xvec = XX

	if y != None:
		assert isinstance(y, list) or type(y)==_np.ndarray, "y must be list/ndarray"
		if isinstance(y, list):
			YY = _np.asfarray(y)

		assert _np.issubdtype(YY.dtype, _np.number), "y must contain only numbers"
		xvec = XX - YY
	
	NGreater = len(_np.argwhere(xvec>md))

	EqIndex = _np.where(xvec == md)
	NEqual = len(EqIndex)
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

	interpolated = CI_Result(pos=-1, prob=conflevel, CILow=0.0, CIHigh=0.0)
	if alternative == "two.sided" or alternative == "notequal":
		x1, x2 = Lower.prob, Upper.prob

		interpolated.CILow = _np.interp(conflevel, [x1, x2], [Lower.CILow, Upper.CILow] )
		interpolated.CIHigh = _np.interp(conflevel, [x1, x2], [Lower.CIHigh, Upper.CIHigh])
	
	elif alternative == "greater":
		interpolated.CILow = _np.interp(conflevel, [Lower.prob, Upper.prob], [Lower.CILow, Upper.CILow])
		interpolated.CIHigh = math.inf
	
	elif alternative == "less":
		interpolated.CILow = -math.inf
		interpolated.CIHigh = _np.interp(conflevel, [Lower.prob, Upper.prob], [Lower.CIHigh, Upper.CIHigh])
	
	else:
		raise ValueError("Values for 'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")

	result = test_sign_Result(
		lower= Lower,
		interpolated=interpolated,
		upper = Upper)
	
	return pvalue, result









""" **************   t- Test ******************* """

@dataclass
class test_t1_result:
	CI_lower:float; CI_upper:float
	SE:float
	N:int
	stdev:float
	mean: float
	tcritical:float


@dataclass
class test_t2_result:
	CI_lower:float; CI_upper:float
	tcritical:float
	n1:int; n2:int
	df:int
	xaver:float; yaver:float
	s1:float; s2:float; sp:float


@dataclass
class test_tpaired_result:
	CI_lower:float; CI_upper:float
	tcritical:float
	xaver:float; yaver:float
	s1:float; s2:float; SE:float
	N:int
	mean:float #mean of difference
	stdev:float #stdev of difference


def _test_t1(x, mu, alternative="two.sided", conflevel=0.95):
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, list) or type(x)==_np.ndarray, "x must be list/ndarray"

	XX = x
	if isinstance(x, list):
		XX = _np.asfarray(x)

	assert len(XX)>= 3, "container must have at least 3 elements"
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"

	N = len(XX)
	df = N -1
	
	stdev = _np.std(XX, ddof =1) #sample's standard deviation
	SE = stdev / math.sqrt(N) #Standard Error of Mean
	
	xaver = _np.mean(XX)
	tcritical = (xaver - mu) / SE

	pvalue = 0.0
	if alternative == "two.sided" or alternative == "notequal":
		if (tcritical <= 0.0):
			#area on the left of tcrit + area on the right of positive
			pvalue = pt(tcritical, df) + (1.0 - pt(abs(tcritical), df))
		else:
			#area on the right of positive tcritical + area on the left of negative tcritical
			pvalue = (1.0 - pt(tcritical, df)) + pt(-tcritical, df)
	
	#area on the right
	elif alternative == "greater":
		pvalue = (1.0 - pt(tcritical, df))
	
	#area on the left
	elif alternative == "less":
		pvalue = pt(tcritical, df); 

	else:
		raise ValueError("Values for 'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")
	
	alpha = 1.0 - conflevel
	CI_upper = xaver - qt(alpha / 2.0, df) * SE
	CI_lower = xaver + qt(alpha / 2.0, df) * SE

	Result = test_t1_result(
		CI_lower=CI_lower,
		CI_upper=CI_upper,
		SE = SE,
		N = N,
		stdev = stdev,
		mean = xaver,
		tcritical = tcritical)
	
	return pvalue, Result



def _test_t2(x, y, mu, varequal = True, alternative="two.sided", conflevel=0.95):
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, list) or type(x)==_np.ndarray, "x must be list/ndarray"

	XX = x
	if isinstance(x, list):
		XX = _np.asfarray(x)
	
	YY = y
	if isinstance(y, list):
		YY = _np.asfarray(y)

	assert len(XX)>= 3, "x must have at least 3 elements"
	assert len(YY)>= 3, "y must have at least 3 elements"
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"
	assert _np.issubdtype(YY.dtype, _np.number), "y must contain only numbers"

	n1, n2 = len(XX), len(YY)
	xaver, yaver = _np.mean(XX), _np.mean(YY)
	s1, s2 = _np.std(XX, ddof = 1), _np.std(YY, ddof = 1)
	var1, var2 = s1**2, s2**2
	alpha = 1 - conflevel

	tcritical, SE = None, None
	sp = -1 #pooled

	if varequal == False:
		df_num = (var1 / n1 + var2 / n2)**2
		df_denom = 1 / (n1 - 1) * (var1 / n1)**2 + 1 / (n2 - 1) * (var2 / n2)**2
		df = math.floor(df_num / df_denom)

		tcritical = ((xaver - yaver) - mu) / math.sqrt(var1 / n1 + var2 / n2)
		SE = math.sqrt(var1 / n1 + var2 / n2)
	
	else:
		df = n1 + n2 - 2

		sp_num = (n1 - 1) * var1 + (n2 - 1) * var2
		sp = math.sqrt(sp_num / df)

		tcritical = ((xaver - yaver) - mu) / (sp * math.sqrt(1 / n1 + 1 / n2))
		SE = sp * math.sqrt(1 / n1 + 1 / n2)
	
	pvalue = 0
	if alternative == "two.sided" or alternative == "notequal":
		if tcritical <= 0:
			#area on the left of tcrit + area on the right of positive
			pvalue = pt(tcritical, df) + (1 - pt(abs(tcritical), df))
		else:
			#area on the right of positive tcritical + area on the left of negative tcritical
			pvalue = (1 - pt(tcritical, df)) + pt(-tcritical, df)
	
	# area on the right
	elif alternative == "greater":	
		pvalue = 1.0 - pt(tcritical, df)
	
	# area on the left
	elif alternative == "less":	
		pvalue = pt(tcritical, df)
	
	else:
		raise ValueError("Values for 'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")
	
	quantile = qt(alpha / 2, df)

	CI1 = (xaver - yaver) - quantile * SE
	CI2 = (xaver - yaver) + quantile * SE

	CI_lower = min(CI1, CI2)
	CI_upper = max(CI1, CI2)

	Result = test_t2_result(
		CI_lower=CI_lower, CI_upper=CI_upper,
		tcritical=tcritical,
		n1 = n1, n2= n2,
		df=df,
		s1 = s1, s2=s2, sp=sp,
		xaver = xaver, yaver = yaver)
	
	return pvalue, Result


def _test_t_paired(x, y, mu, alternative="two.sided", conflevel=0.95):
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, list) or type(x)==_np.ndarray, "x must be list/ndarray"

	XX = x
	if isinstance(x, list):
		XX = _np.asfarray(x)
	
	YY = y
	if isinstance(y, list):
		YY = _np.asfarray(y)

	assert len(XX)>= 3, "container must have at least 3 elements"
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"
	assert _np.issubdtype(YY.dtype, _np.number), "y must contain only numbers"
	assert len(XX) == len(YY), "x and y must have same size"

	xaver, yaver = _np.mean(XX), _np.mean(YY)
	s1, s2 = _np.std(XX, ddof = 1), _np.std(YY, ddof = 1)
	
	Diff = XX- YY
	pvalue, Res1 = _test_t1(x =Diff, mu = mu, alternative = alternative, conflevel = conflevel)

	Result = test_tpaired_result(
		CI_lower=Res1.CI_lower,
		CI_upper = Res1.CI_upper,
		tcritical= Res1.tcritical,
		xaver=xaver,
		yaver=yaver,
		s1=s1,
		s2= s2,
		SE = Res1.SE,
		mean=Res1.mean,
		N = Res1.N,
		stdev=Res1.stdev)
	
	return pvalue, Result



def test_t (x, y = None, varequal=True, alternative="two.sided", mu=0, conflevel=0.95, paired=False ):
	"""
	Performs paired, 1-sample and 2-sample t-test
	"""
	if y == None:
		return _test_t1(x=x, mu=mu, alternative=alternative, conflevel=conflevel )	
	else:
		if paired==False:
			return _test_t2(x=x, y=y, mu=mu, varequal=varequal, alternative=alternative, conflevel=conflevel)
		else:
			return _test_t_paired(x=x, y=y, mu=mu, alternative=alternative, conflevel=conflevel)









""" ************* Z-Test ****************** """

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
	assert isinstance(x, list) or type(x)==_np.ndarray, "x must be list/ndarray"

	XX = x
	if isinstance(x, list):
		XX = _np.asfarray(x)

	assert len(XX)>= 3, "container must have at least 3 elements"
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"

	dim = len(XX)
	xaver = _np.mean(XX)
	SE = sd / math.sqrt(dim)
	stdeviation = _np.std(XX, ddof =1); #sample's standard deviation

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