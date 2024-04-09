import sys, os
from timeit import timeit
import scipy.optimize as opt
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from scisuit.roots import bisect, brentq, Info, toms748


def func(x):
    return x**2-5

N=1000

print("Scipy functions")
print("brentq:", timeit(lambda: opt.brentq(f=func, a=0, b=5), number=N))
print("toms748:", timeit(lambda: opt.toms748(f=func, a=0, b=5), number=N))

print("\n-------------\n")

print("scisuit functions")
print("brentq:", timeit(lambda: brentq(f=func, a=0, b=5, tol=1E-16), number=N))
print("toms748:", timeit(lambda: toms748(f=func, a=0, b=5, tol=1E-16), number=N))

print(toms748(f=func, a=0, b=5, tol=1E-6))
print(math.sqrt(5))