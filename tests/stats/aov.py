from scisuit.stats import aov2

Catalyst = ["A", "A", "A", "A", "A", "A", "A", "A", "A", 
			"B", "B", "B", "B", "B", "B", "B", "B", "B", 
			"C", "C", "C", "C", "C", "C", "C", "C", "C"]

Temperature = ["L", "L", "L", "M", "M", "M", "H", "H", "H", 
			   "L", "L", "L", "M", "M", "M", "H", "H", "H", 
			   "L", "L", "L", "M", "M", "M", "H", "H", "H"]

Yield = [85, 88, 90, 80, 82, 84, 75, 78, 77, 90, 92, 91, 
		 85, 87, 89, 80, 83, 82, 88, 90, 91, 84, 86, 85, 79, 80, 81]

result1 = aov2(y=Yield, x1=Temperature, x2=Catalyst)
print(result1)


""" ------------------------------------- """

brand = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
treatment = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
removal = [0.97, 0.48, 0.48, 0.46, 0.77, 0.14, 0.22, 0.25, 0.67, 0.39, 0.57, 0.19]

result = aov2(y=removal, x1=treatment, x2=brand)
print(result)