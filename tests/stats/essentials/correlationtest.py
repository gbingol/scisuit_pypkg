from scisuit.stats import cor_test

C1 = [500, 760, 320, 1000]
C2 = {67, 43, 20, 45}
	
res = cor_test(C1, C2, 0.95, "spearman")
print(res)