from dataclasses import dataclass
from numbers import Real
from types import FunctionType
from typing import Iterable

import numpy as np


from ctypes import c_double, c_size_t, c_uint8, py_object
from ._ctypeslib import pydll as _pydll

_pydll.c_core_ode_euler.argtypes = [py_object, py_object, c_double, py_object]
_pydll.c_core_ode_euler.restype=py_object


_pydll.c_core_ode_heun.argtypes = [py_object, py_object, c_double, py_object, c_size_t]
_pydll.c_core_ode_heun.restype=py_object

_pydll.c_core_ode_rungekutta.argtypes = [py_object, py_object, c_double, py_object, c_uint8]
_pydll.c_core_ode_rungekutta.restype=py_object






#------------------------------------------------------------------------------
#----------------------------- Base Ode Result  -----------------------------------

@dataclass
class ode_result:
	t:list[Real]
	y:list[Real]
	y0:list[Real]

	def __str__(self):
		s = f"Initial value: {self.y0} \n"
		s += f"Function was evaluated at {len(self.t)} nodes. \n"
		s += "Nodes: " + str(self.t) + "\n"
		s += "Values: " + str(self.y) 
		return s






#---------------------------------------------------------------------------
#-----------------------------  Euler's Method  ----------------------------------------


@dataclass
class result_euler(ode_result):
	def __str__(self):
		s = "Euler's Method for Set of Equations \n"
		s += str(super().__str__())
		return s

def euler(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Real, 
		  t_eval:Iterable[Real]|Real = None)->result_euler:
	assert isinstance(f, FunctionType), "f must be a function."
	assert isinstance(y0, Real), "y0 must be Real."
	assert isinstance(t_eval, Iterable|Real), "t_eval must be Iterable[Real]|Real"

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	result = _pydll.c_core_ode_euler(f, t_span, c_double(y0), t_eval)
	return result_euler(t=result["t"], y=result["y"], y0=y0)






#--------------------------------------------------------------------------------
#---------------------------   Heun's Method  --------------------------------------


@dataclass
class result_heun(ode_result):
	repeat:int
	def __str__(self):
		s = "Heun's Method \n"
		s += f"Number of repetitions: {self.repeat} \n"
		s += str(super().__str__())
		return s

def heun(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Real, 
		  t_eval:Iterable[Real]|Real = None,
		  repeat:int = 1)->result_heun:
	assert isinstance(f, FunctionType), "f must be a function."
	assert isinstance(y0, Real), "y0 must be Real."
	assert isinstance(t_eval, Iterable|Real), "t_eval must be Iterable[Real]|Real"
	assert isinstance(repeat, int) and repeat>=1, "repeat must be an integer >=1."

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	result = _pydll.c_core_ode_heun(f, t_span, c_double(y0), t_eval, c_size_t(repeat))
	return result_heun(t=result["t"], y=result["y"], y0=y0, repeat=repeat )




#------------------------------------------------------------------------------------------------
#----------------------------Runge-Kutta Different Orders -----------------------------------------------


@dataclass
class result_rungekutta(ode_result):
	order:int
	def __str__(self):
		orderstr = str(self.order) + (["nd", "rd", "th", "th"])[self.order-2]
		s = f"{orderstr} order Runge-Kutta Method \n"
		s += str(super().__str__())
		return s

def runge_kutta(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Real, 
		  t_eval:Iterable[Real]|Real = None,
		  order:int = 4)->result_rungekutta:
	assert isinstance(f, FunctionType), "fun must be a function."
	assert isinstance(y0, Real), "y0 must be Real."
	assert isinstance(t_eval, Iterable|Real), "t_eval must be Iterable[Real]|Real"
	assert isinstance(order, int) and 2<=order<=5, "order must be an integer in [2, 5]."

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	result = _pydll.c_core_ode_rungekutta(f, t_span, c_double(y0), t_eval, c_uint8(order))
	return result_rungekutta(t=result["t"], y=result["y"], y0=y0, order=order)






#---------------------------------------------------------------------------
#-----------------------    Adaptive RK45  -----------------------------

