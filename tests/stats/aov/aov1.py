from scisuit.stats import aov, tukey, fisher

A = [16, 11, 20, 21, 14, 7]
B = [21, 12, 14, 17, 13, 17]
C = [37, 32, 12, 25, 39, 41]
D = [45, 59, 48, 46, 38, 47]

#perform 1-way ANOVA
result = aov(A, B, C, D)
print(result)

tukeyres = fisher(0.05, result)
print(tukeyres)