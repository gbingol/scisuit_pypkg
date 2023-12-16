import sys, os
import numpy as np

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from scisuit.integ import trapz, cumtrapz, simpson, romberg, fixed_quad

x = np.arange(1, 6)
y = x**2

print("****** cumtrapz ******")
print(cumtrapz(x, y))


x=np.linspace(0, 3, num=100)
y = x**2

print(trapz(x,y))
print(simpson(x, y))
print(romberg(lambda x: x**2, 0, 3))
print(fixed_quad(lambda x: x**2, 0, 3))