from numbers import Real
from dataclasses import dataclass
from typing import Iterable
from types import FunctionType


from ctypes import py_object, c_double, c_size_t
from ._ctypeslib import pydll as _pydll


_pydll.c_core_ode_euler.argtypes = [py_object, py_object, c_double, py_object]
_pydll.c_core_ode_euler.restype=py_object


_pydll.c_core_ode_heun.argtypes = [py_object, py_object, c_double, py_object, c_size_t]
_pydll.c_core_ode_heun.restype=py_object



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
		s = "Euler's method \n"
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
		s = "Heun's method \n"
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