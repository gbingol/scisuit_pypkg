import numpy as _np

def sample(y, size:int, replace = False):
	"""
	y: ndarray / list.

	## Example
	ss = _np.linspace(start=1, stop=10, num=10) \n
	s = sample(ss, 4) \n
	s1 = sample(ss, 11, replace=True) \n
	s2 = sample(ss, 11, replace=False) \n
	print(s1)
	"""
	n = len(y)

	assert n >= 3, "list/ndarray must have at least 3 elements"
	assert isinstance(y, list) or isinstance(y, _np.ndarray), "list/ndarray expected"
	
	Arr = None
	if(isinstance(y, list)):
		Arr = _np.asarray(y)
	else:
		Arr = _np.array(y)

	if replace == False:
		if size>=n:
			raise ValueError("when replace=False, size < len(y) expected")
		_np.random.shuffle(Arr)
		
		return _np.array(Arr[0:size]).tolist()
	
	else:
		Index = _np.random.randint(low=0, high=n, size=size)
		t=[]
		for i in Index:
			t.append(Arr[i])
		return t

"""
ss = _np.linspace(start=1, stop=10, num=10)
s = sample(ss, 4)
s1 = sample(ss, 11, replace=True)
s2 = sample(ss, 11, replace=False)
print(s1)
"""