from dataclasses import dataclass
from numbers import Real
from types import FunctionType
from typing import Iterable

from numpy import array, arange, float64


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
		_s0 = "s were" if isinstance(self.y0, list) else " was"
		s = f"Initial value: {self.y0} \n"
		s += f"Function{_s0} evaluated at {len(self.t)} nodes. \n"
		s += "Nodes: " + str(self.t) + "\n"
		s += "Values: " + str(self.y) 
		return s






#---------------------------------------------------------------------------
#-----------------------------  Euler's Method  ----------------------------------------


@dataclass
class result_euler(ode_result):
	def __str__(self):
		s = "Euler's Method " + ("for Set of Equations \n" if isinstance(self.y0, Iterable) else " \n")
		s += str(super().__str__())
		return s



def __euler_single(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Real, 
		  t_eval:Iterable[Real]|Real = None)->result_euler:
	
	result = _pydll.c_core_ode_euler(f, t_span, c_double(y0), t_eval)
	return result_euler(t=result["t"], y=result["y"], y0=y0)




def __euler_set(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Iterable[Real], 
		  t_eval:Iterable[Real]|Real = None)->result_euler:
	
	Nodes = arange(t_span[0], t_span[1] + t_eval, t_eval) if isinstance(t_eval, Real) else array(t_eval)

	y = array(y0, dtype=float64)
	yvals = [y.tolist()]
	for i in range(1, len(Nodes)):
		h = float(Nodes[i]-Nodes[i-1])
		slopes = array(f(float(Nodes[i]), y.tolist()), dtype=float64)
		y += slopes*h
		
		yvals.append(y.tolist())
	
	return result_euler(t=Nodes, y=yvals, y0=y0)




def euler(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Iterable[Real] | Real, 
		  t_eval:Iterable[Real]|Real)->result_euler:
	"""
	Solve ODE or set of ODEs using Euler's Method 

	---
	f: function of f(t,y).  
	t_span: The interval wherein the solution is desired.  
	y0: Initial condition(s).  
	t_eval: Specific nodes at which the solution is desired or step size.
	"""
	assert isinstance(f, FunctionType), "f must be a function."
	assert isinstance(y0, Iterable|Real), "y0 must be Iterable[Real] | Real."
	assert isinstance(t_eval, Iterable|Real), "t_eval must be Iterable[Real] | Real"

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."
	assert t_span[1]>t_span[0], "t_span=[a, b] where b>a expected."

	if isinstance(y0, Real):
		return __euler_single(f, t_span, y0, t_eval)
	
	return __euler_set(f, t_span, y0, t_eval)





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
		  t_eval:Iterable[Real]|Real,
		  repeat:int = 1)->result_heun:
	"""
	Solve ODE or set of ODEs using Heun's Method 

	---
	f: function f(t,y).  
	t_span: The interval wherein the solution is desired.  
	y0: Initial condition.  
	t_eval: Specific nodes at which the solution is desired or step size.  
	repeat: The number times the prediction-correction cycle should be performed.
	"""
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


def __rungekutta2(fun, t, y, h):
	k1 = array(fun(t, y), dtype=float64)
	k2 = array(fun(t + 3.0 / 4.0 * h, y + 3.0 / 4.0 * h * k1), dtype=float64)

	return (1.0 / 3.0 * k1 + 2.0 / 3.0 * k2) * h


def __rungekutta3(fun, t, y, h):
	k1 = array(fun(t, y), dtype=float64)
	k2 = array(fun(t + 1.0 / 2.0 * h, y + 1.0 / 2.0 * h * k1), dtype=float64)
	k3 = array(fun(t + h, y - k1 * h + 2.0 * k2 * h), dtype=float64)

	return h / 6.0 * (k1 + 4.0 * k2 + k3)

def __rungekutta4(fun, t, y, h):
	k1 = array(fun(t, y), dtype=float64)
	k2 = array(fun(t + 1.0 / 2.0 * h, y + 1.0 / 2.0 * h * k1), dtype=float64)
	k3 = array(fun(t + 1.0 / 2.0 * h, y + 1.0 / 2.0 * h * k2), dtype=float64)
	k4 = array(fun(t + h, y + k3 * h), dtype=float64)

	return 1/6*(k1 + 2*k2 + 2*k3 + k4)*h


