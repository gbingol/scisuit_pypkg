from scisuit.stats import test_mannwhitney

experiment = [2, 19, 13, 9, 17, 18, 24, 15, 22, 21]
control = [8, 1, 0, 10, 20, 5, 11, 7, 3, 13, 4]

result = test_mannwhitney(experiment, control)
print(result)