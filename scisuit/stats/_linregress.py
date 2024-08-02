import math
from typing import Iterable as _Iterable

import numpy as np

from ._distributions import pf, pt, qt



__all__=['linregress', 'linregressResult']





def _FitZeroIntercept(yobs:np.ndarray, factor:np.ndarray):
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
	sum_x2 = 0
	sum_xy = 0

	assert len(yobs) == len(factor), "yobs and factor have different lengths"
	
	for i in range(len(yobs)):
		sum_x2 += factor[i]**2.0
		sum_xy += factor[i]*yobs[i]
		
	return sum_xy/sum_x2




class linregressResult:
	def __init__(self, Dict) -> None:
		self.m_Dict = Dict
      
	@property
	def R2(self)->float:
		return self.m_Dict["R2"]
	
	@property
	def stderr(self)->float:
		"""standard error"""
		return self.m_Dict["SE"]

	@property
	def pvalue(self)->float:
		"""p-value from ANOVA stat"""
		return self.m_Dict["ANOVA"]["pvalue"]
      

	@property
	def fvalue(self)->float:
		"""F-value from ANOVA stats"""
		return self.m_Dict["ANOVA"]["Fvalue"]
      

	@property
	def intercept(self)->dict|None:
		"""
		returns {coeff, pvalue, tvalue, SE, CILow, CIHigh}
		"""
		return self.m_Dict["CoefStats"][0] if len(self.m_Dict["CoefStats"])>1 else None


	@property
	def ANOVA(self)->dict:
		"""
		returns {DF_Residual, SS_Residual, MS_Residual, DF_Regression, SS_Regression, MS_Regression 
		SS_Total, Fvalue, pvalue}
		"""
		return self.m_Dict["ANOVA"]

	@property
	def coeffstat(self)->dict:
		"""
		{coeff, pvalue, tvalue, SE, CILow, CIHigh}
		"""
		return self.m_Dict["CoefStats"]





