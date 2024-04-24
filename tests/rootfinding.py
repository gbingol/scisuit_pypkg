import sys, os
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scipy.optimize as opt
from scisuit.roots import brentq, toms748
from timeit import timeit

def performance():
	kwargs, N = {"f": lambda x: x**2-5, "a":0, "b":5}, 1000

	print("Scipy functions")
	print("brentq:", timeit(lambda: opt.brentq(**kwargs), number=N))
	print("toms748:", timeit(lambda: opt.toms748(**kwargs), number=N))

	print("scisuit functions")
	print("brentq:", timeit(lambda: brentq(**kwargs, tol=1E-16), number=N))
	print("toms748:", timeit(lambda: toms748(**kwargs, tol=1E-16), number=N))


f1 = {
	"f":lambda x: x**2 - (1-x)**9,
	"fprime": lambda x: 2*x + 9*(1-x)**8,
	"fprime2": lambda x: 2 - 72*(1-x)**7
}

f2 = {
	"f":lambda x: 1/8 * (9 - 1/x),
	"fprime": lambda x: 1 /(8*x**2),
	"fprime2": lambda x: -1/(4*x**3)
}


from scisuit.roots import newton, itp, bisect

print(itp(f=lambda x: x**2-5, a=0, b=3))
print(bisect(f=lambda x: x**2-5, a=0, b=3))

print("-----------------------")

x0,  x1 = -1.4, 1
print(newton(f=f1["f"], x0=x0, x1=x1))
print(newton(f=f1["f"], x0=x0, fprime=f1["fprime"]))
print(newton(f=f1["f"], x0=x0, fprime=f1["fprime"], fprime2=f1["fprime2"]))

print("-----------------------")

x0, x1 = 0.001, 0.25
print(newton(f=f2["f"], x0=x0, x1=x1))
print(newton(f=f2["f"], x0=x0, fprime=f2["fprime"]))
print(newton(f=f2["f"], x0=x0, fprime=f2["fprime"], fprime2=f2["fprime2"]))