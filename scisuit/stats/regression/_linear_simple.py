import math

from dataclasses import dataclass
import numpy as np

from .._distributions import pf, pt, qt




def _FitZeroIntercept(yobs:np.ndarray, factor:np.ndarray)->float:
	"""
	Equation to be solved: a1.x=y1, a2.x=y2 ..... an.x=yn

	Best solution: trans(A)*A*x=trans(A)*b	where A is a matrix with first column a's and second column 0s
	trans(A)*A = a1^2+a2^2+...+an^2
	trans(A)*b = a1*b1+a2*b2+...+an*bn
	x = (trans(A)*b) / (trans(A)*A)

		Also note that (important for coefficient analysis)
	var(beta1) = var(sum(xy)/sum(x^2)) = [1/sum(x^2)]^2 * sum(x^2)*var(population)
	sd(beta1) = S(population)/sqrt(sum(x^2))

	"""
	assert len(yobs) == len(factor), "yobs and factor have different lengths"
	
	sum_x2, sum_xy = 0.0, 0.0
	for i, val in enumerate(yobs):
		sum_x2 += factor[i]**2.0
		sum_xy += factor[i]*val
		
	return float(sum_xy)/float(sum_x2)




@dataclass
class CoeffStats:
	value:float 
	pvalue:float 
	tvalue:float 
	stderr:float 
	CILow:float 
	CIHigh:float
		

def _ComputeCoeffStat(
		beta:float, 
		SE_beta:float, 
		t_beta:float, 
		alpha:float, 
		df:int)->CoeffStats:
	pvalue = 0.0

	#area on the left of tcrit + area on the right of positive
	if t_beta<=0:
		pvalue = pt(q=t_beta, df=df) + (1-pt(q=abs(t_beta), df=df))
	
	#area on the right of positive tcritical + area on the left of negative tcritical
	else:
		pvalue = (1-pt(q=t_beta, df=df)) + pt(q=-t_beta, df=df) 
	

	invTval = float(qt(alpha/2.0, df))

	val1 = beta - SE_beta*invTval
	val2 = beta + SE_beta*invTval

	return CoeffStats(
		value=beta, 
		pvalue=float(pvalue), 
		tvalue=t_beta, 
		stderr=SE_beta, 
		CILow=min(val1,val2),
		CIHigh=max(val1,val2))




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



def _ComputeSummary(yobs, factor, coeffs, intercept=True, alpha=0.05)->tuple[float, list[CoeffStats],AnovaResults]:
	NElems = yobs.size
	assert NElems >= 3, "At least 3 entries must be provided"
	
	mean_x, mean_y = float(np.mean(factor)), float(np.mean(yobs))
	sum_xy, sum_x2, sum_y2, sum_y, sum_x, sum_mean_x, SS_Total = 0, 0, 0, 0, 0, 0, 0.0

	for i in range(NElems):
		xi, yi = float(factor[i]), float(yobs[i])
		sum_x += xi
		sum_y += yi
		sum_x2 += xi**2
		sum_y2 += yi**2
		sum_xy += xi*yi
		sum_mean_x += (xi - mean_x)**2
		SS_Total += (yi - mean_y)**2 #total variability (SS total)


	df = NElems-2
	if not intercept:
		df = NElems-1
		SS_Total=sum_y2
		
	#Forming the ANOVA table for regression
	fit_y = np.polyval(coeffs, factor)
	residual = yobs - fit_y

	SS_Residual = float(sum(residual**2))
	SS_Regression = SS_Total - SS_Residual
	MS_Regression, MS_Residual = SS_Regression, SS_Residual/df

	anova = AnovaResults(
		DF_Residual=df, 
		SS_Residual=SS_Residual,
		MS_Residual=MS_Residual,
		DF_Regression=1, 
		SS_Regression=SS_Regression, 
		MS_Regression=MS_Regression, 
		SS_Total=SS_Total,
		R2=SS_Regression/SS_Total,
		Fvalue = float(MS_Regression/MS_Residual),
		pvalue = 1 - pf(float(MS_Regression/MS_Residual), 1, df))



	#std error of population
	stderror = math.sqrt(MS_Residual)

	SE_beta1 = stderror/math.sqrt(sum_mean_x)

	if not intercept:
		SE_beta1 = stderror/math.sqrt(sum_x2)
	
	beta1, beta0 = float(coeffs[0]), float(coeffs[1])
	t_beta1 = beta1/SE_beta1

	tbl1 = _ComputeCoeffStat(beta1, SE_beta1, t_beta1, alpha, df)

	CoefStats=[]

	if intercept:
		SE_beta0 = stderror*math.sqrt(sum_x2)/(math.sqrt(NElems)*math.sqrt(sum_mean_x))
		t_beta0 = beta0/SE_beta0		
		tbl0 = _ComputeCoeffStat(beta0, SE_beta0, t_beta0, alpha, df)

		CoefStats=[tbl1, tbl0]
	else:
		CoefStats=[tbl1]

	return stderror, CoefStats, anova



#-----------------------------------------------------------

def _ComputeResiduals(yobs:np.ndarray, 
					factor:np.ndarray, 
					Coeffs,
					IsIntercept=True)->tuple[list, list]:

	Residuals, Fits = [], []
	NRows=factor.shape[0]

	for i in range(NRows):
		Intercept = float(Coeffs[0]) if IsIntercept else 0.0
		fit = Intercept
		
		Coeff = float(Coeffs[1]) if IsIntercept else float(Coeffs[0])
		fit += factor[i]*Coeff	
		
		residual = yobs[i] - fit
		
		Residuals.append(float(residual))
		Fits.append(float(fit))
	
	return Residuals, Fits



#---------------------------------------------------------------------


@dataclass
class SimpleLinRegressResult:
	Coefficients:list[float]
	CoefficientStats:list[CoeffStats]
	stderr:float
	anova:AnovaResults
	Residuals:list[float]|None
	Fits:list[float]|None
	
	def GetIntercept(self)->float|None:
		HasIntercept  = len(self.Coefficients)>1
		return self.Coefficients[1] if HasIntercept else None
	
	def __str__(self):
		HasIntercept  = len(self.Coefficients)>1
		
		slope = round(self.Coefficients[0],3)
		intercept = str(round(self.Coefficients[1], 3)) + (" + " if slope>0 else "") if HasIntercept else ""

		anova = self.anova
		s = "   Simple Linear Regression  \n"
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


def SimpleLinRegress(yobs, 
				factor, 
				intercept=True, 
				alpha=0.05, 
				residuals=True) -> SimpleLinRegressResult:

	assert isinstance(yobs, np.ndarray), "yobs must be of type numpy array"
	assert isinstance(factor, np.ndarray), "factor must be of numpy array"

	if intercept:
		coeffs = np.polyfit(factor, yobs, 1)
	else:
		coeffs = np.zeros(2)
		coeffs[0] = _FitZeroIntercept(yobs, factor)
		
	stderror, CoefStats, anova = _ComputeSummary(yobs, factor, coeffs, intercept, alpha)

	Residuals, Fits = None, None
	if residuals:
		Residuals, Fits = _ComputeResiduals(yobs, factor, coeffs, intercept)

		
	return SimpleLinRegressResult(
						Coefficients=coeffs,
						CoefficientStats=CoefStats,
						anova=anova,
						stderr=stderror,
						Residuals=Residuals, 
						Fits=Fits)



	