import math
import numpy as np
from scipy.integrate import solve_ivp

def f(x, y): 
	return 4*math.exp(0.8*x)-0.5*y

sol = solve_ivp(f, [0, 2], [2])
print(sol.t)
print(sol.y)