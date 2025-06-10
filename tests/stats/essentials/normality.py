from scisuit.stats import anderson, ks_1samp, shapiro
from scisuit.stats import rchisq, pchisq


_data = [2.39798, -0.16255, 0.54605, 0.68578, -0.78007, 
		 1.34234, 1.53208, -0.86899, -0.50855, -0.58256, 
		 -0.54597, 0.08503, 0.38337, 0.26072, 0.34729]

result_ad = anderson(_data)
print("Anderson-Darling: ", result_ad)

result_ks = ks_1samp(_data)
print("Kolmogorov-Smirnov: ", result_ks)

result_sw = shapiro(_data)
print("Shapiro-Wilkinson: ", result_sw)


"""

data = rchisq(n=100, df=5)
#test normality
print("Normality test")
result = ks_1samp(x=data)
print(result)

#test chisq
print("\nChisq test")
result = ks_1samp(data, cdf=pchisq, args=(5,))
print(result)

"""