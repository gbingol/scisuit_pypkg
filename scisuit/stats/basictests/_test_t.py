import math
from numbers import Real
from dataclasses import dataclass
from typing import Iterable

import numpy as _np
from .._distributions import pt, qt




@dataclass
class test_t1_result:
	pvalue:float
	CI_lower:float 
	CI_upper:float
	SE:float
	N:int
	stdev:float
	mean: float
	tvalue:float
	alternative:str="two.sided"

	def __str__(self):
		s = "    One-sample t-test for " + self.alternative + "\n"
		s += f"N={self.N}, mean={self.mean} \n"
		s += f"SE={self.SE}, t={self.tvalue} \n"
		s += f"p-value ={self.pvalue} \n"
		s += f"Confidence interval: ({self.CI_lower}, {self.CI_upper})"

		return s



def _test_t1(x:Iterable, mu:Real, alternative="two.sided", conflevel=0.95)->test_t1_result:
	
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"

	xx = _np.asarray(x, dtype=_np.float64)

	assert len(xx)>= 3, "container must have at least 3 elements"
	assert _np.issubdtype(xx.dtype, _np.number), "x must contain only numbers"

	nn = len(xx)
	df = nn -1
	
	stdev = _np.std(xx, ddof =1) #sample's standard deviation
	stderr = stdev / math.sqrt(nn) #Standard Error of Mean
	
	xaver = float(_np.mean(xx))
	tvalue = float((xaver - mu) / stderr)

	pvalue = 0.0
	if alternative == "two.sided" or alternative == "notequal":
		if (tvalue <= 0.0):
			#area on the left of tcrit + area on the right of positive
			pvalue = pt(tvalue, df) + (1.0 - pt(abs(tvalue), df))
		else:
			#area on the right of positive tvalue + area on the left of negative tvalue
			pvalue = (1.0 - pt(tvalue, df)) + pt(-tvalue, df)
	
	#area on the right
	elif alternative == "greater":
		pvalue = (1.0 - pt(tvalue, df))
	
	#area on the left
	elif alternative == "less":
		pvalue = pt(tvalue, df); 

	else:
		raise ValueError("Values for 'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")
	
	alpha = 1.0 - conflevel
	if alternative == "two.sided" or alternative == "notequal":
		CI_upper = xaver - qt(alpha / 2.0, df) * stderr
		CI_lower = xaver + qt(alpha / 2.0, df) * stderr
	elif alternative == "greater":
		CI_upper = math.inf
		CI_lower = xaver + qt(alpha, df) * stderr
	
	elif alternative == "less":
		CI_lower = -math.inf
		CI_upper = xaver - qt(alpha, df) * stderr
	

	return test_t1_result(
		pvalue=float(pvalue),
		CI_lower=float(CI_lower),
		CI_upper=float(CI_upper),
		SE = float(stderr),
		N = nn,
		stdev = float(stdev),
		mean = float(xaver),
		tvalue = float(tvalue),
		alternative=alternative)
	


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


@dataclass
class test_t2_result:
	pvalue:float
	CI_lower:float 
	CI_upper:float
	tvalue:float
	n1:int; n2:int
	df:int
	xaver:float; yaver:float
	s1:float; s2:float; sp:float
	varequal:bool
	alternative:str

	def __str__(self):
		s = "    Two-sample t-test assuming " + ("equal" if self.varequal else "unequal") + " variances \n"
		s += f"n1={self.n1}, n2={self.n2}, df={self.df} \n"
		s += f"s1={self.s1}, s2={self.s2} \n"
		if self.varequal:
			s += f"Pooled std = {self.sp} \n"
		
		s += f"t={self.tvalue} \n"
		s += f"p-value = {self.pvalue} ({self.alternative}) \n"
		s += f"Confidence interval: ({self.CI_lower}, {self.CI_upper})"

		return s



