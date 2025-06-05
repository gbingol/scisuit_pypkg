from scisuit.stats import test_friedman

"""
Strength of cotton fibers
							Treatments
			36		54		72		108		144
			-------------------------------------
		1|	7.62	8.14	7.76	7.17	7.46
Blocks	2|	8.00	8.15	7.73	7.57	7.68
		3|	7.93	78.87	7.74	7.80	7.21

"""

#Above shown data table must be entered in the following way
responses = [7.62, 8, 7.93, 8.14, 8.15, 7.87, 7.76, 7.73, 7.74, 7.17, 7.57, 7.8, 7.46, 7.68, 7.21]
factors = ["36", "36", "36", "54", "54", "54", "72", "72", "72", "108", "108", "108", "144", "144", "144"]
groups = ["1", "2", "3", "1", "2", "3", "1", "2", "3", "1", "2", "3", "1", "2", "3"]


result = test_friedman(responses, factors, groups)
print(result)