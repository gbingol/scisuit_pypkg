from numbers import Real
from dataclasses import dataclass
from typing import Iterable
from types import FunctionType


from ctypes import py_object, c_double
from ._ctypeslib import pydll as _pydll


_pydll.c_core_ode_euler.argtypes = [py_object, py_object, c_double, py_object, py_object]
_pydll.c_core_ode_euler.restype=py_object


#---------------------------------------------------------------------------

@dataclass
class ode_result:
	t:list[Real]
	y:list[Real]



def euler(fun:FunctionType, 
		  t_span:Iterable[Real], 
		  y0:Real, 
		  t_eval:Iterable[Real]|Real = None)->ode_result:
	assert isinstance(fun, FunctionType), "fun must be a function."
	assert isinstance(y0, Real), "y0 must be Real."

	_tspan = [v for v in t_span if isinstance(v, Real)]
	assert len(_tspan) == 2, "t_span must contain exactly two real numbers."

	if isinstance(t_eval, Iterable):
		result = _pydll.c_core_ode_euler(fun, t_span, c_double(y0), None, t_eval)
	else:
		result = _pydll.c_core_ode_euler(fun, t_span, c_double(y0), t_eval, None)

	return ode_result(t=result["t"], y=result["y"])

