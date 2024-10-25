from dataclasses import dataclass, asdict
from typing import Iterable

from ctypes import py_object, c_double
from ..._ctypeslib import pydll as _pydll




_pydll.c_stat_test_anova_aov.argtypes = [py_object]
_pydll.c_stat_test_anova_aov.restype=py_object


_pydll.c_stat_test_anova_tukey.argtypes = [c_double, py_object] #alpha and aovresults
_pydll.c_stat_test_anova_tukey.restype=py_object


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
	for v in args:
		assert isinstance(v, Iterable), "Iterable objects expected."
	
	res:dict = _pydll.c_stat_test_anova_aov(args)

	return aov_results(
		Treat_DF= res["Treat_DF"],
		Treat_MS = res["Treat_MS"],
		Treat_SS = res["Treat_SS"],

		Error_DF= res["Error_DF"],
		Error_SS = res["Error_SS"],
		Error_MS = res["Error_MS"],
		Total_DF=res["Total_DF"],

		Total_SS = res["Total_SS"],
		Total_MS = res["Total_SS"]/res["Total_DF"],
		Fvalue = res["Fvalue"],
		pvalue=res["pvalue"],

		#For tukey test
		Averages=res["Averages"],
		SampleSizes=res["SampleSizes"])



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

	lst = _pydll.c_stat_test_anova_tukey(c_double(alpha), asdict(aovresult))

	TukeyTable = []
	for v in lst:
		comp = TukeyComparison(
		a=v["a"], 
		b = v["b"],
		Diff=v["diff"],
		CILow = min(v["CILow"], v["CIHigh"]),
		CIHigh = max(v["CILow"], v["CIHigh"]))

		TukeyTable.append(comp)

	return TukeyResults(r=TukeyTable, alpha=alpha)
