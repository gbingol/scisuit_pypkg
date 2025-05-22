import numbers
import numpy as np
import scisuit.plot as plt


Data = [ 
[-0.814,-1.339,0.584,1.521,0.094,1.684,-2.303,0.562,-0.545,0.338], 
[-0.129,0.244,2.671,-1.283,1.375,2.111,1.67,0.505,0.077,-0.157], 
[1.574,-2.135,0.662,1.351,-0.401,0.943,-1.158,-0.019,0.09,-0.383], 
]

Data = np.array(Data, dtype=np.float64)

"""
Multidimensional Array Note:
Each array represents a column set AXIS variable for statistics of:
Column = 1 , Row = 0
"""
AXIS = 1

# Sample std (for population change to 0)
DDOF = 1 

print('Sum=', np.sum(Data, axis=AXIS)) 
print('Mean=', np.mean(Data, axis=AXIS)) 
print('Min=', np.min(Data, axis=AXIS)) 
print('Max=', np.max(Data, axis=AXIS)) 
print('Sum of Squares=', np.sum(Data*Data, axis=AXIS)) 

#Visualize Data
if isinstance(Data[0], numbers.Real):
	plt.boxplot(Data)
else:
	for i, data in enumerate(Data):
		plt.boxplot(data, 'Column='+str(i+1))
plt.title("Box-Whisker Plot")
plt.show()