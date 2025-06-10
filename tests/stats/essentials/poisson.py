from scisuit.stats import test_poisson1sample, test_poisson1sample_Result

def volcanoerupt():
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
	




def volcanoerupt_summarizeddata():
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




def customercomplaints():
	days = range(1,31) #data collected
	complaints = [19,18,22,21,17,18,22,19,16,23,25,16,18,18,
			   20,21,15,23,21,19,26,
			   21,17,26,16,24,21,18,17,21]
	
	return test_poisson1sample(
				complaints,  
				length=1, 
				hypotest=True, 
				hyporate=10, 
				conflevel=0.95, 
				method="normal", 
				alternative="greater")


print(volcanoerupt())

print("\n------------\n")

print(volcanoerupt_summarizeddata())

print("\n------------\n")

print(customercomplaints())