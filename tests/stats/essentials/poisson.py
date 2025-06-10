from scisuit.stats import test_poisson1sample, test_poisson1sample_Result

def samples_freq():
	Sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
	Freq = [57, 203, 383, 525, 532, 408, 273, 139, 45, 27, 10, 6]
		
	res = test_poisson1sample(Sample, Freq, None, None, 1.0, True, 4.0, 0.95, "normal", "two.sided")
	print(res)


def summarizeddata():
	samplesize = 2608
	totaloccur = 10092

	res = test_poisson1sample(None, None, samplesize, totaloccur, 1.0, True, 4.0, 0.95, "normal", "two.sided")
	print(res)


samples_freq()
summarizeddata()