import numbers
import scisuit.plot as plt
from scisuit.stats import test_f

conflevel = 0.95
Ratio = 1.0

AlterOpt = ["two.sided", "greater", "less"]
Alternative = AlterOpt[0]

xdata = [10.7,10.7,10.4,10.9,10.5,10.3,9.6,11.1,11.2,10.4]
ydata = [9.6,10.4,9.7,10.3,9.2,9.3,9.9,9.5,9,10.9]

xdata = [i for i in xdata if isinstance(i, numbers.Real) ]
ydata = [i for i in ydata if isinstance(i, numbers.Real) ]


#Result is a test_f_Result type class and contains details
Result = test_f(x=xdata, y=ydata, ratio=Ratio, alternative=Alternative, conflevel=conflevel)
print(Result)

#Visualize the results using box-whisker
plt.boxplot(xdata, "X")
plt.boxplot(ydata, "Y")
plt.show()