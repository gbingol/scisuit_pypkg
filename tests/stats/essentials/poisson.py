from scisuit.stats import test_poisson1sample, test_poisson1sample_Result

def samples_freq():
	Sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
	Freq = [57, 203, 383, 525, 532, 408, 273, 139, 45, 27, 10, 6]
		
	return test_poisson1sample(
				Sample, 
				Freq, 
				length=1.0, 
				hypotest=True, 
				hyporate=4.0, 
				conflevel=0.95, 
				method="normal", 
				alternative="two.sided")
	


def summarizeddata():
	samplesize = 2608
	totaloccur = 10092

	return test_poisson1sample(
						samplesize=samplesize, 
						totaloccur=totaloccur, 
						length=1.0, 
						hypotest=True, 
						hyporate=4.0, 
						conflevel=0.95, 
						method="normal", 
						alternative="two.sided")


print(samples_freq())

print("\n------------\n")

print(summarizeddata())