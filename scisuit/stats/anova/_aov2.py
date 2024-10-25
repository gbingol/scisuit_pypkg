from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .._distributions import pf

from ctypes import py_object
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_test_anova_aov2.argtypes = [py_object, py_object, py_object]
_pydll.c_stat_test_anova_aov2.restype=py_object


def _parsedata(y, x1, x2, v1, v2):
	"""
	parse the data that comes in the format of y, x1, x2 to
	columns of x1 (v1 columns) and rows of x2 (v1 columns)

	The formatted data looks like how Excel accepts data for 2-factor ANOVA
	"""
	Tbl = []
	for i in range(len(v2)):
		Tbl.append(list())
		for j in range(len(v1)):
			Tbl[i].append(list())

	for k in range(len(y)):
		i, j = -1, -1

		while (True):
			i += 1 
			if x2[k] == v2[i]: break

		while (True):
			j +=1
			if x1[k] == v1[j]: break
		
		Tbl[i][j].append(float(y[k]))
	
	return Tbl



def _averageMatrix(Tbl, v2):
	"""contains average value of each cell's data list"""
	MatAverage = []
	for i in range(len(v2)):
		arr = np.array(Tbl[i]).transpose()
		v = arr.mean(axis = 0)
		MatAverage.append(v.tolist())
	return MatAverage


#----------------------------------------------------------------
#----------------------------------------------------------------



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



#--------------------------------------------------------------------


def aov2_replicate(
		yy:np.ndarray, 
		xx1:np.ndarray, 
		xx2:np.ndarray,
		v1:np.ndarray, #unique factor #1
		v2:np.ndarray #unique factor #2
		)->aov2_results:
	"""Data has replicates"""

	Tbl = _parsedata(yy, xx1, xx2, v1, v2)
	MatAverage = _averageMatrix(Tbl, v2)

	SSerror = 0
	Residuals, Fits = [], []

	for i in range(len(v2)):
		for j in range(len(v1)):
			sz = len(Tbl[i][j])
			for k in range(sz):
				Err = float(Tbl[i][j][k] - MatAverage[i][j])
				SSerror += Err**2.0

				Residuals.append(Err)
				Fits.append(float(MatAverage[i][j]))

	MatAverage = np.array(MatAverage)
	GrandMean = MatAverage.mean()
	Nreplicate = len(Tbl[0][0])
	DFerror = (Nreplicate - 1) * (len(v1)) * (len(v2))
	MSerror = SSerror / DFerror

	meanj = MatAverage.mean(axis = 0)
	meani = MatAverage.transpose().mean(axis = 0)

	DFFact1, DFFact2 = len(v1) - 1, len(v2) - 1
	SSFact1 = np.sum((meanj - GrandMean)**2) * Nreplicate * len(v2)
	SSFact2 = np.sum((meani - GrandMean)**2) * Nreplicate * len(v1)
	MSFact1, MSFact2 = float(SSFact1) / DFFact1, float(SSFact2) / DFFact2

	SSinteract = 0
	for i in range(len(v2)):
		for j in range(len(v1)):
			SSinteract += (MatAverage[i, j] - meanj[j] - meani[i] + GrandMean)**2

	SSinteract *= Nreplicate
	DFinteract = DFFact1 * DFFact2
	MSinteract = SSinteract / DFinteract

	FvalFact1, FvalFact2, Fvalinteract = float(MSFact1 / MSerror), float(MSFact2 / MSerror), float(MSinteract / MSerror)
	pvalFact1 = 1.0 - pf(FvalFact1, DFFact1, DFerror)
	pvalFact2 = 1.0 - pf(FvalFact2, DFFact2, DFerror)
	pvalinteract = 1.0 - pf(Fvalinteract, DFinteract, DFerror)

	return aov2_results(
		DFError=DFerror, 
		DFFact1=DFFact1, 
		DFFact2=DFFact2,
		DFinteract=DFinteract,
		FvalFact1=FvalFact1, 
		FvalFact2 =FvalFact2, 
		Fvalinteract = Fvalinteract,
		MSError = float(MSerror), 
		MSFact1 = MSFact1, 
		MSFact2 = MSFact2, 
		MSinteract= float(MSinteract),
		pvalFact1 = float(pvalFact1), 
		pvalFact2 = float(pvalFact2), 
		pvalinteract= float(pvalinteract),
		SSError = float(SSerror), 
		SSFact1 = float(SSFact1), 
		SSFact2 = float(SSFact2), 
		SSinteract = float(SSinteract),

		Fits=Fits,
		Residuals=Residuals
	)



