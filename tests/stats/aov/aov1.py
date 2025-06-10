import numpy as np


from scisuit.stats import aov

A = np.array([16, 11, 20, 21, 14, 7])
B = np.array([21, 12, 14, 17, 13, 17])
C = np.array([37, 32, 12, 25, 39, 41])
D = np.array([45, 59, 48, 46, 38, 47])

#perform 1-way ANOVA
result = aov(A, B, C, D)
print(result)

