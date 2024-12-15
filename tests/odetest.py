import math
import numpy as np
from scipy.integrate import solve_ivp

from scisuit.ode import euler, heun, runge_kutta, runge_kutta45

def f(x, y): 
	return 4*math.exp(0.8*x)-0.5*y


teval = [0,1,2,3,4]

sol = solve_ivp(f, t_span=[0, 4], y0=[2], t_eval=teval)
print(sol.t)
print(sol.y)

print("--------------")

sol_euler = euler(f, t_span=[0, 2], y0=2, t_eval=teval)
print(sol_euler)

print("--------------")

sol_heun = heun(f, t_span=[0, 2], y0=2, t_eval=teval, repeat=15)
print(sol_heun)


print("--------------")

sol_rk = runge_kutta(f, t_span=[0, 2], y0=2, t_eval=teval, order=5)
print(sol_rk)


print("--------------")

sol_adaprk = runge_kutta45(f, t_span=[0, 4], y0=2)
print(sol_adaprk)