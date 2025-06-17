import numpy as np
from numpy.dtypes import StringDType
from dataclasses import dataclass




@dataclass
class tally_Result:
	values: list[str]
	counts: list[int]
	percents: list[float]
	cumcounts:list[int]
	cumpercents:list[float]



def tally(data:list[str])->tally_Result:
	"""
	Computes: 
	- individual unique elements  
	- Each element's counts
	- Each element's percentage
	- Cumulative counts and percentages
	"""

	arr = np.array(data, dtype=StringDType)
	values, counts = np.unique_counts(arr)
	
	Percents = counts/np.sum(counts)*100
	CumCounts = np.cumsum(counts)
	CumPercents = np.cumsum(Percents)

	return tally_Result(
		values=values,
		counts=counts,
		percents=Percents,
		cumcounts=CumCounts,
		cumpercents=CumPercents)