#--------------------------------------------------------------------


def aov2_noreps(
		yy:np.ndarray, 
		xx1:np.ndarray, 
		xx2:np.ndarray,
		v1:np.ndarray, #unique factor #1
		v2:np.ndarray #unique factor #2
		)->aov2_results:
	"""Data has NO replicates"""

	grand_mean = np.mean(yy)

	x1_means = [float(np.mean(yy[xx1 == b])) for b in v1]
	x2_means = [float(np.mean(yy[xx2 == t])) for t in v2]

	SSFact1 = len(v2)*sum([(v - grand_mean)**2 for v in x1_means])
	SSFact2 = len(v1)*sum([(v - grand_mean)**2 for v in x2_means])

	SS_total = sum((yy[i] - grand_mean)**2 for i in range(len(yy)))
	SS_error = SS_total - SSFact1 - SSFact2

	DFFact1, DFFact2 = len(v1) - 1, len(v2) - 1
	MSFact1, MSFact2 = float(SSFact1) / DFFact1, float(SSFact2) / DFFact2

	DFerror = DFFact1* DFFact2
	MSerror = SS_error/DFerror	

	FvalFact1, FvalFact2 = float(MSFact1 / MSerror), float(MSFact2 / MSerror)
	pvalFact1 = 1.0 - pf(FvalFact1, DFFact1, DFerror)
	pvalFact2 = 1.0 - pf(FvalFact2, DFFact2, DFerror)

	return aov2_results(
		DFError=DFerror, 
		DFFact1=DFFact1, 
		DFFact2=DFFact2,
		DFinteract=None,
		FvalFact1=FvalFact1, 
		FvalFact2 =FvalFact2, 
		Fvalinteract = None,
		MSError = float(MSerror), 
		MSFact1 = MSFact1, 
		MSFact2 = MSFact2, 
		MSinteract= None,
		pvalFact1 = float(pvalFact1), 
		pvalFact2 = float(pvalFact2), 
		pvalinteract= None,
		SSError = float(SS_error), 
		SSFact1 = float(SSFact1), 
		SSFact2 = float(SSFact2), 
		SSinteract = None,

		Residuals=None,
		Fits=None
	)




#--------------------------------------------------------------------
#--------------------------------------------------------------------


def aov2_temp(y:Iterable, x1:Iterable, x2:Iterable)->aov2_results:
	"""
	Performs 2-way ANOVA for balanced designs.

	---
	y: Responses   
	x1, x2: factors
	"""
	xx1 = np.asarray(x1)
	xx2 = np.asarray(x2)
	yy = np.asarray(y)

	assert len(xx1)>= 3, "x1 must have at least 3 elements"
	assert len(xx2) == len(xx1), "x1 and x2 must have same size"
	assert len(xx1) == len(yy), "x1 and y must have same size"

	assert np.issubdtype(yy.dtype, np.number), "y must contain only numbers"

	v1 = np.unique(xx1)
	v2 = np.unique(xx2)

	assert len(v1)>1, "Factor #1 must have at least two-levels."
	assert len(v2)>1, "Factor #2 must have at least two-levels."

	Tbl = _parsedata(yy, xx1, xx2, v1, v2)
	NReplicate = len(Tbl[0][0])

	if NReplicate>1:
		return aov2_replicate(yy=yy, xx1=xx1, xx2=xx2, v1=v1, v2=v2)
	
	return aov2_noreps(yy=yy, xx1=xx1, xx2=xx2, v1=v1, v2=v2)



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


	