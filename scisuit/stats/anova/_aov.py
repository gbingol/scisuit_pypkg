import math
import numbers
from dataclasses import dataclass

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



class aov: 

	class TukeyComparison:
		def __init__(self) -> None:
			self.m_a=None
			self.m_b=None
			self.m_MeanValueDiff=None
			self.m_CILow=None
			self.m_CIHigh=None

		def __str__(self) -> str: 
			retStr = str(self.m_a) + "-" + str(self.m_b) + \
				"\t \t" + \
				str(round(self.m_MeanValueDiff, 2)) + \
				"\t \t" + \
				str(round(self.m_CILow, 2)) + \
				"," \
				+ str(round(self.m_CIHigh, 2))
			return retStr


	def __init__(self, *args) -> None:
		self._args = args
		self._Averages = []
		self._SampleSizes = []

		self.m_MSError=None
		self.m_DFTreatment=None
		self.m_DFError=None
		self.m_TukeyTable=[]
		self.m_pvalue = None



	def compute(self)->tuple[float, aov_results]:
		SS_Treatment, SS_Error, SS_Total=0, 0, 0
		NEntries = 0

		#C is a variable defined to speed up computations (see Larsen Marx Chapter 12 on ANOVA)
		_c = 0.0

		for elem in self._args:
			TypeOK=isinstance(elem, list) or isinstance(elem, np.ndarray)
			if(TypeOK == False):
				raise TypeError("list/ndarray expected")

			ElemSize = len(elem)
			LocalSum = 0.0
			
			for entry in elem:
				LocalSum += entry
				SS_Total += entry**2
			
			#Required for Tukey test
			self._Averages.append(LocalSum/ElemSize)
			self._SampleSizes.append(ElemSize) 

			_c += LocalSum
			NEntries += ElemSize
			SS_Treatment += LocalSum**2/ElemSize

            
		_c = _c**2 / NEntries
		
		SS_Total = SS_Total - _c
		SS_Treatment = SS_Treatment - _c
		SS_Error = SS_Total - SS_Treatment

		self.m_DFError, self.m_DFTreatment = NEntries-len(self._args), len(self._args)-1 
		DF_Total = self.m_DFError + self.m_DFTreatment

		MS_Treatment, self.m_MSError = SS_Treatment/self.m_DFTreatment , SS_Error/self.m_DFError

		Fvalue = MS_Treatment/self.m_MSError

		self.m_pvalue = 1 - pf(q = float(Fvalue), df1 = self.m_DFTreatment, df2 = self.m_DFError)

		ResultCls = aov_results(
			Treat_DF=self.m_DFTreatment,
			Treat_MS = float(MS_Treatment),
			Treat_SS = float(SS_Treatment),
			Error_DF=self.m_DFError,
			Error_SS = float(SS_Error),
			Error_MS = float(self.m_MSError),
			Total_DF=DF_Total,
			Total_SS = float(SS_Total),
			Total_MS = float(SS_Total/DF_Total),
			Fvalue = float(Fvalue))

		return self.m_pvalue, ResultCls



	def tukey(self, alpha)->list:
		"""
		perform tukey test
		"""
		
		if(len(self._Averages) == 0):
			raise RuntimeError("first compute must be called")
		
		if(isinstance(alpha, numbers.Number) == False):
			raise TypeError("Alpha must be of type number")

		D = qdist(1-alpha, self.m_DFTreatment-1, self.m_DFError-1) / math.sqrt(self._SampleSizes[0])
		ConfIntervalLength = D*math.sqrt(self.m_MSError)

		self.m_TukeyTable=[]
		for i in range(len(self._Averages)):
			for j in range(i+1, len(self._Averages)):
				MeanValueDiff = self._Averages[i]-self._Averages[j]
				ConfInterval1 = MeanValueDiff-ConfIntervalLength
				ConfInterval2 = MeanValueDiff+ConfIntervalLength

				com = self.TukeyComparison()

				com.m_a=i
				com.m_b=j
				com.m_MeanValueDiff=MeanValueDiff
				com.m_CILow = min(ConfInterval1,ConfInterval2)
				com.m_CIHigh = max(ConfInterval1,ConfInterval2)

				self.m_TukeyTable.append(com)

		return self.m_TukeyTable
