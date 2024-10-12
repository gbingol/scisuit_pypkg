import numpy as np
from typing import Iterable 
from ._linear_simple import SimpleLinRegress, SimpleLinRegressResult
from ._linear_multiple import MultipleLinregress, MultipleLinRegressResult




def linregress(
		yobs:Iterable, 
		factor:Iterable | Iterable[Iterable], 
		intercept=True, 
		alpha=0.05,
		residuals = True)->SimpleLinRegressResult|MultipleLinRegressResult:
	"""
	Performs simple/multiple linear regression

	yobs: Dependent data  
	factor: independent data   
	intercept: True if there is intercept   
	alpha: significance level   
	residuals: Compute residuals and fits (otherwise None is returned)
	"""
	Observed = np.asarray(yobs, dtype=np.float64)
	Factor = np.asarray(factor, dtype=np.float64)

	IsMatrix = len(Factor.shape) == 2
	IsVector = len(Factor.shape) == 1

	if(IsMatrix):
		return MultipleLinregress(yobs=Observed, factor=np.transpose(Factor), intercept=intercept, alpha=alpha, residuals=residuals)
	
	elif(IsVector):
		return SimpleLinRegress(yobs=Observed, factor=Factor, intercept=intercept, alpha=alpha, residuals=residuals)
	
	else:
		return TypeError("factor must be either Iterable, Iterable[Iterable]")