from scisuit.stats import pca
import scisuit.plot as plt
import scisuit.settings

"""
#Mahalanobis distance cannot be computed
Sample = [
    [50000,72000,61000,88000,91100,45100], 
    [16,18,18,20,18,14], 
	[28,35,36,35,38,41], 
	[2,10,6,4,8,15], 
	[2,8,5,4,9,14], 
	[5000,12000,15000,980,20000,3900], 
	[1200,5400,1000,1100,0,22000], 
	[2,4,2,4,1,4]]
"""

Sample = [
   [50000,72000,61000,88000,91100,45100,36200,41000,40000,32000,29000,21240,58700,
		41000,38720,88240,40000,34600,29800,56400,39800, 54200,42650,62200,72200,26530,36500,40000,41200,50000], 
	[16,18,18,20,18,14,14,12,16,16,16,12,12,14,16,16,18,16,12,16,14, 16,16,14,16,12,16,16,12,16], 
	[28,35,36,35,38,41,29,34,32,30,28,26,38,29,36,38,39,40,27,30,29,31,27,40,34,30,26,29,34,35], 
	[2,10,6,4,8,15,6,9,8,2,1,2,9,5,11,13,7,14,1,2,3,5,3,8,5,1,2,3,5,8], 
	[2,8,5,4,9,14,5,8,7,2,4,2,9,4,11,12,6,12,3,1,2,3,2,10,4,2,2,2,4,6], 
	[5000,12000,15000,980,20000,3900,100,5000,19000,16000,2100,100,4500,300,24500,13600,16000,34000,100,3000,2500,
	14200,5200,10000,12000,0,3100,1900,1000,4500], 
	[1200,5400,1000,1100,0,22000,7000,200,1760,550,4600,10010,7800,10000,540,8100,1300,100,10000,1200,900,
	800,1000,700,400,12000,800,1300,1200,1400], 
	[2,4,2,4,1,4,5,3,2,1,2,3,5,6,2,2,2,3,5,2,3,2,3,2,4,2,3,3,2,2]]

Labels = ["Income", "Education", "Age", "Residence", "Employ", "Savings", "Debt", "Cards"]

result  = pca(Sample, Labels, outliers=True, scores=True)

scisuit.settings.NDIGITS = 4
print(result)

eigs = result.eigs
outliers = result.outliers
eigenvals = [e.value for e in eigs]
plt.multivariate.scree(eigenvals)

plt.figure()

 
plt.multivariate.outlier(outliers.mahalanobis, outliers.reference)

plt.figure()

scores = result.scores
plt.multivariate.score([(e.firstcomp, e.secondcomp) for e in scores])

plt.figure()
plt.multivariate.loading(pc1=eigs[0].vector, pc2=eigs[1].vector, labels=Labels)

plt.show()