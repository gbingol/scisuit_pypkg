import numbers
import scisuit.plot as plt
from scisuit.stats import test_z, test_z1_Result

#Inputs
conflevel = 0.95
Mu = 132.4
Sigma = 6 #sd of population

AlterOpt = ["two.sided", "greater", "less"]
Alternative = AlterOpt[0]

Data = [141,146,144,141,141,136,137,149,141,142,142,147,148,155,150,144,140,140,139,148,143,
143,149,140,132,158,149,144,145,146,143,135,147,153,142,142,138,150,145,126,135,
142,140,148,146,149,137,140,154,140,149,140,147,137,131,152,150,146,134,137,142,
147,158,144,146,148,143,143,132,149,144,152,150,148,143,142,141,154,141,144,142,
138,146,145,]

#Ensure Data contains only numbers and at least 3 of them
Data = [i for i in Data if isinstance(i, numbers.Real)]
assert len(Data)>2, "At least 3 data points expected"

Result:test_z1_Result = test_z(x=Data, mu=Mu, sd1=Sigma, alternative=Alternative, conflevel=conflevel)
print(Result)
	
#For visualization purposes
plt.hist(Data)
plt.figure()
plt.boxplot(Data)
			
plt.show()