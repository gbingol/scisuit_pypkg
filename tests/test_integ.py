import sys, os
import numpy as np

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from scisuit import trapz, cumtrapz

x = np.arange(1,6)
y = x**2

print(cumtrapz(x, y))



x=np.linspace(0, 3, num=100)
y = x**2

print(trapz(x,y))