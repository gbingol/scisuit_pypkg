import ctypes as _ct
import dataclasses as _dc
import numbers as _numbers
import types as _types

from ._ctypeslib import pydll as _pydll


@_dc.dataclass
class BracketResult:
	a:float
	b:float
	c:float
	fa:float
	fb:float
	fc:float


def bracket(
	f:_types.FunctionType, 
	xa:_numbers.Real = 0.0, 
	xb:_numbers.Real = 1.0, 
	grow_limit=110,
	maxiter=1000)->BracketResult:
	"""
	Bracket the minimum of a function.
	Returns three points that bracket the minimum of the function.

	## Inputs:
	f: A unary function
	xa, xb: Initial guesses, local minimum need not be contained within this interval.
	grow_limit: Maximum grow limit.
	maxiter: Maximum number of iterations
	"""
	assert isinstance(f, _types.FunctionType), "f must be function"
	assert isinstance(xa, _numbers.Real), "xa must be real number"
	assert isinstance(xb, _numbers.Real), "xb must be real number"
	assert isinstance(grow_limit, _numbers.Real), "grow_limit must be real number"
	assert isinstance(maxiter, int), "maxiter must be int"

	assert maxiter>0, "maxiter>0 expected"

	d:dict =_pydll.c_optimize_bracket(_ct.py_object(f), 
						_ct.c_double(xa), 
						_ct.c_double(xb),
						_ct.c_double(grow_limit),
						_ct.c_uint32(maxiter))
	
	return BracketResult(a=d["a"], b=d["b"], c=d["c"], fa=d["fa"], fb=d["fb"], fc=d["fc"])
