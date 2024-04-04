import sys, os
import pprint

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 



import scisuit.stats as st
import numpy as np


def AOV():
	from scisuit.stats import aov

	A = np.array([16, 11, 20, 21, 14, 7])
	B = np.array([21, 12, 14, 17, 13, 17])
	C = np.array([37, 32, 12, 25, 39, 41])
	D = np.array([45, 59, 48, 46, 38, 47])

	#perform 1-way ANOVA
	cls = aov(A, B, C, D)

	#p-value and extra info
	pval, info = cls.compute()

	print("p-value=" + str(pval))
	print(info)

	TukeyList = cls.tukey(0.05)
	for c in TukeyList:
		print(c)


def AOV2():
	vent = [-49, 0, -98, 148, 49, 49, -24, 25, -123, 222, 123, 
		 	74, 11, 60, -88, 306, 158, 158, 56, 105, -141, 400, 
			253, 203, 146, 244, -51, 687, 441, 392, 61, 61, 160, 
			12, -86, -37, -11, 136, -110, 235, 87, 38, 169, 317, 
			22, 71, 169, -77, 413, -128, 266, 118, 69, 216, -46, 
			446, 397, 249, 692, 151, 73, -74, 172, -25, 73, 24, 
			-98, 148, 99, 247, 50, 1, 180, 180, 33, -66, 82, 328, 
			574, 131, 328, 279, 33, -164, 8, 205, 549, 254, 402, 
			352, 183, -63, -14, 84, 84, 35, 14, -85, 63, 112, 161, 
			260, 192, -54, 192, 340, 45, 94, 439, 95, -102, 292, 242, 
			144, 701, 406, 258, 160, 455, -37]
	o2 = [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 
	      19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 17, 17, 
		  17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 
		  17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 15, 15, 15, 15, 
		  15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 
		  15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 13, 13, 13, 13, 13, 13, 
		  13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 
		  13, 13, 13, 13, 13, 13, 13, 13]
	co2 = [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 4.5, 4.5, 4.5, 4.5, 4.5, 
		4.5, 6, 6, 6, 6, 6, 6, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 
		3, 3, 3, 3, 3, 3, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 
		6, 6, 6, 6, 6, 6, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 
		3, 3, 3, 3, 3, 3, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 6, 
		6, 6, 6, 6, 6, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 
		3, 3, 3, 3, 3, 3, 4.5, 4.5, 4.5, 4.5, 4.5, 
		4.5, 6, 6, 6, 6, 6, 6, 9, 9, 9, 9, 9, 9]
	
	result = st.aov2(vent, o2, co2)
	print(result)



def ttest_2sample():
	from scisuit.stats import test_t

	treat = [24, 43, 58, 71, 43, 49, 61, 44, 67, 49, 53, 56, 59, 52, 62, 54, 57, 33, 46, 43, 57]
	cont = [42, 43, 55, 54, 20, 85, 33, 41, 19, 60, 53, 42, 46, 10, 17, 28, 48, 37, 42, 55, 26, 62, 37]

	pval, tbl=test_t(x=treat, y=cont, varequal=False)

	print("p-value=" + str(pval))
	pprint.pprint(tbl)



def ttest_1sample():
	v = [5, 6, 0, 4, 11, 9, 2, 3]
	pval, tbl=st.test_t(x=v, mu=8.6)
	print(pval)
	print(tbl)



def ttest_paired():
	pre=[18, 21, 16, 22, 19, 24, 17, 21, 23, 18, 14, 16, 16, 19, 18, 20, 12, 22, 15, 17]
	post=[22, 25, 17, 24, 16, 29, 20, 23, 19, 20, 15, 15, 18, 26, 18, 24, 18, 25, 19, 16]
	pvalue, tbl=st.test_t(x=pre, y=post, paired=True)
	print(pvalue)
	print(tbl)




def ztest():
	x = [141, 146, 144, 141, 141, 136, 137, 149, 141, 142, 
	142, 147, 148, 155, 150, 144, 140, 140, 139, 148, 143, 143, 149, 140, 132, 
	158, 149, 144, 145, 146, 143, 135, 147, 153, 142, 142, 138, 150, 145, 126]

	pval, tbl=st.test_z(x=x, mu=132.4, sd=6)
	print(pval)
	print(tbl)



def ftest():
	x = [10.7, 10.7, 10.4, 10.9, 10.5, 10.3, 9.6, 11.1, 11.2, 10.4]
	y = [9.6, 10.4, 9.7, 10.3, 9.2, 9.3, 9.9, 9.5, 9.0, 10.9]
	pval, res = st.test_f(x, y)
	print(pval)
	print(res)



def signtest():
	data = [4.8, 4.0, 3.8, 4.3, 3.9, 4.6, 3.1, 3.7]
	pval, result = st.test_sign(data, md=3.55)
	print(pval)
	print(result)



def norm_andersondarling():
	data = [2.39798, -0.16255, 0.54605, 0.68578, -0.78007, 
		 1.34234, 1.53208, -0.86899, -0.50855, -0.58256, 
		 -0.54597, 0.08503, 0.38337, 0.26072, 0.34729]
	
	result = st.test_norm_ad(data)

	print(result)


def ks1sampletest():
	from scisuit.stats import ks_1samp, Ks1SampletestResult
	x = [-0.62467049, 0.02793576, 0.17729038, 0.23238647, 0.28809798, 0.41124504, 0.7944974, 0.84870481]

	print(ks_1samp(x))


"""
AOV()
AOV2()
ztest()
ftest()
signtest()
ttest_2sample()
norm_andersondarling()

"""
