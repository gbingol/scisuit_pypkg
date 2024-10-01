import math
import numbers
from dataclasses import dataclass
from typing import Iterable

import numpy as _np
from ._distributions import pt, qt




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


def _test_t1(
		x:Iterable, 
		mu:numbers.Real, 
		alternative="two.sided", 
		conflevel=0.95)->tuple[float, test_t1_result]:
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"

	XX = _np.asarray(x, dtype=_np.float64)

	assert len(XX)>= 3, "container must have at least 3 elements"
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"

	N = len(XX)
	df = N -1
	
	stdev = _np.std(XX, ddof =1) #sample's standard deviation
	SE = stdev / math.sqrt(N) #Standard Error of Mean
	
	xaver = _np.mean(XX)
	tcritical = float((xaver - mu) / SE)

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



def _test_t2(
		x:Iterable, 
		y:Iterable, 
		mu:numbers.Real, 
		varequal = True, 
		alternative="two.sided", 
		conflevel=0.95)->tuple[float, test_t2_result]:
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"

	XX = _np.asarray(x, dtype=_np.float64)
	YY = _np.asarray(y, dtype=_np.float64)

	assert len(XX)>= 3, "x must have at least 3 elements"
	assert len(YY)>= 3, "y must have at least 3 elements"
	assert _np.issubdtype(XX.dtype, _np.number), "x must contain only numbers"
	assert _np.issubdtype(YY.dtype, _np.number), "y must contain only numbers"

	n1, n2 = len(XX), len(YY)
	xaver, yaver = float(_np.mean(XX)), float(_np.mean(YY))
	s1, s2 = float(_np.std(XX, ddof = 1)), float(_np.std(YY, ddof = 1))
	var1, var2 = s1**2, s2**2
	alpha = 1 - conflevel

	tcritical, SE = None, None
	sp = -1 #pooled

	if varequal == False:
		df_num = (var1 / n1 + var2 / n2)**2
		df_denom = 1 / (n1 - 1) * (var1 / n1)**2 + 1 / (n2 - 1) * (var2 / n2)**2
		df = math.floor(df_num / df_denom)

		tcritical = float((xaver - yaver) - mu) / math.sqrt(var1 / n1 + var2 / n2)
		SE = math.sqrt(var1 / n1 + var2 / n2)
	
	else:
		df = n1 + n2 - 2

		sp_num = (n1 - 1) * var1 + (n2 - 1) * var2
		sp = math.sqrt(sp_num / df)

		tcritical = float((xaver - yaver) - mu) / (sp * math.sqrt(1 / n1 + 1 / n2))
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


def _test_t_paired(x, y, mu, alternative="two.sided", conflevel=0.95)->tuple[float, test_tpaired_result]:
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"

	XX = x
	if isinstance(x, list):
		XX = _np.asarray(x, dtype=_np.float64)
	
	YY = y
	if isinstance(y, list):
		YY = _np.asarray(y, dtype=_np.float64)

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



def test_t (
		x:Iterable, 
		y:Iterable|None = None, 
		varequal=True, 
		alternative="two.sided", 
		mu:numbers.Real=0.0, 
		conflevel:numbers.Real=0.95, 
		paired=False ):
	"""
	Performs paired, 1-sample and 2-sample t-test

	x, y: First and second samples
	varequal: assuming equal variances
	alternative: 'two.sided', 'less' or 'greater'
	mu: Assumed difference between samples or assumed mean
	conflevel: Confidence level, [0,1]
	paired: For paired t-test
	"""
	if y == None:
		return _test_t1(x=x, mu=mu, alternative=alternative, conflevel=conflevel )	
	else:
		if paired==False:
			return _test_t2(x=x, y=y, mu=mu, varequal=varequal, alternative=alternative, conflevel=conflevel)
		else:
			return _test_t_paired(x=x, y=y, mu=mu, alternative=alternative, conflevel=conflevel)