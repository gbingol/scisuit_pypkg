from scisuit.stats import pca
import scisuit.settings

Sample = [
    [50000,72000,61000,88000,91100,45100], 
    [16,18,18,20,18,14], 
	[28,35,36,35,38,41], 
	[2,10,6,4,8,15], 
	[2,8,5,4,9,14], 
	[5000,12000,15000,980,20000,3900], 
	[1200,5400,1000,1100,0,22000], 
	[2,4,2,4,1,4]]

scisuit.settings.NDIGITS = 4
result  = pca(Sample, [], outliers=False)
print(result)