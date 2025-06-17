import numpy as np
from math import sqrt, log
from dataclasses import dataclass

from .._distributions import pchisq




@dataclass
class chisq_assoc_Result:
	df: int
	expected:list[int]
	raw:list[float]
	standard:list[float]
	adjusted:list[float]
	contrib:list[float]
	chisq:tuple[float, float] 
	pvalue: tuple[float, float]

	def __str__(self):
		s = "Chi-square Test \n"
		s += f"df = {self.df} \n"
		s += f"chi-sq (Pearson, Likelihood) = {[round(x, 3) for x in self.chisq]} \n"
		s += f"p-values(Pearson, Likelihood) = {[round(x, 3) for x in self.pvalue]}"
		return s

@dataclass 
class chisquare_GoodnessFit_Result:
	expected:list[int]
	contribt:list[float]
	chisq: float
	df: int
	pvalue: float
	n: int

	def __str__(self):
		s = "Chi-square Test \n"
		s += f"N = {self.n} \n"
		s += f"df = {self.df}, chi-sq = {round(self.chisq, 3)} \n"
		s += f"p-value={round(self.pvalue, 3)} \n"
		return s





def _chisq_assoc(data:list[list[int]])->chisq_assoc_Result:
	"""
	Performs Chisq Test for Association  

	data: Each sub-array should represent a column of data
	"""
	#Inputs
	Data = np.array(data, dtype=np.int64)

	num_rows, num_cols = Data.shape
	assert num_cols>1 and num_rows>1, "At least 2 by 2 entry is expected"

	df = (num_rows-1)*(num_cols - 1)

	ColSums = np.sum(Data, axis=1)
	RowSums = np.sum(Data, axis=0)
	GrandSum = np.sum(ColSums)

	ExpectedCounts:list[list[float]] = []
	RawResiduals:list[list[float]] = []
	StdResiduals:list[list[float]] = []
	AdjustResiduals:list[list[float]] = []
	ContribtoChiSq:list[list[float]] = []

	Chisq_Pearson, Chisq_Likelihood =  0.0, 0.0

	for i, rowval in enumerate(RowSums):
		ExpectedCounts.append([])
		RawResiduals.append([])
		StdResiduals.append([])
		AdjustResiduals.append([])
		ContribtoChiSq.append([])

		for j, colval in enumerate(ColSums):
			ObservedVal = int(Data[j][i])
			
			expectCnt = colval * rowval / GrandSum
			
			rawRes = ObservedVal - expectCnt
			stdRes = rawRes / sqrt(expectCnt)
			AdjRes = rawRes / sqrt(expectCnt * (1 - expectCnt / rowval) * (1 - expectCnt / colval))

			ContribChiSq = rawRes ** 2 / expectCnt

			Chisq_Pearson += ContribChiSq
			Chisq_Likelihood += ObservedVal * log(ObservedVal / expectCnt)

			ExpectedCounts[i].append(float(expectCnt))
			RawResiduals[i].append(float(rawRes))
			StdResiduals[i].append(float(stdRes))
			AdjustResiduals[i].append(float(AdjRes))
			ContribtoChiSq[i].append(float(ContribChiSq))

	Chisq_Likelihood *= 2.0

	return chisq_assoc_Result(
		expected=ExpectedCounts,
		raw=RawResiduals,
		adjusted=AdjustResiduals,
		standard=StdResiduals,
		contrib=ContribChiSq,
		chisq=(float(Chisq_Pearson), float(Chisq_Likelihood)),
		df=df,
		pvalue=(1.0-pchisq(q=Chisq_Pearson, df=df), 1.0-pchisq(q=Chisq_Likelihood, df=df))
	)




def test_chisq(
		data:list[int]|list[list[int]], 
		p:list[float] = None)->chisq_assoc_Result|chisquare_GoodnessFit_Result:
	"""
	Performs Chi-Sq Test  

	data: Either 1D or 2D list of ints  
	p: Probabilities (optional)

	---
	- If 2D list of ints are provided then p is not taken into consideration  
	- If 1D list of ints provided and p is None, then equal probabilities will be assumed
	"""
	if isinstance(data[0], list):
		return _chisq_assoc(data)
	
	proportions = p if p != None else [1/len(e) for e in data]
	assert len(p) == len(data), "data and p must have same lengths"

	Total = sum(data)
	Chisq = 0.0
	ExpectedCount:list[float] = []
	ContribChiSq: list[float] = []
	for i, v in enumerate(data):
		Expected = proportions[i]*Total
		rawResidual = v - Expected
		contribChisq = rawResidual**2/Expected

		Chisq += contribChisq
			
		ExpectedCount.append(Expected)
		ContribChiSq.append(contribChisq)

	df = len(data) - 1
	pvalue = 1.0 - pchisq(q=Chisq, df=df)

	return chisquare_GoodnessFit_Result(
		expected=ExpectedCount,
		contribt=ContribChiSq,
		chisq=Chisq, 
		df=df,
		pvalue=pvalue,
		n= Total)

