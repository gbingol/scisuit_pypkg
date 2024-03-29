from ._ctypeslib import pydll as _pydll
import ctypes as _ct
import numbers as _numbers
import types as _types
import numpy as _np
import dataclasses as _dc
import sys as _sys


__all__ = ['bisect', 'brentq', 'muller', 'newton', 'ridder', 'fsolve', "Info"]


@_dc.dataclass
class Info:
	"""
	err: error (if available)
	iter: number of iterations to reach the root
	conv: whether converged to a root or not
	msg: if convergence is False, a reason is given
	"""
	err:float = None
	iter:int = -1
	conv:bool = False
	msg:str =""



def bisect(
	f:_types.FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100, 
	method="bf", 
	modified=False)->tuple[float, Info]:
	"""
	Finds the root using bisection method, returns (root, Info)

	## Inputs:
	f: A unary function
	a, b: The interval where the root lies in
	tol: tolerance for error
	maxiter: Maximum number of iterations
	method: "bf" for brute-force (halving) 
	"rf" for regula falsi (false position) 
	modified: True for modified regula falsi method.
	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"

	root, lst =_pydll.c_root_bisect(f, _ct.c_double(a), _ct.c_double(b), 
			_ct.c_double(tol), 
			_ct.c_int(maxiter), 
			_ct.c_char_p(method.encode('utf-8')),
			_ct.c_bool(modified))
	
	return root, Info(lst[0], lst[1], lst[2], lst[3])




def brentq(
	f:_types.FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100)->tuple[float, Info]:
	"""
	Uses the Brent's method (1973) to find the root of the function 
	using inverse quadratic interpolation, returns (root, Info)

	## Inputs:
	f: A unary function whose root is sought after \n
	a, b: The interval where root lies in \n
	tol: tolerance for error \n
	maxiter: Maximum number of iterations during the search for the root
	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"

	root, lst = _pydll.c_root_brentq(f, _ct.c_double(a), _ct.c_double(b), _ct.c_double(tol), _ct.c_int(maxiter))

	return root, Info(None, lst[0], lst[1], lst[2])




def muller(
	f:_types.FunctionType, 
	x0:_numbers.Complex, 
	h=None, 
	x1=None, 
	x2=None, 
	tol=1E-5, 
	maxiter=100)->tuple[float, Info]:
	"""
	Finds root of an equation using Muller method, returns (root, Info)
	## Inputs:
	f: A unary function \n
	x0, x1, x2:	Initial guesses \n
	h: Step length \n
	tol: tolerance for error \n
	maxiter: Max number of iterations
	"""
	assert callable(f), "f must be function"
	assert isinstance(x0, _numbers.Complex), "x0 must be a Complex/Real number"
	
	root, lst = _pydll.c_root_muller(f, x0, h, x1, x2, _ct.c_double(tol), _ct.c_int(maxiter))

	return root, Info(None, lst[0], lst[1], lst[2])



def newton(
	f:_types.FunctionType, 
	x0:float, 
	x1=None, 
	fprime=None, 
	tol=1E-5, 
	maxiter=100)->tuple[float, Info]:
	"""
	If fprime is provided then uses Newton-Raphson method  \n
	If fprime is not provided, then x1 must be provided uses Secant method.

	returns (root, Info)

	## Inputs:
	f: A unary function 
	fprime: derivative of f 
	x0, x1: Initial guesses 
	tol: tolerance for error 
	maxiter: Max number of iterations
	"""
	assert callable(f), "f must be function"
	assert isinstance(x0, _numbers.Real)
	if(fprime == None):
		assert isinstance(x1, _numbers.Real), "If fprime not provided, x1 must be a real number"
	else:
		assert callable(fprime), "If fprime is provided, it must be of type function."

	root, lst = _pydll.c_root_newton(f, _ct.c_double(x0), x1, fprime, _ct.c_double(tol), _ct.c_int(maxiter))

	return root, Info(lst[0], lst[1], lst[2], lst[3])




def ridder(
	f:_types.FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100)->tuple[float, Info]:
	"""
	Uses Ridder's method.

	## Inputs:
	f: A unary function 
	a, b: The interval where the root lies in 
	tol: tolerance for error 
	maxiter: Maximum number of iterations
	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"
	
	root, lst = _pydll.c_root_ridder(f, _ct.c_double(a), _ct.c_double(b), _ct.c_double(tol), _ct.c_int(maxiter))

	return root, Info(None, lst[0], lst[1], lst[2])




def fsolve(
		F:list[_types.FunctionType], 
		x0:list[float], 
		tol=1E-5, 
		maxiter=100 )->tuple:
	"""
	Solves a system of non-linear equations using Newton's approach. \n
	Functions are in the format of f(x1,x2,...)=0
	

	## Inputs:
	F: a list of functions \n
	x0: a list of initial guesses \n


	## EXAMPLE
	x^2 + y^2 = 5 \n
	x^2 - y^2 = 1 \n

	First define the functions, F(x, y) = 0: \n

	def f1(t): \n
		return t[0]**2 + t[1]**2 - 5 \n

	def f2(t): \n
		return t[0]**2 - t[1]**2 - 1 \n
	\n
	roots, iter=fsolve( [f1,f2], [1,1] ) \n
	\n
	print(roots, "  iter:", iter) \n
	1.73205	1.41421	iter:5 \n

	print(f1(roots), " ", f2(roots)) \n
	9.428e-09    9.377e-09 
	
	"""
	assert isinstance(F, list), "F must be a list of functions"
	assert isinstance(x0, list), "x0 must be a list of numbers"

	assert isinstance(tol, _numbers.Number) and tol>0, "tol>0 expected."
	assert isinstance(maxiter, int) and maxiter>0, "maxiter>0 expected."

	dim = len(F)

	assert dim>=2, "At least 2 functions are required"
	assert dim == len(x0), "F and x0 must have same length"


	#solution vector as floating point
	v = _np.asfarray(x0)
      
	#values of each function	
	Fvals = _np.zeros(dim)

	Jacobi = _np.zeros((dim, dim)) 

	for iter in range(maxiter):
		maxfuncval = 0 #convergence criteria
	
		for i in range(dim):
			func = F[i]     #function

			assert isinstance(func, _types.FunctionType), "Entries of F must be functions of form f(t) = 0"
			
			Fvals[i] = func(v.tolist())
		
			for j in range(dim):
				oldval = v[j]
				
				#Note that vector contains (xi+dx,...)
				v[j] += tol  
				
				#evaluate function with (xi+dx,...)
				f_dxi = func(v.tolist()) 
				
				#restore the old value, vector again contains (xi,...)
				v[j] = oldval
				
				#evaluate function with (xi,...)
				f_xi = func(v.tolist())  
				
				if(abs(maxfuncval) < abs(f_xi)): 
					maxfuncval = abs(f_xi) 
				
				#register the derivative with respect to xi to Jacobian matrix
				Jacobi[i, j] = (f_dxi - f_xi) / tol


		#return solution vector and number of iterations
		if(abs(maxfuncval) < tol): 
			return v.tolist(),  iter

		DetJacobi = abs(_np.linalg.det(Jacobi))

		if(DetJacobi <= tol):
			raise RuntimeError("At iter="+ str(iter) + " Jacobian Det=" + str(DetJacobi) + ", try different initial values") 
			
		v = v - _np.linalg.solve(Jacobi, Fvals)


