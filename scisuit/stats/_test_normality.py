import numbers
from dataclasses import dataclass
from typing import Iterable

import numpy as _np

from .._ctypeslib import pydll as _pydll
from ._distributions import pnorm, psmirnov





# ----  Anderson-Darling Test -----

@dataclass
class ADTestRes:
	pvalue:float
	A2:float


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
	D:float #test statistic
	pvalue:float
	D_loc:float #location of max distance (D)
	D_sign:int
	


def ks_1samp(x:Iterable)->Ks1SampletestResult:
	"""
	Performs two.sided Kolmogorov-Smirnov test

	Note: By default, the CDF values are generated using pnorm function.
	"""
	assert isinstance(x, Iterable), "x must be Iterable"

	_xx = [v for v in x if isinstance(v, numbers.Real)]
	assert len(x) == len(_xx), "x must contain only Real numbers"

	n = len(x)
	x = _np.sort(x)
	cdfvals = pnorm(x)
	
	dplus = (_np.arange(1.0, n + 1) / n - cdfvals)
	_plus = dplus.argmax()

	dminus = (cdfvals - _np.arange(0.0, n)/n)
	_minus = dminus.argmax()

	Dminus, dminus_loc = float(dminus[_minus]), float(x[_minus])
	Dplus, dplus_loc = float(dplus[_plus]), float(x[_plus])
	
	Dvalue = max(Dplus, Dminus)

	return Ks1SampletestResult(
					D = Dvalue, 
					pvalue = 1-psmirnov(Dvalue, n),
					D_sign = 1 if Dplus>Dminus else -1,
					D_loc = dplus_loc if Dplus>Dminus else dminus_loc)
