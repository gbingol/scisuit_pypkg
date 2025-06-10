import numpy as np

from scisuit.stats import test_t



def ttest_2sample():
	

	treat = [24, 43, 58, 71, 43, 49, 61, 44, 67, 49, 53, 56, 59, 52, 62, 54, 57, 33, 46, 43, 57]
	cont = [42, 43, 55, 54, 20, 85, 33, 41, 19, 60, 53, 42, 46, 10, 17, 28, 48, 37, 42, 55, 26, 62, 37]

	result=test_t(x=treat, y=cont, varequal=False)
	print(result)



def ttest_1sample():
	v = [5, 6, 0, 4, 11, 9, 2, 3]
	tbl=test_t(x=v, mu=8.6)
	print(tbl)



def ttest_paired():
	pre=[18, 21, 16, 22, 19, 24, 17, 21, 23, 18, 14, 16, 16, 19, 18, 20, 12, 22, 15, 17]
	post=[22, 25, 17, 24, 16, 29, 20, 23, 19, 20, 15, 15, 18, 26, 18, 24, 18, 25, 19, 16]
	tbl=test_t(x=pre, y=post, paired=True)
	
	print(tbl)



ttest_2sample()