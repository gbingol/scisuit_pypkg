import sys, os
import pprint

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.stats as st

import math
import numpy as np
import matplotlib.pyplot as plt


n=5

#Generate 250 random numbers from uniform dist
W = np.array(list( map( lambda _: st.runif(n=250) , [None]*n) )).transpose() #2D array (250*5)

#For uniform distribution
mu=0.5
sigma=math.sqrt(1/12)

#W1+W2+...
x = np.sum(W, axis=1) #len=50


#z-ratio
z = (x - n*mu)/(math.sqrt(n)*sigma)

#DeMoivre's equation
f = 1.0/math.sqrt(2*math.pi)*np.exp(-z**2/2.0)

#Density scaled histogram
plt.hist(z, density=True, color = "green", ec="red")

#Overlay scatter plot
plt.scatter(x=z, y=f, marker="x")

plt.show()




def GammaDist():
	print(st.dgamma(x=4, scale=4, shape=3))
	print(st.pgamma(q = 3, shape = 10, scale = 0.25))
	print(st.qgamma(p =[0, 0.1, 0.2], shape = 10, scale = 0.25))


def ExponentialDist():
	print(st.dexp(x=3, rate=0.2))
	print(st.pexp(q=3, rate=0.2))
	print(st.qexp(p=0.3, rate=0.2))

	print(st.dexp(x=[1,2,3], rate=0.2))
	print(st.pexp(q=[1,2,3], rate=0.2))
	print(st.qexp(p=[0.1, 0.2, 0.3], rate=0.2))



def BinomialDist():
	print(st.dbinom(x=2, size=5, prob=0.3))
	print(st.dbinom(x=[7, 8, 9], size=9, prob=0.94))
	print(st.qbinom(p=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], size=9, prob=0.65))


def NegativeBinomialDist():
	print(st.dnbinom(x=2, size=5, prob=0.3))
	print(st.dnbinom(x=[7, 8, 9], size=9, prob=0.94))

	print(st.pnbinom(q=4, size=6, prob=0.8))

	print(st.qnbinom(p=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], size=9, prob=0.65))


def GeometricDist():
	print(st.dgeom(x=3, prob=0.6))
	print(st.dgeom(x=[0,1,2,3], prob=0.6))

	print("-------------------")

	print(st.pgeom(q=3, prob=0.6))
	print(st.pgeom(q=[0,1,2,3], prob=0.6))

	print("-------------------")

	print(st.qgeom(p=0.5, prob=0.45))
	print(st.qgeom(p=[0,0.1,0.2,0.3, 0.5, 0.7], prob=0.45))


def HyperGeometricDist():
	print(st.dhyper(x=3, m=10, n=4, k=5))
	print(st.phyper(q=3, m=10, n=4, k=5))
	print(st.qhyper(p=[i*0.1 for i in range(10)], m=10, n=4, k=5))



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