import sys, os
import pprint
import numpy as np

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.stats as st



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



def dmultinom():
	from scisuit.stats import dmultinom

	probs = [1/21*i for i in range(1,7)]
	x=[2]*6

	p = dmultinom(x=x, size=12, prob=probs)
	print(f"probability={p}")


def rmultinom():
	from scisuit.stats import rmultinom

	n=10

	#testing probabilities
	p = np.array([0.05, 0.15, 0.30, 0.50 ])

	#2D array
	arr = np.array(rmultinom(n=1000, size=10, prob=p))

	#means of each 1000 numbers with probabilities 0.05, 0.15 ...
	means = np.mean(arr, axis=1)

	#expected value (n*p[i])
	E_X = n*p

	print(f"Difference = {means - E_X}")


def weibull():
	print(st.dweibull(x=3, shape=2, scale=4))
	print(st.pweibull(q=3, shape=2, scale=4))
	print(st. qweibull(p=0.3, shape=2, scale=4))


def gamma_weibull_scale():
	import matplotlib.pyplot as plt
	from scisuit.stats import dgamma, dweibull

	figure, axis = plt.subplots(nrows=2, ncols=1)

	axis[0].set_title("Gamma")
	axis[1].set_title("Weibull")


	x=np.linspace(0, 7, num=100)

	for beta in [0.5, 1, 2, 4]:
		axis[0].plot(x, dgamma(x=x, shape=2, scale=beta), label=str(beta))
		axis[1].plot(x, dweibull(x=x, shape=2, scale=beta), label=str(beta))

	axis[0].legend()
	axis[1].legend()
	plt.tight_layout()
	plt.show()


def gamma_weibull_shape():
	import matplotlib.pyplot as plt
	from scisuit.stats import dgamma, dweibull

	figure, axis = plt.subplots(nrows=2, ncols=1)

	axis[0].set_title("Gamma")
	axis[1].set_title("Weibull")


	x=np.linspace(0.1, 7, num=100)

	for alpha in [0.6, 1, 3]:
		axis[0].plot(x, dgamma(x=x, shape=alpha, scale=1), label=str(alpha))
		axis[1].plot(x, dweibull(x=x, shape=alpha, scale=1), label=str(alpha))

	axis[0].legend()
	axis[1].legend()
	plt.tight_layout()
	plt.show()



from scisuit.stats import dbeta, pbeta, qbeta

print(dbeta(x=0.1, shape1=0.5, shape2=1))
print(pbeta(q=0.1, shape1=0.5, shape2=1))
print(qbeta(p=0.1, shape1=0.5, shape2=1))

