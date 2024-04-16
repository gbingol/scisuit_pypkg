import sys, os
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scipy.optimize as opt
from scisuit.roots import brentq, toms748
from timeit import timeit

def f(x):
    return x**2-5

N=1000

print("Scipy functions")
print("brentq:", timeit(lambda: opt.brentq(f=f, a=0, b=5), number=N))
print("toms748:", timeit(lambda: opt.toms748(f=f, a=0, b=5), number=N))

print("scisuit functions")
print("brentq:", timeit(lambda: brentq(f=f, a=0, b=5, tol=1E-16), number=N))
print("toms748:", timeit(lambda: toms748(f=f, a=0, b=5, tol=1E-16), number=N))

print("Root:", toms748(f=f, a=0, b=5, tol=1E-6))