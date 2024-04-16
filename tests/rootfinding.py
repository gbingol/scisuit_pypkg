import sys, os
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scipy.optimize as opt
from scisuit.roots import brentq, toms748
from timeit import timeit


kwargs, N = {"f": lambda x: x**2-5, "a":0, "b":5}, 1000

print("Scipy functions")
print("brentq:", timeit(lambda: opt.brentq(**kwargs), number=N))
print("toms748:", timeit(lambda: opt.toms748(**kwargs), number=N))

print("scisuit functions")
print("brentq:", timeit(lambda: brentq(**kwargs, tol=1E-16), number=N))
print("toms748:", timeit(lambda: toms748(**kwargs, tol=1E-16), number=N))

print("Root:", toms748(**kwargs, tol=1E-6))