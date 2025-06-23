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


"""
One-Way ANOVA Results 
Source             df              SS              MS               F         p-value
Treatment           3         4194.33         1398.11           27.23      2.9061e-07
Error              20         1027.00           51.35
Total              23         5221.33

   Tukey Test Results (alpha=0.05)

Pairwise Diff             i-j             Interval
1 - 2                -0.83           (-12.41, 10.75)
1 - 3               -16.17           (-27.75, -4.59)
1 - 4               -32.33          (-43.91, -20.75)
2 - 3               -15.33           (-26.91, -3.75)
2 - 4               -31.50          (-43.08, -19.92)
3 - 4               -16.17           (-27.75, -4.59)

"""