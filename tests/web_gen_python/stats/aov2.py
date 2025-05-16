import numbers
import scisuit.plot as plt
from scisuit.stats import aov2

#Inputs
Factor1 = [19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,
19,19,19,19,19,19,19,19,19,17,17,17,17,17,17,17,17,17,17,17,
17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,15,
15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,
15,15,15,15,15,15,15,15,15,13,13,13,13,13,13,13,13,13,13,13,
13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,]

Factor2 = [0,0,0,0,0,0,3,3,3,3,3,3,4.5,4.5,4.5,4.5,4.5,4.5,6,6,6,
6,6,6,9,9,9,9,9,9,0,0,0,0,0,0,3,3,3,3,3,
3,4.5,4.5,4.5,4.5,4.5,4.5,6,6,6,6,6,6,9,9,9,9,9,9,0,
0,0,0,0,0,3,3,3,3,3,3,4.5,4.5,4.5,4.5,4.5,4.5,6,6,6,
6,6,6,9,9,9,9,9,9,0,0,0,0,0,0,3,3,3,3,3,
3,4.5,4.5,4.5,4.5,4.5,4.5,6,6,6,6,6,6,9,9,9,9,9,9,]
assert len(Factor1) == len(Factor2), "Factors must have same length"

Observations = [-49,0,-98,148,49,49,-24,25,-123,222,123,74,11,60,-88,306,158,158,56,105,-141,
400,253,203,146,244,-51,687,441,392,61,61,160,12,-86,-37,-11,136,-110,235,87,
38,169,317,22,71,169,-77,413,-128,266,118,69,216,-46,446,397,249,692,151,73,
-74,172,-25,73,24,-98,148,99,247,50,1,180,180,33,-66,82,328,574,131,328,
279,33,-164,8,205,549,254,402,352,183,-63,-14,84,84,35,14,-85,63,112,161,
260,192,-54,192,340,45,94,439,95,-102,292,242,144,701,406,258,160,455,-37,]
Observations = [i for i in Observations if isinstance(i, numbers.Real)]
assert len(Observations) == len(Factor1), "Observations and Factors must have same length"

Result = aov2(y=Observations, x1=Factor1, x2=Factor2)
print(Result)
	

#For visualization purposes
Residuals = Result.Residuals
Fits = Result.Fits

if Residuals != None and Fits != None:
	plt.scatter(y = Residuals, x=Fits)
	plt.title("Fitted Values vs Residuals")

	plt.figure()

	plt.hist(Residuals, density=True)
	plt.title("Histogram of Residuals")

	plt.show()