def __rungekutta5(fun, t, y, h):
	k1 = array(fun(t, y), dtype=float64)
	k2 = array(fun(
		t + 1.0 / 4.0 * h, 
		y + 1.0 / 4.0 * h * k1), 
		dtype=float64)
	k3 = array(fun(
		t + 1.0 / 4.0 * h, 
		y + 1.0 / 8.0 * h * k1 + 1.0 / 8.0 * h * k2), 
		dtype=float64)
	k4 = array(fun(
		t + 1.0 / 2.0 * h, 
		y - 1.0 / 2.0 * h * k2 + h * k3), 
		dtype=float64)
	k5 = array(fun(
		t + 3.0 / 4.0 * h, 
		y + 3.0 / 16.0 * h * k1 + 9.0 / 16.0 * h * k4), 
		dtype=float64)
	k6 = array(fun(
		t + h, 
		y - 3.0 / 7.0 * k1 * h + 2.0 / 7.0 * k2 * h + 12.0 / 7.0 * k3 * h - 12.0 / 7.0 * k4 * h + 8.0 / 7.0 * k5 * h), 
		dtype=float64)
		
	return h / 90.0 * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)



@dataclass
class result_rungekutta(ode_result):
	order:int
	def __str__(self):
		orderstr = str(self.order) + (["nd", "rd", "th", "th"])[self.order-2]
		s = f"{orderstr} order Runge-Kutta Method \n"
		s += str(super().__str__())
		return s


def __runge_kutta_single(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Real, 
		  t_eval:Iterable[Real]|Real = None,
		  order:int = 4)->result_rungekutta:

	result = _pydll.c_core_ode_rungekutta(f, t_span, c_double(y0), t_eval, c_uint8(order))
	return result_rungekutta(t=result["t"], y=result["y"], y0=y0, order=order)



def __runge_kutta_set(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Iterable[Real], 
		  t_eval:Iterable[Real]|Real = None,
		  order:int = 4)->result_rungekutta:

	func = [__rungekutta2, __rungekutta3, __rungekutta4, __rungekutta5][order-2]

	x = arange(t_span[0], t_span[1] + t_eval, t_eval) if isinstance(t_eval, Real) else array(t_eval)
	y = array(y0, dtype=float64)

	yvals = [y.tolist()]

	k = f(x[0], y)
	for i in range(1, len(x)):
		h = float(x[i]-x[i-1])
		y += func(f, x[i], array(y, dtype=float64), h)
		
		yvals.append(y.tolist())
	
	return result_rungekutta(t=x, y=yvals, y0=y0, order=4)



def runge_kutta(f:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Iterable[Real] | Real, 
		  t_eval:Iterable[Real]|Real,
		  order:int = 4)->result_rungekutta:
	"""
	Solve ODE or set of ODEs using Runge-Kutta Method 

	---
	f: function of f(t,y).  
	t_span: The interval wherein the solution is desired.  
	y0: Initial condition(s).  
	t_eval: Specific nodes at which the solution is desired or step size.
	order: Order of Runge-Kutta method in [2, 5]
	"""
	assert isinstance(f, FunctionType), "f must be a function."
	assert isinstance(y0, Iterable|Real), "y0 must be Iterable[Real] | Real."
	assert isinstance(t_eval, Iterable|Real), "t_eval must be Iterable[Real] | Real"
	assert isinstance(order, int) and 2<=order<=5, "order must be an integer in [2, 5]."

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."
	assert t_span[1]>t_span[0], "t_span=[a, b] where b>a expected."

	if isinstance(y0, Real):
		return __runge_kutta_single(f, t_span, y0, t_eval, order=order)
	
	return __runge_kutta_set(f, t_span, y0, t_eval, order)





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
	"""
	Solve ODE using Adaptive Runge-Kutta Method 

	---
	f: function of f(t,y).  
	t_span: The interval wherein the solution is desired.  
	y0: Initial condition.
	"""
	assert isinstance(f, FunctionType), "f must be a function."
	assert isinstance(y0, Real), "y0 must be Real."

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	t, t_end = t_span
	y = array([y0], dtype=float)
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