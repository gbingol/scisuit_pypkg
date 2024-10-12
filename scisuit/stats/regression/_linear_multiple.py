import math
from typing import Iterable as _Iterable

from dataclasses import dataclass
import numpy as np

from .._distributions import pf, pt, qt



@dataclass
class AnovaResults:
	DF_Residual:int
	SS_Residual:float
	MS_Residual:float
	DF_Regression:int
	SS_Regression:float
	MS_Regression:float
	SS_Total:float
	Fvalue:float
	pvalue:float
	R2:float


@dataclass
class CoeffStats:
	value:float 
	pvalue:float 
	tvalue:float 
	stderr:float 
	CILow:float 
	CIHigh:float



#-------------------------------------------------------------

def _ComputeSummary(
				yobs:np.ndarray, 
				factor:np.ndarray, 
				Coeffs, 
				ModifiedMatrix, 
				intercept=True, alpha=0.05)->tuple[float, list[CoeffStats],AnovaResults]:
	nrows, ncols = factor.shape

	MeanYObs = np.mean(yobs)
	ypredicted = np.zeros(nrows)

	SS_Total, SS_Residual = 0, 0
	sum_y2=0.0
	for i in range(nrows):
		#row vector * col vector = number
		ypredicted[i] = np.dot(ModifiedMatrix[i, :], Coeffs)
		
		SS_Total += (MeanYObs-yobs[i])**2
		SS_Residual += (yobs[i]-ypredicted[i])**2
		sum_y2 += yobs[i]**2
	
	NObservations = nrows
	DF_Regression = ncols
	DF_Residual = NObservations - (DF_Regression + 1)

	if not intercept:
		DF_Residual = NObservations - DF_Regression
		SS_Total = sum_y2
	

	SS_Regression = SS_Total - SS_Residual
	MS_Residual = SS_Residual / DF_Residual
	MS_Regression = SS_Regression/DF_Regression
	FValue = MS_Regression/MS_Residual

	pvalue = 1 - pf(float(FValue), DF_Regression, DF_Residual)

	anova = AnovaResults(
		DF_Residual=DF_Residual, 
		SS_Residual=SS_Residual,
		MS_Residual=MS_Residual,
		DF_Regression=1, 
		SS_Regression=SS_Regression, 
		MS_Regression=MS_Regression, 
		SS_Total=SS_Total,
		R2=SS_Regression/SS_Total,
		Fvalue = FValue,
		pvalue = pvalue)
	

	SEMat = np.linalg.inv(np.dot(np.transpose(ModifiedMatrix),ModifiedMatrix))
	stderror = np.sqrt(np.diag(SEMat))*math.sqrt(MS_Residual)

	CoefStatistics=[]
	for i in range(len(Coeffs)):
		Tvalue = Coeffs[i]/stderror[i]
		_pt = pt(q=float(Tvalue), df = nrows-1)
		_pvalue = float(2*(1 - _pt) if Tvalue>=0 else 2*_pt)	
		
		invTval = qt(alpha/2.0, DF_Residual)
		
		val1 = Coeffs[i] - stderror[i]*invTval
		val2 = Coeffs[i] + stderror[i]*invTval

		CoefStatistics.append(CoeffStats(
							value=float(Coeffs[i]), 
							pvalue=float(_pvalue), 
							tvalue=float(Tvalue), 
							stderr=float(stderror[i]), 
							CILow=min(val1,val2),
							CIHigh=max(val1,val2)))

	return stderror, CoefStatistics, anova




#-------------------------------------------------------

def _ComputeResiduals(yobs:np.ndarray, factor:np.ndarray, Coeffs, intercept:bool)->tuple[list, list]:
	IsIntercept = intercept

	Residuals, Fits = [], []

	NRows, NCols = factor.shape
	for i in range(NRows):
		Intercept = float(Coeffs[0]) if IsIntercept else 0.0
		fit = Intercept
		for j in range(NCols):
			Coeff = float(Coeffs[j+1]) if IsIntercept else float(Coeffs[j])
			fit += factor[i, j]*Coeff	
		
		residual = yobs[i] - fit
		
		Residuals.append(float(residual))
		Fits.append(float(fit))
	
	return Residuals, Fits



#--------------------------------------------------------------
#--------------------------------------------------------------

@dataclass
class MultipleLinRegressResult:
	Coefficients:list[float]
	CoefficientStats:list[CoeffStats]
	stderr:float
	anova:AnovaResults
	Residuals:list[float]|None
	Fits:list[float]|None
	intercept:bool
	
		
	def __str__(self):
		intercept = str(round(self.Coefficients[0], 3)) + (" + " if slope>0 else "") if self.intercept else ""

		anova = self.anova
		s = "   Multiple Linear Regression  \n"
		s += f"F={round(anova.Fvalue,2)}, p-value={round(anova.pvalue, 4)}, R2={round(anova.R2,2)} \n \n"
		s += f"The regression equation: Y = {intercept} {slope}·X  \n \n"
		s += "{:<10} {:>15} {:>15} {:>15} {:>15}\n".format(
			"Predictor", "Coeff", "StdError", "T", "p-value")
		
		if HasIntercept:
			Stat = self.CoefficientStats[1]
			s += "{:<10} {:>15.3f} {:>15.2f} {:>15.2f} {:>15.4f} \n".format(
				"Intercept", Stat.value, Stat.stderr, Stat.tvalue, Stat.pvalue)
		
		Stat = self.CoefficientStats[0]
		s += "{:<10} {:>15.3f} {:>15.2f} {:>15.2f} {:>15.4f} \n".format(
			"Slope", Stat.value, Stat.stderr, Stat.tvalue, Stat.pvalue)

		return s



def MultipleLinregress(
		yobs:np.ndarray, 
		factor:np.ndarray, 
		intercept=True, 
		alpha=0.05,
		residuals=True) -> MultipleLinRegressResult:
		assert isinstance(yobs, np.ndarray), "yobs must be of type numpy 1D array"
		assert isinstance(factor, np.ndarray), "factor must be of type numpy 2D array"

		NRows = factor.shape[0]
		assert NRows == yobs.size, "Rows of matrix == size of observed variables expected."

		modifiedMatrix = np.copy(factor)

		if intercept:
			NRows = factor.shape[0]
			ones = np.ones(NRows)
			modifiedMatrix = np.insert(modifiedMatrix, 0, values=ones, axis=1)

		coeffs = np.linalg.lstsq(modifiedMatrix, b=yobs, rcond=None)[0]

		stderror, CoefficientStats, anova = _ComputeSummary(yobs, factor, coeffs, modifiedMatrix, intercept, alpha)

		Residuals, Fits = None, None
		if residuals:
			Residuals, Fits = _ComputeResiduals(yobs, factor, coeffs, intercept)

		return MultipleLinRegressResult(
							Coefficients=coeffs,
							CoefficientStats=CoefficientStats,
							stderr=stderror, 
							anova=anova,
							intercept=intercept,
							Residuals=Residuals,
							Fits=Fits)


