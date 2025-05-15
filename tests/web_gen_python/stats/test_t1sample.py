import numbers
import scisuit.plot as plt
from scisuit.stats import test_t, test_t1_result

#Inputs
conflevel = 0.95
Mu = 0.618

AlterOpt = ["two.sided", "greater", "less"]
Alternative = AlterOpt[0]

Data = [0.69,0.606,0.57,0.749,0.672,0.628,0.609,0.844,0.654,0.615,0.668,0.601,0.576,0.67,0.606,0.611,0.553,0.933]

#Ensure Data contains only numbers and at least 3 of them
Data = [i for i in Data if isinstance(i, numbers.Real)]
assert len(Data)>2, "At least 3 data points expected"

Result:test_t1_result = test_t(x=Data, mu=Mu, alternative = Alternative, conflevel = conflevel)
print(Result)

#For visualization purposes
plt.hist(Data)
plt.figure()
plt.boxplot(Data)
			
plt.show()