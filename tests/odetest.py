import math
import numpy as np
from scipy.integrate import solve_ivp as scisolve

from scisuit.ode import solve_ivp


"""

sol = solve_ivp(f, t_span=[0, 4], y0=[2], t_eval=teval)
print(sol.t)
print(sol.y)

print("--------------")

sol_euler = euler(f, t_span=[0, 2], y0=2, t_eval=teval)
print(sol_euler)

print("--------------")

sol_heun = heun(f, t_span=[0, 2], y0=2, t_eval=teval, repeat=15)
print(sol_heun)


"""
teval = [0,1,2,3,4]

def f(x, y): 
	return 4*math.exp(0.8*x)-0.5*y


def f_stiff(x, y):
	#solution for y(0)=0, y(x) = -(997*e^(-1000*x))/999 - (2000*e^(-x))/999 + 3
	return -1000*y + 3000 - 2000*math.exp(-x)


def f_system(t, y):
	y1, y2 = y
	dydt = [-0.5*y1, 4-0.3*y2-0.1*y1]  # dy1/dt = -0.5*y1, dy2/dt =4-0.3*y2-0.1*y1
	return dydt

def f_system_stiff(t, y):
	"""
	Solution set:
	y1 = 52.96*math.exp(3.9899*t) - 0.67*math.exp(-302.0101*t)
	y2 = 17.83*math.exp(-3.9899*t) + 65.99*math.exp(-302.0101*t)
	"""
	y1, y2 = y
	dydt = [-5*y1+3*y2, 100*y1-301*y2]  # dy1/dt = -5*y1+3*y2, dy2/dt =100*y1-301*y2
	return dydt

"""

solset_rk = solve_ivp(f_system, [0,2], [4,6], t_eval=0.5, method="rk5")
print(solset_rk)


print("--------------")

sol_rk = solve_ivp(f, t_span=[0, 2], y0=2, t_eval=teval, method="rk5")
print(sol_rk)


print("--------------")

sol_adaprk = solve_ivp(f, t_span=[0, 4], y0=2)
print(sol_adaprk)

"""

"""
sol_stiff = solve_ivp(f_stiff, [0,2], y0=0, t_eval=0.05, method="euler_s")
print(sol_stiff)
"""

sol_stiff = scisolve(f_system_stiff, [0,2], y0=[52.29, 83.82], t_eval=[0, 0.05, 0.1], method="RK45")
print(sol_stiff)

sol_stiff = solve_ivp(f_system_stiff, [0,2], y0=[52.29, 83.82], t_eval=[0, 0.05, 0.1], method="euler_s")
print(sol_stiff)