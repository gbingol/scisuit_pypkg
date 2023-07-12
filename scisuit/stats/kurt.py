import numpy as _np

def kurt(y:_np.ndarray | list):
	"""
	Computes excess kurtosis. \n
	y: ndarray / list.
	"""
	n = len(y)

	assert n >= 4, "list/ndarray must have at least 4 elements"
	assert isinstance(y, list) or isinstance(y, _np.ndarray), "list/ndarray expected"
	
	Arr = y
	if(isinstance(y, list)):
		Arr = _np.asfarray(y)

	avg = _np.mean(Arr)
	stdev = _np.std(Arr, ddof=1)

	s = 0
	for Num in y:
		s += (Num - avg)**4

	Kurt = (s/n)/(stdev)**4 - 3

	return float(Kurt)