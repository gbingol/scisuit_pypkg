import sys, os
import pprint

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from scisuit.roots import bisect, brentq, Info

def func(x):
    return x**2-5

root, info = bisect(f=func, a=0, b=5)

print("**** Bisection method ****")
print(root," ", info)

root, info = brentq(f=func, a=0, b=5)

print("\n **** Brent's method ****")
print(root," ", info)

from scisuit.roots import bisect
root, info = bisect(lambda x: x**2-5, a = 0, b = 4)
print(root, " ",  info)