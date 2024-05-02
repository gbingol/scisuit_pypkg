import numpy as np
from scipy.integrate import solve_ivp

def f(x, y): 
	return -2*x**3 + 12*x**2 - 20*x + 8.5

sol = solve_ivp(f, [0, 4], [1], t_eval=np.arange(0.0, 4.5, 0.5))
print(sol.t)
print(sol.y)