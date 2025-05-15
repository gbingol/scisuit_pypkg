import numbers
import scisuit.plot as plt
from scisuit.stats import test_t, test_tpaired_result

#Inputs
conflevel = 0.95 #confidence level
MeanDiff = 0 #Assumed mean difference

AlterOpt = ["two.sided", "greater", "less"]
Alternative = AlterOpt[0]

xdata = [18,21,16,22,19,24,17,21,23,18,14,16,16,19,18,20,12,22,15,17]
ydata = [22,25,17,24,16,29,20,23,19,20,15,15,18,26,18,24,18,25,19,16]

xdata = [i for i in xdata if isinstance(i, numbers.Real)]
ydata = [i for i in ydata if isinstance(i, numbers.Real)]

assert len(xdata) == len(ydata), "Sample #1 and #2 must have same lengths"
assert len(xdata)>2, "At least 3 data points expected"
assert len(ydata)>2, "At least 3 data points expected"

Result:test_tpaired_result = test_t(x=xdata, y=ydata, mu=MeanDiff, paired=True, alternative=Alternative, conflevel=conflevel)
print(Result)

#For visualization purposes
plt.boxplot(xdata)
plt.boxplot(ydata)
			
plt.show()