from numbers import Real
from dataclasses import dataclass
from typing import Iterable
from types import FunctionType


from ctypes import py_object, c_double, c_size_t, c_uint8
from ._ctypeslib import pydll as _pydll


_pydll.c_core_ode_euler.argtypes = [py_object, py_object, c_double, py_object]
_pydll.c_core_ode_euler.restype=py_object


_pydll.c_core_ode_heun.argtypes = [py_object, py_object, c_double, py_object, c_size_t]
_pydll.c_core_ode_heun.restype=py_object

_pydll.c_core_ode_rungekutta.argtypes = [py_object, py_object, c_double, py_object, c_uint8]
_pydll.c_core_ode_rungekutta.restype=py_object



#---------------------------------------------------------------------------

@dataclass
class ode_result:
	t:list[Real]
	y:list[Real]
	y0:float

	def __str__(self):
		s = f"Initial value: {self.y0} \n"
		s += f"Function was evaluated at {len(self.t)} nodes. \n"
		s += "Nodes: " + str(self.t) + "\n"
		s += "Values: " + str(self.y) 
		return s



#--------------------------------------------------------------------------------


@dataclass
class result_euler(ode_result):
	def __str__(self):
		s = "Euler's Method \n"
		s += str(super().__str__())
		return s

def euler(fun:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Real, 
		  t_eval:Iterable[Real]|Real = None)->ode_result:
	assert isinstance(fun, FunctionType), "fun must be a function."
	assert isinstance(y0, Real), "y0 must be Real."
	assert isinstance(t_eval, Iterable|Real), "t_eval must be Iterable[Real]|Real"

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	result = _pydll.c_core_ode_euler(fun, t_span, c_double(y0), t_eval)
	return result_euler(t=result["t"], y=result["y"], y0=y0)



#--------------------------------------------------------------------------------


@dataclass
class result_heun(ode_result):
	repeat:int
	def __str__(self):
		s = "Heun's Method \n"
		s += f"Number of repetitions: {self.repeat} \n"
		s += str(super().__str__())
		return s

def heun(fun:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Real, 
		  t_eval:Iterable[Real]|Real = None,
		  repeat:int = 1)->ode_result:
	assert isinstance(fun, FunctionType), "fun must be a function."
	assert isinstance(y0, Real), "y0 must be Real."
	assert isinstance(t_eval, Iterable|Real), "t_eval must be Iterable[Real]|Real"
	assert isinstance(repeat, int) and repeat>=1, "repeat must be an integer >=1."

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	result = _pydll.c_core_ode_heun(fun, t_span, c_double(y0), t_eval, c_size_t(repeat))
	return result_heun(t=result["t"], y=result["y"], y0=y0, repeat=repeat )



#--------------------------------------------------------------------------------


@dataclass
class result_rungekutta(ode_result):
	order:int
	def __str__(self):
		orderstr = str(self.order) + (["nd", "rd", "th", "th"])[self.order-2]
		s = f"{orderstr} order Runge-Kutta Method \n"
		s += str(super().__str__())
		return s

def runge_kutta(fun:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Real, 
		  t_eval:Iterable[Real]|Real = None,
		  order:int = 4)->ode_result:
	assert isinstance(fun, FunctionType), "fun must be a function."
	assert isinstance(y0, Real), "y0 must be Real."
	assert isinstance(t_eval, Iterable|Real), "t_eval must be Iterable[Real]|Real"
	assert isinstance(order, int) and 2<=order<=5, "order must be an integer in [2, 5]."

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	result = _pydll.c_core_ode_rungekutta(fun, t_span, c_double(y0), t_eval, c_uint8(order))
	return result_rungekutta(t=result["t"], y=result["y"], y0=y0, order=order)