def _test_t2(
		x:Iterable, 
		y:Iterable, 
		mu:Real, 
		varequal = True, 
		alternative="two.sided", 
		conflevel=0.95)->test_t2_result:
	
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"

	xx = _np.asarray(x, dtype=_np.float64)
	yy = _np.asarray(y, dtype=_np.float64)

	assert len(xx)>= 3, "x must have at least 3 elements"
	assert len(yy)>= 3, "y must have at least 3 elements"
	assert _np.issubdtype(xx.dtype, _np.number), "x must contain only numbers"
	assert _np.issubdtype(yy.dtype, _np.number), "y must contain only numbers"

	n1, n2 = len(xx), len(yy)
	xaver, yaver = float(_np.mean(xx)), float(_np.mean(yy))
	s1, s2 = float(_np.std(xx, ddof = 1)), float(_np.std(yy, ddof = 1))
	var1, var2 = s1**2, s2**2
	alpha = 1 - conflevel

	tvalue, stderr = None, None
	sp = -1 #pooled

	if varequal == False:
		df_num = (var1 / n1 + var2 / n2)**2
		df_denom = 1 / (n1 - 1) * (var1 / n1)**2 + 1 / (n2 - 1) * (var2 / n2)**2
		df = math.floor(df_num / df_denom)

		tvalue = float((xaver - yaver) - mu) / math.sqrt(var1 / n1 + var2 / n2)
		stderr = math.sqrt(var1 / n1 + var2 / n2)
	
	else:
		df = n1 + n2 - 2

		sp_num = (n1 - 1) * var1 + (n2 - 1) * var2
		sp = math.sqrt(sp_num / df)

		tvalue = float((xaver - yaver) - mu) / (sp * math.sqrt(1 / n1 + 1 / n2))
		stderr = sp * math.sqrt(1 / n1 + 1 / n2)
	
	pvalue = 0
	if alternative == "two.sided" or alternative == "notequal":
		if tvalue <= 0:
			#area on the left of tcrit + area on the right of positive
			pvalue = pt(tvalue, df) + (1 - pt(abs(tvalue), df))
		else:
			#area on the right of positive tvalue + area on the left of negative tvalue
			pvalue = (1 - pt(tvalue, df)) + pt(-tvalue, df)
	
	# area on the right
	elif alternative == "greater":	
		pvalue = 1.0 - pt(tvalue, df)
	
	# area on the left
	elif alternative == "less":	
		pvalue = pt(tvalue, df)
	
	else:
		raise ValueError("Values for 'alternative': \"two.sided\" or \"notequal\", \"greater\", \"less\"")
	
	if alternative == "two.sided" or alternative == "notequal":
		quantile = qt(alpha / 2, df)
		conf1 = (xaver - yaver) - quantile * stderr
		conf2 = (xaver - yaver) + quantile * stderr
	
	elif alternative == "greater":
		conf1 = math.inf
		conf2 = (xaver - yaver) + qt(alpha, df) * stderr
	
	elif alternative == "less":
		conf1 = -math.inf
		conf2 = (xaver - yaver) - qt(alpha, df) * stderr
	
	CI_lower = min(conf1, conf2)
	CI_upper = max(conf1, conf2)

	return test_t2_result(
		pvalue=float(pvalue),
		CI_lower=float(CI_lower), 
		CI_upper=float(CI_upper),
		tvalue=tvalue,
		n1 = n1, 
		n2= n2,
		df=df,
		s1 = s1, 
		s2=s2, 
		sp=sp,
		xaver = xaver, 
		yaver = yaver,
		varequal=varequal,
		alternative=alternative)
	



#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

@dataclass
class test_tpaired_result:
	pvalue:float
	CI_lower:float 
	CI_upper:float
	tvalue:float
	xaver:float; yaver:float
	s1:float; s2:float; SE:float
	N:int
	mean:float #mean of difference
	stdev:float #stdev of difference
	alternative:str

	def __str__(self):
		s = "    Paired t-test for " + self.alternative + "\n"
		s += f"N={self.N}, mean1={self.xaver}, mean2={self.yaver}, mean diff={self.mean} \n"
		s += f"t={self.tvalue} \n"
		s += f"p-value ={self.pvalue} \n"
		s += f"Confidence interval: ({self.CI_lower}, {self.CI_upper})"

		return s


def _test_t_paired(x, y, mu, alternative="two.sided", conflevel=0.95)-> test_tpaired_result:
	assert conflevel>=0.0 or conflevel <= 1.0, "conflevel must be in range (0, 1)"
	assert isinstance(x, Iterable), "x must be Iterable"

	xx = x
	if isinstance(x, list):
		xx = _np.asarray(x, dtype=_np.float64)
	
	yy = y
	if isinstance(y, list):
		yy = _np.asarray(y, dtype=_np.float64)

	assert len(xx)>= 3, "container must have at least 3 elements"
	assert _np.issubdtype(xx.dtype, _np.number), "x must contain only numbers"
	assert _np.issubdtype(yy.dtype, _np.number), "y must contain only numbers"
	assert len(xx) == len(yy), "x and y must have same size"

	xaver, yaver = _np.mean(xx), _np.mean(yy)
	s1, s2 = _np.std(xx, ddof = 1), _np.std(yy, ddof = 1)
	
	Diff = xx- yy
	Res1 = _test_t1(x =Diff, mu = mu, alternative = alternative, conflevel = conflevel)

	return test_tpaired_result(
		pvalue=Res1.pvalue,
		CI_lower=Res1.CI_lower,
		CI_upper = Res1.CI_upper,
		tvalue= Res1.tvalue,
		xaver=xaver,
		yaver=yaver,
		s1=s1,
		s2= s2,
		SE = Res1.SE,
		mean=Res1.mean,
		N = Res1.N,
		stdev=Res1.stdev,
		alternative=Res1.alternative)



#---------------------------------------------------------------
#---------------------------------------------------------------


def test_t (
		x:Iterable, 
		y:Iterable|None = None, 
		varequal=True, 
		alternative="two.sided", 
		mu:Real=0.0, 
		conflevel:Real=0.95, 
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