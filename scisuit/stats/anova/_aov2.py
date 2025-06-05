from dataclasses import dataclass
from typing import Iterable


from ctypes import py_object
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_test_anova_aov2.argtypes = [py_object, py_object, py_object]
_pydll.c_stat_test_anova_aov2.restype=py_object






@dataclass
class aov2_results():
	DFError:int 
	DFFact1:int 
	DFFact2:int 
	DFinteract:int
	FvalFact1:float 
	FvalFact2:float 
	Fvalinteract:float
	MSError:float 
	MSFact1:float 
	MSFact2:float
	MSinteract:float
	pvalFact1:float 
	pvalFact2:float
	pvalinteract:float
	SSError:float
	SSFact1:float
	SSFact2:float
	SSinteract:float

	Residuals:list
	Fits:list


	def __str__(self):
		s = "    Two-way ANOVA Results    \n"
		s += "{:<10} {:>10} {:>15} {:>15} {:>15} {:>15}\n".format(
			"Source", "df", "SS", "MS", "F", "p-value")
		
		s += "{:<10} {:>10} {:>15.2f} {:>15.2f} {:>15.2f} {:>15.4e}\n".format(
			"x1", self.DFFact1, self.SSFact1, self.MSFact1, self.FvalFact1, self.pvalFact1)
		
		s += "{:<10} {:>10} {:>15.2f} {:>15.2f} {:>15.2f} {:>15.4e}\n".format(
			"x2", self.DFFact2, self.SSFact2, self.MSFact2, self.FvalFact2, self.pvalFact2)
		
		if self.DFinteract != None:
			s += "{:<10} {:>10} {:>15.2f} {:>15.2f} {:>15.2f} {:>15.4e}\n".format(
				"x1*x2", self.DFinteract, self.SSinteract, self.MSinteract, self.Fvalinteract, self.pvalinteract)
		
		return s



def aov2(y:Iterable, x1:Iterable, x2:Iterable)->aov2_results:
	"""
	Performs 2-way ANOVA for balanced designs.

	---
	y: Responses   
	x1, x2: factors
	"""

	assert len(x1)>= 3, "x1 must have at least 3 elements"
	assert len(x2) == len(x1), "x1 and x2 must have same size"
	assert len(x1) == len(y), "x1 and y must have same size"

	for v in y:
		assert isinstance(v, float|int), "y must contain only numbers"


	dct:dict = _pydll.c_stat_test_anova_aov2(y, x1, x2)

	return aov2_results(
		DFError = dct["DFError"], 
		DFFact1 = dct["DFFact1"], 
		DFFact2 = dct["DFFact2"],
		DFinteract = dct.get("DFinteract"),
		FvalFact1 = dct["FvalFact1"], 
		FvalFact2 = dct["FvalFact2"], 
		Fvalinteract = dct.get("Fvalinteract"),
		MSError = dct["MSError"], 
		MSFact1 = dct["MSFact1"], 
		MSFact2 = dct["MSFact2"], 
		MSinteract= dct.get("MSinteract"),
		pvalFact1 = dct["pvalFact1"], 
		pvalFact2 = dct["pvalFact2"], 
		pvalinteract= dct.get("pvalinteract"),
		SSError = dct["SSError"], 
		SSFact1 = dct["SSFact1"], 
		SSFact2 = dct["SSFact2"], 
		SSinteract = dct.get("SSinteract"),

		Residuals = dct.get("Residuals"),
		Fits=dct.get("Fits")
	)


	