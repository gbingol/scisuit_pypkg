import sys, os
import numpy as np

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

import scisuit.fitting as fit
x = [0, 1, 2, 3]
y = [1, -8, -30, -59]

t = fit.spline(x,y)
#print(t[0].poly)

#print(t)

time= [0, 2, 5, 8, 10]
T=[20, 25, 30, 28, 22]

print(fit.approx(time, T, 10))

