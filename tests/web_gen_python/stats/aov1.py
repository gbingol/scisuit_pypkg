import scisuit.plot as plt
from scisuit.stats import aov, aov_results

#Inputs
Data = [ 
[16,11,20,21,14,7], 
[21,12,14,17,13,17], 
[37,32,12,25,39,41], 
[45,59,48,46,38,47], 
]

Result:aov_results = aov(*Data)
print(Result)
	
#For visualization purposes
for _d in Data:
	plt.boxplot(_d)
			
plt.show()