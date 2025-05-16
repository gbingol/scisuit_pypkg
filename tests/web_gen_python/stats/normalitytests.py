import numbers
import scisuit.plot as plt
from scisuit.stats import ks_1samp, anderson, shapiro

Data = [2.39798,-0.16255,0.54605,0.68578,-0.78007,1.34234,1.53208,-0.86899,-0.50855,-0.58256,-0.54597,0.08503,0.38337,0.26072,0.34729]

Data = [e for e in Data if isinstance(e, numbers.Real)]
assert len(Data)>=3, "At least 3 numbers required."

ADResult = anderson(Data)
print("Anderson-Darling Test")
print(ADResult)

KSResult = ks_1samp(Data)
print("Kolmogorov-Smirnov Test")
print(KSResult)

SWResult = shapiro(Data)
print("Shapiro-Wilk Test")
print(SWResult)

plt.boxplot(Data)
plt.title("Box-Whisker Plot")

plt.figure()

plt.qqnorm(Data)
plt.title("QQ Plot")

plt.show()