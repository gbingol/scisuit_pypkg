import numpy as _np
import math as _math



def skew(y):
	"""
	Computes the skewness of a distribution <br>
	skew(y=) <br>
	
	y: ndarray / list.
	"""
	n = len(y)

	assert n >= 3, "list/ndarray must have at least 3 elements"
	assert isinstance(y, list) or isinstance(y, _np.ndarray), "list/ndarray expected"
	
	Arr = None
	if(isinstance(y, list)):
		Arr = _np.asarray(y)
	else:
		Arr = _np.array(y)
	
	avg, std_p = _np.mean(Arr), _np.std(Arr)

	skew_p = _np.sum((Arr-avg)**3)
	skew_p /= (n * std_p**3.0);

	return _math.sqrt(n * (n - 1)) * skew_p/(n-2)

"""
y = _np.random.standard_normal(1000)
print(skew(y))
"""