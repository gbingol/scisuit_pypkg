import sys, os
import numpy as np

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

import scisuit.fitting as fit
x = [0, 1, 2, 3]
y = [1, -8, -30, -59]

t = fit.spline(x,y)
print(t[0].poly)

print(t)
