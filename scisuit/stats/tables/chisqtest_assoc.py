import numpy as np
from math import sqrt, log
from dataclasses import dataclass

from scisuit.stats import pchisq




@dataclass
class chisq_assoc_Result:
	df: int
	ExpectedCounts:list[int]
	RawResiduals:list[float]
	StdResiduals:list[float]
	AdjustResiduals:list[float]
	ContribtoChiSq:list[float]
	chisq:tuple[float, float] 
	pvalue: tuple[float, float]




def chisq_assoc(data:list[list[int]])->chisq_assoc_Result:
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
		ExpectedCounts=ExpectedCounts,
		RawResiduals=RawResiduals,
		AdjustResiduals=AdjustResiduals,
		StdResiduals=StdResiduals,
		ContribtoChiSq=ContribChiSq,
		chisq=(Chisq_Pearson, Chisq_Likelihood),
		df=df,
		pvalue=(1.0-pchisq(q=Chisq_Pearson, df=df), 1.0-pchisq(q=Chisq_Likelihood, df=df))
	)