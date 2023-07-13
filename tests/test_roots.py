import sys, os
import pprint

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from scisuit.roots import bisect, brentq

def func(x):
    return x**2-5

rbi = bisect(f=func, a=0, b=5)
rbq = brentq(f=func, a=0, b=5)

print("**** Bisection method ****\n")
print(rbi)

print("\n **** Brent's method ****\n")
print(rbq)