import math
import numpy as np

from . import pt, qt

from dataclasses import dataclass


__all__ = ['test_t', 'test_t1_result', 'test_t2_result', 'test_tpaired_result']



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
	assert isinstance(x, list) or type(x)==np.ndarray, "x must be list/ndarray"

	XX = x
	if isinstance(x, list):
		XX = np.asfarray(x)

	assert len(XX)>= 3, "container must have at least 3 elements"
	assert np.issubdtype(XX.dtype, np.number), "x must contain only numbers"

	N = len(XX)
	df = N -1
	
	stdev = np.std(XX, ddof =1) #sample's standard deviation
	SE = stdev / math.sqrt(N) #Standard Error of Mean
	
	xaver = np.mean(XX)
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
	assert isinstance(x, list) or type(x)==np.ndarray, "x must be list/ndarray"

	XX = x
	if isinstance(x, list):
		XX = np.asfarray(x)
	
	YY = y
	if isinstance(y, list):
		YY = np.asfarray(y)

	assert len(XX)>= 3, "x must have at least 3 elements"
	assert len(YY)>= 3, "y must have at least 3 elements"
	assert np.issubdtype(XX.dtype, np.number), "x must contain only numbers"
	assert np.issubdtype(YY.dtype, np.number), "y must contain only numbers"

	n1, n2 = len(XX), len(YY)
	xaver, yaver = np.mean(XX), np.mean(YY)
	s1, s2 = np.std(XX, ddof = 1), np.std(YY, ddof = 1)
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
	assert isinstance(x, list) or type(x)==np.ndarray, "x must be list/ndarray"

	XX = x
	if isinstance(x, list):
		XX = np.asfarray(x)
	
	YY = y
	if isinstance(y, list):
		YY = np.asfarray(y)

	assert len(XX)>= 3, "container must have at least 3 elements"
	assert np.issubdtype(XX.dtype, np.number), "x must contain only numbers"
	assert np.issubdtype(YY.dtype, np.number), "y must contain only numbers"
	assert len(XX) == len(YY), "x and y must have same size"

	xaver, yaver = np.mean(XX), np.mean(YY)
	s1, s2 = np.std(XX, ddof = 1), np.std(YY, ddof = 1)
	
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
	if y == None:
		return _test_t1(x=x, mu=mu, alternative=alternative, conflevel=conflevel )	
	else:
		if paired==False:
			return _test_t2(x=x, y=y, mu=mu, varequal=varequal, alternative=alternative, conflevel=conflevel)
		else:
			return _test_t_paired(x=x, y=y, mu=mu, alternative=alternative, conflevel=conflevel)