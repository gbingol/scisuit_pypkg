from scisuit.stats import aov2

Catalyst = ["A", "A", "A", "A", "A", "A", "A", "A", "A", 
			"B", "B", "B", "B", "B", "B", "B", "B", "B", 
			"C", "C", "C", "C", "C", "C", "C", "C", "C"]

Temperature = ["L", "L", "L", "M", "M", "M", "H", "H", "H", 
			   "L", "L", "L", "M", "M", "M", "H", "H", "H", 
			   "L", "L", "L", "M", "M", "M", "H", "H", "H"]

Yield = [85, 88, 90, 80, 82, 84, 75, 78, 77, 90, 92, 91, 
		 85, 87, 89, 80, 83, 82, 88, 90, 91, 84, 86, 85, 79, 80, 81]

result = aov2(y=Yield, x1=Temperature, x2=Catalyst)
print(result)