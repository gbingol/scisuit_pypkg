import math
import pathlib

from timeit import timeit
import scipy.optimize as opt
from scisuit.optimize import bracket, golden, brent, parabolic

def f1(x):
	return 10*x**2 + 3*x + 5

def f2(x):
	return (x-1)**2

#maximum
def f3(x):
	return -(2*math.sin(x) -x**2/10)

def performance(f, n=1000):
	print(
		"Scipy", "\n",
		"bracket:", timeit(lambda: opt.bracket(f), number=n), "\n", 
		"golden:", timeit(lambda: opt.golden(f), number=n), "\n",
		"brent:", timeit(lambda: opt.brent(f), number=n))

	print("----------------------")

	print(
		"scisuit", "\n",
		"bracket:", timeit(lambda: bracket(f), number=n), "\n",
		"golden:", timeit(lambda: golden(f, xlow=-2, xhigh=4, tol=1E-9), number=n), "\n", 
		"brent:", timeit(lambda: brent(f, xlow=-2, xhigh=4), number=n))


performance(f1)
performance(f2)
