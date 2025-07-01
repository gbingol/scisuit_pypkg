import numbers
from dataclasses import dataclass
from typing import Iterable

from ctypes import py_object, c_double, c_char_p, c_bool
from ..._ctypeslib import pydll as _pydll

_pydll.c_stat_test_multivariate_pca.argtypes = [py_object, c_bool, c_bool]
_pydll.c_stat_test_multivariate_pca.restype = py_object


@dataclass 
class EigenComp:
	value: float
	vector: list[float]


@dataclass
class Outliers:
	mahalanobis: list[float]
	reference: float


@dataclass
class Score:
	firstcomp:float
	secondcomp:float


@dataclass
class pca_Result:
	_labels: list[str]
	eigs: list[EigenComp]
	outliers: Outliers|None
	scores: list[Score]|None


def pca(variables:list[list[numbers.Real]], labels:list[str] = [], outliers = True, scores = True)->pca_Result:
	"""
	Principal Components Analysis  
	---
	variables: The data section - each sublist is considered as a column of a table  
	labels: The labels of the variables  
	outliers: Should compute outliers (mahalanobis distance and reference line)  
	scores: Should compute scores (data necessary for score and biplot charts)
	"""
	dct = _pydll. c_stat_test_multivariate_pca(variables, c_bool(outliers), c_bool(scores))

	DctEigs:list[tuple[float, list[float]]] = dct["eigs"]

	LstEigs:list[EigenComp] = []
	for e in DctEigs:
		eigval, eigvec = e
		LstEigs.append(EigenComp(value=eigval, vector=eigvec))
	

	ObjOutliers:Outliers = None
	if outliers:
		mahalanobis = dct["mahalanobis"]
		referenceLine = dct["reference"]
		ObjOutliers = Outliers(mahalanobis=mahalanobis, reference=referenceLine)
	

	LstScores:list[Score] = []
	if scores:
		dctScores = dct["scores"]
		for e in dctScores:
			first, second = e
			LstScores.append(Score(firstcomp=first, secondcomp=second))
		
	return pca_Result(eigs=LstEigs, outliers=ObjOutliers, scores=LstScores, _labels = labels)


		
