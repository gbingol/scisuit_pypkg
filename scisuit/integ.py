import numpy as _np
import math as _math

def trapz(x:list|_np.ndarray, y:list|_np.ndarray)->float:
    """
    Computes area using trapezoidal method and uses Numpy's trapz method.

    ## Input: 
    x, y: list or ndarray
    """
    return _np.trapz(x=x, y=y)



def cumtrapz(x:list|_np.ndarray, y:list|_np.ndarray)->list:
	"""
	Computes the left-tailed cumulative area

	##Input:
	x, y: list or ndarray
	"""
	val = 0.0
	a, b, f_a, f_b = 0.0, 0.0, 0.0, 0.0
	retList =[0.0]

	for i in range(len(x)-1):
		a = x[i]
		b = x[i + 1]

		if _math.isclose(b, a, abs_tol = 1E-5):
			raise ValueError("|X(i+1)-X(i)|<1E-5")

		if (b < a):
			raise ValueError("X(i+1) > X(i) expected.")

		f_a = y[i]
		f_b = y[i + 1]

		val += (b - a) * (f_a + f_b) / 2.0

		retList.append(val)
	
	return retList