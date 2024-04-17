import sys, os
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scipy.optimize as opt
from scisuit.optimize import bracket

def f(x):
	return 10*x**2 + 3*x + 5

print(opt.bracket(f))
print(bracket(f))