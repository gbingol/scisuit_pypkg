import sys, os
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from timeit import timeit
import scipy.optimize as opt
from scisuit.optimize import bracket, golden, brent, parabolic

def f(x):
	return 10*x**2 + 3*x + 5

def f2(x):
	return (x-1)**2

#maximum
def f3(x):
	return -(2*math.sin(x) -x**2/10)

def performance():
	n = 1000

	print("Scipy")
	print("bracket:", timeit(lambda: opt.bracket(f2), number=n))
	print("golden:", timeit(lambda: opt.golden(f2), number=n))

	print("----------------------")

	print("scisuit")
	print("bracket:", timeit(lambda: bracket(f2), number=n))
	print("golden:", timeit(lambda: golden(f2, xlow=-2, xhigh=4, tol=1E-9), number=n))



print(opt.bracket(f2))
print(bracket(f2))

print(opt.golden(f2, brack=(2,4)))
print(golden(f2, xlow=-2, xhigh=4, tol=1E-9))

print(opt.brent(f3, full_output=True))
print(brent(f3, xlow=-2, xhigh=4))

print(parabolic(f3, xa=10, xb=4))