class simple_linregress:
	""" simple linear model """
      
	def __init__(self, yobs, factor, intercept=True, alpha=0.05) -> None:
		assert isinstance(yobs, np.ndarray), "yobs must be of type numpy array"
		assert isinstance(factor, np.ndarray), "factor must be of numpy array"

		self.m_yobs = yobs
		self.m_factor = factor
		self.m_intercept = intercept
		self.m_alpha = alpha
		

	def compute(self)->list[float]:
		"""
		returns [slope, [intercept]] and must be called before summary()
		"""
		if self.m_intercept:
			self.m_coeffs = np.polyfit(self.m_factor, self.m_yobs, 1)
		else:
			self.m_coeffs = np.zeros(2)
			self.m_coeffs[0] = _FitZeroIntercept(self.m_yobs, self.m_factor)
		
		return self.m_coeffs.tolist()



	def summary(self)->linregressResult:
		assert self.m_coeffs.size > 0, "compute must be called first"
		
		N = self.m_yobs.size
		assert N >= 3, "At least 3 entries must be provided"
		
		mean_x, mean_y = np.mean(self.m_factor), np.mean(self.m_yobs)
		sum_xy, sum_x2, sum_y2, sum_y, sum_x, sum_mean_x, SS_Total = 0, 0, 0, 0, 0, 0, 0

		for i in range(N):
			xi, yi = float(self.m_factor[i]), float(self.m_yobs[i])
			sum_x += xi
			sum_y += yi
			sum_x2 += xi**2
			sum_y2 += yi**2
			sum_xy += xi*yi
			sum_mean_x += (xi - mean_x)**2
			SS_Total += (yi - mean_y)**2 #total variability (SS total)


		df = N-2
		if self.m_intercept == False:
			df = N-1
			SS_Total=sum_y2
            
		#Forming the ANOVA table for regression
		fit_y = np.polyval(self.m_coeffs, self.m_factor)
		residual = self.m_yobs - fit_y

		SS_Residual = float(sum(residual**2))
		SS_Regression = SS_Total - SS_Residual
		MS_Regression, MS_Residual = SS_Regression, SS_Residual/df

		ANOVA = {
			"DF_Residual":df, "SS_Residual":SS_Residual, "MS_Residual":MS_Residual,
			"DF_Regression":1, "SS_Regression":SS_Regression, "MS_Regression":MS_Regression, 
			"SS_Total":SS_Total
			}
		
		ANOVA["Fvalue"] = float(MS_Regression/MS_Residual)
		ANOVA["pvalue"] = 1 - pf(float(MS_Regression/MS_Residual), 1, df)



		def CoeffStat(beta, SE_beta, t_beta):
			pvalue=0

			#area on the left of tcrit + area on the right of positive
			if t_beta<=0:
				pvalue = pt(q=t_beta, df=df) + (1-pt(q=abs(t_beta), df=df))
			
			#area on the right of positive tcritical + area on the left of negative tcritical
			else:
				pvalue = (1-pt(q=t_beta, df=df)) + pt(q=-t_beta, df=df) 
			

			tbl = {"coeff":beta, "pvalue":pvalue, "tvalue":t_beta, "SE":SE_beta }

			invTval = qt(self.m_alpha/2.0, ANOVA["DF_Residual"])

			val1 = beta - SE_beta*invTval
			val2 = beta + SE_beta*invTval

			tbl["CILow"] = min(val1,val2)
			tbl["CIHigh"] = max(val1,val2)

			return tbl


		#std error of population
		s = math.sqrt(MS_Residual)

		SE_beta1=s/math.sqrt(sum_mean_x)

		if(not self.m_intercept):
			SE_beta1 = s/math.sqrt(sum_x2)
		
		beta1, beta0 = float(self.m_coeffs[0]), float(self.m_coeffs[1])
		t_beta1 = beta1/SE_beta1

		tbl1 = CoeffStat(beta1, SE_beta1, t_beta1)

		CoefStats=[]

		if(self.m_intercept):
			SE_beta0 = s*math.sqrt(sum_x2)/(math.sqrt(N)*math.sqrt(sum_mean_x))
			t_beta0 = beta0/SE_beta0		
			tbl0 = CoeffStat(beta0, SE_beta0, t_beta0)

			CoefStats=[tbl0, tbl1]
		else:
			CoefStats=[tbl1]


		return linregressResult({
			"CoefStats":CoefStats, 
			"ANOVA":ANOVA, 
			"R2":SS_Regression/SS_Total, 
			"SE":s})



	def residuals(self)->tuple[list, list]:
		IsIntercept = self.m_intercept
		Coeffs = self.m_coeffs

		Residuals, Fits = [], []

		NRows = self.m_factor.shape

		for i in range(NRows):
			Intercept = float(Coeffs[0]) if IsIntercept else 0.0
			fit = Intercept
			
			Coeff = float(Coeffs[1]) if IsIntercept else float(Coeffs[0])
			fit += self.m_factor[i]*Coeff	
			
			residual = self.m_yobs[i] - fit
			
			Residuals.append(float(residual))
			Fits.append(float(fit))
		
		return Residuals, Fits





