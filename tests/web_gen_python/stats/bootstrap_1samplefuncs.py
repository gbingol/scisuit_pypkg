import numbers
import numpy as np
import scisuit.plot as plt

from functools import partial

#Inputs
Data = np.array([81,75,44,33], dtype=np.float64)

#Ensure Data contains only numbers and at least 3 of them
Data = [i for i in Data if isinstance(i, numbers.Real)]
assert len(Data)>2, "At least 3 data points expected"

NSamples = 1000

var = partial(np.var, ddof=1)
std = partial(np.std, ddof=1)

Funcs = [np.mean, np.median, std, var, np.sum]
Func = Funcs[4]

#collect the differences
results = []

for i in range(NSamples):
	x = np.array(np.random.choice(Data, size=len(Data), replace=True))
	results.append(Func(x))

print("Mean=", np.mean(results))
print("StDev=", np.std(results, ddof=1)) #Sample std
	
#For visualization purposes
if len(results)>=10:
	plt.hist(results)
	plt.show()