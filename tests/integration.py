import sys, os
import numpy as np

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from scisuit.integ import simpson, romberg, fixed_quad, cumtrapz
from numpy import trapezoid

#Discrete data
x=np.linspace(0, 3, num=20)
y = x**2

print(f"Trapz: {trapezoid(x,y)}")
print(f"Cumtrapz: {cumtrapz(x,y)}")
print(f"Simpson: {simpson(x, y)}")

print("\n------------- \n")

#Function
f = lambda x: x**2

print(f"Romberg: {romberg(f= f, a=0, b=3)}")
print(f"Fixed quad n=3: {fixed_quad(f=f, a=0, b=3, n=3)}")