class multiple_linregress:
	"""
	multiple linear regression
	"""
	def __init__(self, yobs:np.ndarray, factor:np.ndarray, intercept=True, alpha=0.05) -> None:
		assert isinstance(yobs, np.ndarray), "yobs must be of type numpy 1D array"
		assert isinstance(factor, np.ndarray), "factor must be of type numpy 2D array"

		NRows = factor.shape[0]
		assert NRows == yobs.size, "N rows of matrix must be equal to the size of the observed variables."

		self.m_yobs = yobs
		self.m_factor = factor
		self.m_intercept = intercept
		self.m_alpha = alpha



	def compute(self)->list:
		self.m_modifiedMatrix = np.copy(self.m_factor)

		if self.m_intercept:
			NRows = self.m_factor.shape[0]
			ones = np.ones(NRows)
			self.m_modifiedMatrix = np.insert(self.m_modifiedMatrix, 0, values=ones, axis=1)

		self.m_coeffs = np.linalg.lstsq(a=self.m_modifiedMatrix, b=self.m_yobs, rcond=None)[0]
		return self.m_coeffs.tolist()



	def summary(self)->linregressResult:
		assert len(self.m_coeffs) > 0, "compute must be called first"

		nrows, ncols = self.m_factor.shape

		MeanYObs = np.mean(self.m_yobs)
		ypredicted = np.zeros(nrows)

		SS_Total, SS_Residual = 0, 0
		sum_y2=0.0
		for i in range(nrows):
			#row vector * col vector = number
			ypredicted[i] = np.dot(self.m_modifiedMatrix[i, :], self.m_coeffs)
			
			SS_Total += (MeanYObs-self.m_yobs[i])**2
			SS_Residual += (self.m_yobs[i]-ypredicted[i])**2
			sum_y2 += self.m_yobs[i]**2
		
		NObservations = nrows
		DF_Regression = ncols
		DF_Residual = NObservations - (DF_Regression + 1)

		if not self.m_intercept:
			DF_Residual = NObservations - DF_Regression
			SS_Total = sum_y2
		

		SS_Regression = SS_Total - SS_Residual
		MS_Residual = SS_Residual / DF_Residual
		MS_Regression = SS_Regression/DF_Regression
		FValue = MS_Regression/MS_Residual

		pvalue = 1 - pf(float(FValue), DF_Regression, DF_Residual)

		ANOVA = {"SS_Total":SS_Total, "SS_Residual":SS_Residual, "SS_Regression":SS_Regression,
				"DF_Regression":DF_Regression, "DF_Residual":DF_Residual, "MS_Residual":MS_Residual,
				"MS_Regression": MS_Regression, 
				"Fvalue": FValue,
				"pvalue": pvalue}
		

		SEMat = np.linalg.inv(np.dot(np.transpose(self.m_modifiedMatrix),self.m_modifiedMatrix))
		SE = np.sqrt(np.diag(SEMat))*math.sqrt(MS_Residual)

		CoefStats=[]
		for i in range(len(self.m_coeffs)):
			tbl = {}

			tbl["coeff"] = float(self.m_coeffs[i])
			tbl["SE"] = float(SE[i])
			
			Tvalue = self.m_coeffs[i]/SE[i]
			tbl["tvalue"] = float(Tvalue)

			_pt = pt(q=float(Tvalue), df = nrows-1)
			tbl["pvalue"] = float(2*(1 - _pt) if Tvalue>=0 else 2*_pt)
			
			
			invTval = qt(self.m_alpha/2.0, DF_Residual)
			
			val1 = self.m_coeffs[i] - SE[i]*invTval
			val2 = self.m_coeffs[i] + SE[i]*invTval

			tbl["CILow"] = float(min(val1,val2))
			tbl["CIHigh"] = float(max(val1,val2))

			CoefStats.append(tbl)

		return linregressResult({
			"CoefStats":CoefStats, 
			"ANOVA":ANOVA, 
			"R2":SS_Regression/SS_Total, 
			"SE":SE})



	def residuals(self)->tuple[list, list]:
		IsIntercept = self.m_intercept
		Coeffs = self.m_coeffs

		Residuals, Fits = [], []

		NRows, NCols = self.m_factor.shape
		for i in range(NRows):
			Intercept = float(Coeffs[0]) if IsIntercept else 0.0
			fit = Intercept
			for j in range(NCols):
				Coeff = float(Coeffs[j+1]) if IsIntercept else float(Coeffs[j])
				fit += self.m_factor[i, j]*Coeff	
			
			residual = self.m_yobs[i] - fit
			
			Residuals.append(float(residual))
			Fits.append(float(fit))
		
		return Residuals, Fits




def linregress(
		yobs:_Iterable, 
		factor:_Iterable | _Iterable[_Iterable], 
		intercept=True, 
		alpha=0.05)->simple_linregress|multiple_linregress:
	"""
	Performs simple/multiple linear regression

	yobs: Dependent data 
	factor: independent data
	intercept: True if there is intercept
	alpha: significance level
	"""
	Observed = np.asarray(yobs, dtype=np.float64)
	Factor = np.asarray(factor, dtype=np.float64)

	IsMatrix = len(Factor.shape) == 2
	IsVector = len(Factor.shape) == 1

	if(IsMatrix):
		return multiple_linregress(Observed, Factor, intercept, alpha)
	
	elif(IsVector):
		return simple_linregress(Observed, Factor, intercept, alpha)
	
	else:
		return TypeError("factor must be either Iterable, Iterable[Iterable]")