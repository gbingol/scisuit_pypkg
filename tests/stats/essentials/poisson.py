from scisuit.stats import test_poisson1sample, test_poisson1sample_Result

Sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
Freq = [57, 203, 383, 525, 532, 408, 273, 139, 45, 27, 10, 6]
	
res = test_poisson1sample(Sample, Freq, None, None, 1.0, True, 4.0, 0.95, "normal", "two.sided")
print(res)