import numbers
import numpy as np
import scisuit.plot as plt


Data = [ 
[0.397,0.813,-0.247,0.072,-0.531,0.544,-1.184,-0.274,1.119,-0.149], 
[0.57,1.632,0.227,-1.73,-1.051,-0.02,2.066,-1.006,1.784,0.962], 
[-0.705,0.739,0.51,-1.634,-0.342,-2.022,1.8,1.729,-1.735,-0.2], 
]

Data = np.array(Data, dtype=np.float64)

AXIS = 1 # Column statistics (for Row Stats change to 1)
DDOF = 1 # Sample std (for population change to 0)

print('Sum=', np.sum(Data, axis=AXIS))

print('Mean=', np.mean(Data, axis=AXIS))

print('SD=', np.std(Data, axis=AXIS, ddof=DDOF))

print('Min=', np.min(Data, axis=AXIS))

print('Max=', np.max(Data, axis=AXIS))

print('Range=', np.max(Data, axis=AXIS) - np.min(Data, axis=AXIS))

print('Sum of Squares=', np.sum(Data*Data, axis=AXIS))

#Visualize Data
if isinstance(Data[0], numbers.Real):
	plt.boxplot(Data)
else:
	for i, data in enumerate(Data):
		plt.boxplot(data, 'Column='+str(i+1))
plt.title("Box-Whisker Plot")
plt.show()