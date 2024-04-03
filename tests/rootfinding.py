import sys, os
import timeit
import scipy
import scipy.optimize

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from scisuit.roots import bisect, brentq, Info

def func(x):
    return x**2-5



print("Scipy:", timeit.timeit(lambda: scipy.optimize.brentq(f=func, a=0, b=5), number=1000))
print("scisuit:", timeit.timeit(lambda: brentq(f=func, a=0, b=5, tol=1E-16), number=1000))
