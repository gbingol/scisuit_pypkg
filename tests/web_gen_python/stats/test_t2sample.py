import numbers
import scisuit.plot as plt
from scisuit.stats import test_t

#Inputs
conflevel = 0.95 #confidence level
MeanDiff = 0 #Assumed mean difference
EqualVars = True #Equal variances?

AlterOpt = ["two.sided", "greater", "less"]
Alternative = AlterOpt[0]

xdata = [24,43,58,71,43,49,61,44,67,49,53,56,59,52,62,54,57,33,46,43,57]
ydata = [42,43,55,54,20,85,33,41,19,60,53,42,46,10,17,28,48,37,42,55,26,62,37]

xdata = [i for i in xdata if isinstance(i, numbers.Real)]
ydata = [i for i in ydata if isinstance(i, numbers.Real)]

assert len(xdata)>2, "At least 3 data points expected"
assert len(ydata)>2, "At least 3 data points expected"

Result = test_t(x=xdata, y=ydata, mu=MeanDiff, varequal=EqualVars, alternative=Alternative, conflevel=conflevel)
print(Result)

#For visualization purposes
plt.boxplot(xdata)
plt.boxplot(ydata)
			
plt.show()