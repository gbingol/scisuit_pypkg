import numbers
from dataclasses import dataclass
from typing import Iterable
from types import FunctionType

import numpy as _np

from .._ctypeslib import pydll as _pydll
from ._distributions import pnorm, psmirnov





# ----  Anderson-Darling Test -----

@dataclass
class ADTestRes:
	pvalue:float
	A2:float #test statistics


def anderson(x:Iterable)->ADTestRes:
	"""
	Performs Anderson-Darling test
	"""
	assert isinstance(x, Iterable), "x must be an Iterable object"
	
	_xx = [v for v in x if isinstance(v, numbers.Real)]
	assert len(x) == len(_xx), "x must contain only Real numbers"
	
	pval, A2 = _pydll.c_stat_test_norm_ad(x)
	return ADTestRes(pvalue=pval, A2=A2)




# ------- Kolmogorov-Smirnov Test

@dataclass
class Ks1SampletestResult:
	pvalue:float
	D:float #test statistics
	D_loc:float #location of max distance (D)
	D_sign:int
	


def ks_1samp(
		x:Iterable, 
		cdf:FunctionType=pnorm, 
		args:tuple=())->Ks1SampletestResult:
	"""
	Performs two.sided Kolmogorov-Smirnov test
	"""
	assert isinstance(x, Iterable), "x must be Iterable"

	_xx = [v for v in x if isinstance(v, numbers.Real)]
	assert len(x) == len(_xx), "x must contain only Real numbers"

	assert isinstance(cdf, FunctionType), "cdf must be a function"

	n = len(x)
	x = _np.sort(x)
	cdfvals = cdf(x, *args)
	
	dplus = (_np.arange(1.0, n + 1) / n - cdfvals)
	_plus = dplus.argmax()

	dminus = (cdfvals - _np.arange(0.0, n)/n)
	_minus = dminus.argmax()

	Dminus, dminus_loc = float(dminus[_minus]), float(x[_minus])
	Dplus, dplus_loc = float(dplus[_plus]), float(x[_plus])
	
	Dvalue = max(Dplus, Dminus)

	return Ks1SampletestResult(
					pvalue = 1-psmirnov(Dvalue, n),
					D = Dvalue, 
					D_sign = 1 if Dplus>Dminus else -1,
					D_loc = dplus_loc if Dplus>Dminus else dminus_loc)




# ----  Shapiro-Wilkinson Test -----

@dataclass
class ShapiroTestResult:
	pvalue:float
	W:float #test statistics
	msg:str #warning message, if exists


def shapiro(x:Iterable)->ShapiroTestResult:
	"""
	Performs Shapiro-Wilkinson test

	- x must be iterable containing only Real numbers
	- x must have at least length 3.
	- if len(x)>5000, W is accurate, but the p-value may not be.
	"""
	assert isinstance(x, Iterable), "x must be an Iterable object."

	N = len(x)
	if N < 3:
		raise ValueError("x must be at least length 3.")
	
	_xx = [v for v in x if isinstance(v, numbers.Real)]
	assert N == len(_xx), "x must contain only Real numbers."
	
	result = _pydll.c_stat_test_shapirowilkinson(x)
	return ShapiroTestResult(W=result[0], pvalue=result[1], msg=result[2])
