import math
import numbers
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ._qdist import qdist
from .._distributions import pf

__all__ = ['aov','aov_results']




@dataclass
class aov_results:
	Treat_DF:int
	Treat_SS:float
	Treat_MS:float
	Error_DF:int
	Error_SS:float
	Error_MS:float
	Total_DF:int
	Total_SS:float
	Total_MS:float
	Fvalue:float
	pvalue:float

	#For tukey test
	Averages:list
	SampleSizes:list

	def __str__(self):
		s = "    One-Way ANOVA Results \n"
		s += "{:<10} {:>10} {:>15} {:>15} {:>15} {:>15}\n".format(
			"Source", "df", "SS", "MS", "F", "p-value")
		
		s += "{:<10} {:>10} {:>15.2f} {:>15.2f} {:>15.2f} {:>15.4e}\n".format(
			"Treatment", self.Treat_DF, self.Treat_SS, self.Treat_MS, self.Fvalue, self.pvalue)
		
		s += "{:<10} {:>10} {:>15.2f} {:>15.2f}\n".format(
			"Error", self.Error_DF, self.Error_SS, self.Error_MS)
		
		s += "{:<10} {:>10} {:>15.2f}\n".format("Total", self.Total_DF, self.Total_SS)

		return s





def aov(*args)->aov_results:
	Averages, SampleSizes = [], []
	MSError, DFTreatment, DFError = None, None, None
	SS_Treatment, SS_Error, SS_Total=0, 0, 0
	NEntries = 0

	#C is a variable defined to speed up computations (see Larsen Marx Chapter 12 on ANOVA)
	_c = 0.0

	for elem in args:
		if(not isinstance(elem, Iterable)):
			raise TypeError("Iterable's expected")

		ElemSize = len(elem)
		LocalSum = 0.0
		
		for entry in elem:
			LocalSum += entry
			SS_Total += entry**2
		
		#Required for Tukey test
		Averages.append(LocalSum/ElemSize)
		SampleSizes.append(ElemSize) 

		_c += LocalSum
		NEntries += ElemSize
		SS_Treatment += LocalSum**2/ElemSize

		
	_c = _c**2 / NEntries
	
	SS_Total = SS_Total - _c
	SS_Treatment = SS_Treatment - _c
	SS_Error = SS_Total - SS_Treatment

	DFError, DFTreatment = NEntries-len(args), len(args)-1 
	DF_Total = DFError + DFTreatment

	MS_Treatment, MSError = SS_Treatment/DFTreatment , SS_Error/DFError

	Fvalue = MS_Treatment/MSError
	pvalue = 1 - pf(q = float(Fvalue), df1 = DFTreatment, df2 = DFError)

	return aov_results(
		Treat_DF=DFTreatment,
		Treat_MS = float(MS_Treatment),
		Treat_SS = float(SS_Treatment),

		Error_DF=DFError,
		Error_SS = float(SS_Error),
		Error_MS = float(MSError),
		Total_DF=DF_Total,

		Total_SS = float(SS_Total),
		Total_MS = float(SS_Total/DF_Total),
		
		Fvalue = float(Fvalue),
		pvalue=pvalue,

		#For tukey test
		Averages=Averages,
		SampleSizes=SampleSizes	)



@dataclass
class TukeyComparison:
	a:int
	b:int
	Diff:float #differences in mean values
	CILow:float
	CIHigh:float

	def __str__(self) -> str: 
		s1 = f"{self.a+1} - {self.b+1}"
		s2 = f"({round(self.CILow, 2)}, {round(self.CIHigh, 2)})"
		return "{:<10} {:>15.2f} {:>25}".format(s1, self.Diff, s2)


@dataclass
class TukeyResults:
	r:list[TukeyComparison]
	alpha:float

	def __str__(self):
		s = f"   Tukey Test Results (alpha={self.alpha}) \n\n"
		s += "{:<10} {:>15} {:>20} \n".format("Pairwise Diff", "i-j" ,"Interval")
		for l in self.r:
			s += str(l) + "\n"
		return s


	

def tukey(alpha:float, aovresult:aov_results)->TukeyResults:
	"""perform tukey test"""	
	assert isinstance(alpha, float), "alpha must be float."
	assert isinstance(aovresult, aov_results), "aovresult must be aov_results."

	Averages, SampleSizes = aovresult.Averages, aovresult.SampleSizes
	Treat_DF, Error_DF = aovresult.Treat_DF, aovresult.Error_DF
	Error_MS = aovresult.Error_MS

	Dvalue = qdist(1-alpha, Treat_DF-1, Error_DF-1) / math.sqrt(SampleSizes[0])
	L_Conf = Dvalue*math.sqrt(Error_MS) #length of confidence interval

	TukeyTable = []
	nn = len(Averages)
	for i in range(nn):
		for j in range(i+1, nn):
			Diff = Averages[i]-Averages[j]
			Conf1 = Diff - L_Conf
			Conf2 = Diff + L_Conf

			comp = TukeyComparison(
			a=i, 
			b = j,
			Diff=Diff,
			CILow = min(Conf1, Conf2),
			CIHigh = max(Conf1,Conf2))

			TukeyTable.append(comp)

	return TukeyResults(r=TukeyTable, alpha=alpha)
