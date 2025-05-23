import numbers
import numpy as np
import scisuit.plot as plt

#Inputs
NSamples = 1000

x = np.array([81,75,44,33], dtype=np.float64)
y = np.array([50,60,70,80], dtype=np.float64)

#Ensure Data contains only numbers and at least 3 of them
x = [i for i in x if isinstance(i, numbers.Real)]
assert len(x)>2, "At least 3 data points expected for Sample #1"

y = [i for i in y if isinstance(i, numbers.Real)]
assert len(y)>2, "At least 3 data points expected for Sample #2"

#collect the differences
results = []

for i in range(NSamples):
	x_ = np.array(np.random.choice(x, size=len(x), replace=True))
	y_ = np.array(np.random.choice(y, size=len(y), replace=True))

	results.append(np.mean(x_) - np.mean(y_))

print("Mean=", np.mean(results))
print("StDev=", np.std(results, ddof=1)) #Sample std
	
#For visualization purposes
if len(results)>=10:
	plt.hist(results)
	plt.show()