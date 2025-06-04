from scisuit.stats import test_kruskal

responses = [52, 58, 59, 65, 69, 71, 55, 58, 60, 62, 66, 78, 57, 
		66, 70, 77, 79, 81, 67, 72, 81, 84, 91, 95]

groups = ["A", "A", "A", "A", "A", "A", 
		"B", "B", "B", "B", "B", "B", 
		"C", "C", "C", "C", "C", "C", 
		"D", "D", "D", "D", "D", "D"]


result = test_kruskal(responses, groups)
print(result)