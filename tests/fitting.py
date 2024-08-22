import numpy as np


import scisuit.fitting as fit
x = [0, 1, 2, 3]
y = [1, -8, -30, -59]

t = fit.spline(x,y)
print(t)

time= [0, 2, 5, 8, 10]
T=[20, 25, 30, 28, 22]

print(fit.approx(time, T, 10))


time= [1, 2, 5, 8, 10]
T=[20, 25, 30, 28, 22]

r = fit.expfit(x=time, y=T, intercept=20)
print(r)

r = fit.logfit(x=time, y=T)
print(r)

r = fit.powfit(x=time, y=T)
print(r)
