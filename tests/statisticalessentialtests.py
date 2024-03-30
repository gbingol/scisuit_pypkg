import sys, os
import pprint
import numpy as np

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

import scisuit.stats as st

def ttest():
	from scisuit.stats import test_t

	treat = [24, 43, 58, 71, 43, 49, 61, 44, 67, 49]
	cont = [42, 43, 55, 54, 20, 85, 33, 41, 19, 60, 53, 42]

	pval, tbl=test_t(x=treat, y=cont, varequal=False)

	print("p-value=" + str(pval))
	pprint.pprint(tbl)



def ANOVA1():
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
	pprint.pprint(info)



def ftest():
	x = [10.7, 10.7, 10.4, 10.9, 10.5, 10.3, 9.6, 11.1, 11.2, 10.4]
	y = [9.6, 10.4, 9.7, 10.3, 9.2, 9.3, 9.9, 9.5, 9.0, 10.9]
	pval, res = st.test_f(x, y)
	print(pval)
	print(res)

ftest()