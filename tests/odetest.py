import math
import numpy as np
from scipy.integrate import solve_ivp

from scisuit.ode import euler

def f(x, y): 
	return 4*math.exp(0.8*x)-0.5*y

sol = solve_ivp(f, t_span=[0, 2], y0=[2], t_eval=[0,0.5,1, 2])
print(sol.t)
print(sol.y)

sol2 = euler(f, t_span=[0, 2], y0=2, t_eval=0.1)
print(sol2)