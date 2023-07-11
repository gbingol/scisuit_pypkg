import numpy as _np

def mode(y):
	"""
	y: ndarray / list.<br>
	mode(y=) &rarr; (list, int)
	"""
	n = len(y)

	assert n >= 3, "list/ndarray must have at least 3 elements"
	assert isinstance(y, list) or isinstance(y, _np.ndarray), "list/ndarray expected"
	
	Arr = None
	if(isinstance(y, list)):
		Arr = _np.asarray(y)
	else:
		Arr = _np.array(y)

	values, counts = _np.unique(Arr, return_counts=True)
	if(len(values) == len(Arr)):
		return ([], 0)

	index = _np.argwhere(counts == _np.max(counts))

	return values[index].flatten().tolist(), int(_np.max(counts))

"""
t1=[1, 2, 3, 4, 5]
t2=[1, 3, 5, 7, 9, 3, 5, 7, 3, 6]
arr = np.array([1, 3, 5, 5, 7, 9, 3, 5, 7, 3, 6])
print(mode(y = arr))
"""