def __rk45_step(func, x,y, h=0.1,  atol=1E-6, rtol=1E-3):
	k1 = func(x, y)
	k2 = func(
		x + 1.0/5.0*h, 
		y + 1.0/5.0*k1*h)
	k3 = func(
		x + 3.0/10.0*h, 
		y + 3.0/40.0*k1*h + 9.0/40.0*k2*h)
	k4 = func(
		x + 3.0/5.0*h, 
		y + 3.0/10.0*k1*h -9.0/10.0*k2*h + 6.0/5.0*k3*h )
	k5 = func(
		x + h, 
		y - 11.0/54.0*k1*h + 5.0/2.0*k2*h - 70.0/27.0*k3*h + 35.0/27.0*k4*h)
	k6 = func(
		x + 7.0/8.0*h, 
		y + 1631.0/55296.0*k1*h + 175.0/512.0*k2*h + 575.0/13824.0*k3*h + 44275.0/110592.0*k4*h + 253.0/4096.0*k5*h)

	#4th order estimate
	y4 = y + (37.0/378.0*k1 + 250.0/621.0*k3 + 125.0/594.0*k4 + 512.0/1771.0*k6)*h

	#5th order estimate
	y5 = y + (2825.0/27648.0*k1 + 18575.0/48384.0*k3 + 13525.0/55296.0*k4 + 277.0/14336.0*k5 + 1.0/4.0*k6)*h

	err = abs(y5 - y4)
	tol = atol + rtol * abs(y)
	error_ratio = max(err / tol)
	
	# Accept or reject the step
	if error_ratio <= 1:
		t_new = x + h
		y_new = y5  # Use higher-order solution
		h_new = h * min(2.0, max(0.1, 0.9 * error_ratio**-0.2))
	else:
		# Step is too large, recompute
		t_new = x
		y_new = y
		h_new = h * min(5.0, max(0.1, 0.8 * error_ratio**-0.2))

	return t_new, y_new, h_new


@dataclass
class result_rungekutta45(ode_result):
	def __str__(self):
		s = f"Adaptive Runge-Kutta (45) Method \n"
		s += str(super().__str__())
		return s


def runge_kutta45(
		f:FunctionType, 
		t_span:Iterable[Real], 
		y0:Real, 
		h0=0.1)->result_rungekutta45:
	assert isinstance(f, FunctionType), "f must be a function."
	assert isinstance(y0, Real), "y0 must be Real."

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	t, t_end = t_span
	y = np.array([y0], dtype=float)
	h = h0

	t_values = [t]
	y_values = [float(y[0])]

	while t < t_end:
		if t + h > t_end:
			h = t_end - t  # Adjust final step to reach t_end
		t, y, h = __rk45_step(f, t, y, h)
		t_values.append(float(t))
		y_values.append(float(y))

	return result_rungekutta45(t=t_values, y=y_values, y0=y0)
	



#------------------------------------------------------------------------
#-----------------------------------------------------------------------



#--------------------------------------------------------------------------------
#---------------------------   Euler's Method for Set of Eq --------------------------------------



@dataclass
class result_euler_set(ode_result):
	def __str__(self):
		s = "Euler's Method \n"
		s += str(super().__str__())
		return s

def euler_set(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:list[Real], 
		  t_eval:Iterable[Real]|Real = None)->result_euler_set:
	assert isinstance(f, FunctionType), "f must be a function."
	assert isinstance(y0, Iterable), "y0 must be Iterable."
	assert isinstance(t_eval, Iterable|Real), "t_eval must be Iterable[Real]|Real"

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	tEvalNodes = np.arange(t_span[0], t_span[1] + t_eval, t_eval) if isinstance(t_eval, Real) else np.array(t_eval)

	y = np.array(y0, dtype=np.float64)
	yvals = [y.tolist()]
	for i in range(1, len(tEvalNodes)):
		h = float(tEvalNodes[i]-tEvalNodes[i-1])
		slopes = np.array(f(float(tEvalNodes[i]), y.tolist()), dtype=np.float64)
		y += slopes*h
		
		yvals.append(y.tolist())
	
	return result_euler_set(t=tEvalNodes, y=yvals, y0=y0)
