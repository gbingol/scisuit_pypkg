import dataclasses as _dc
import numbers as _numbers
import sys as _sys
import types as _types

import numpy as _np

from ctypes import py_object, c_double, c_int, c_char_p, c_bool

from ._ctypeslib import pydll as _pydll



__all__ = ['bisect','itp', 'brentq', 'muller', 'newton', 'ridder', 'fsolve', "Info", "toms748"]



_pydll.c_root_bisect.argtypes = [py_object, c_double, c_double, c_double, c_int, c_char_p, c_bool]
_pydll.c_root_bisect.restype = py_object


_pydll.c_root_itp.argtypes = [
					py_object, #f
					c_double, #a
					c_double, #b
					c_double, #k1
					c_double, #k2
					c_double, #TOL
					c_int] #maxiter
_pydll.c_root_itp.restype = py_object


_pydll.c_root_brentq.argtypes = [
					py_object, 
					c_double, 
					c_double, 
					c_double, 
					c_int]
_pydll.c_root_brentq.restype = py_object


_pydll.c_root_muller.argtypes = [
					py_object, 
					py_object, 
					py_object, 
					py_object, 
					py_object, 
					c_double, 
					c_int]
_pydll.c_root_muller.restype = py_object


_pydll.c_root_newton.argtypes = [
					py_object, #f
					c_double, #X0
					py_object, #X1
					py_object, #fprime
					py_object, #fprime2
					c_double, #tol
					c_int #maxiter
				]
_pydll.c_root_newton.restype = py_object


_pydll.c_root_ridder.argtypes = [
					py_object, 
					c_double, 
					c_double, 
					c_double, 
					c_int]
_pydll.c_root_ridder.restype = py_object


_pydll.c_root_toms748.argtypes = [
					py_object, 
					c_double, 
					c_double, 
					c_double, 
					c_int]
_pydll.c_root_toms748.restype = py_object





#--------------------------------------------------------------------


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

	root, lst =_pydll.c_root_bisect(f, c_double(a), c_double(b), 
			c_double(tol), 
			c_int(maxiter), 
			c_char_p(method.encode('utf-8')),
			c_bool(modified))
	
	return root, Info(lst[0], lst[1], lst[2], lst[3])


#-----------------------------------------

def itp(
	f:_types.FunctionType, 
	a:_numbers.Real, 
	b:_numbers.Real, 
	k1:_numbers.Real = 0.1,
	k2:_numbers.Real = 2.5656733089749,
	tol:_numbers.Real=1E-5, 
	maxiter:int=100)->tuple[float, Info]:
	"""
	Finds the root using itp (interpolation, truncation, projection) method

	## Inputs:
	f: A unary function
	a, b: The interval where the root lies in
	k1, k2: parameters to control interpolation phase
	tol: tolerance for error
	maxiter: Maximum number of iterations

	## Reference:
	- Oliveira IFD & Takahashi RHC (2020). An Enhancement of the Bisection Method Average 
	  Performance Preserving Minmax Optimality, ACM Transactions on Mathematical Software, 47:1
	"""
	assert isinstance(f, _types.FunctionType), "f must be function."
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"

	assert isinstance(k1, _numbers.Real), "k1 must be real number"
	assert isinstance(k2, _numbers.Real), "k2 must be real number"

	assert isinstance(tol, _numbers.Real), "tol must be Real number"
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int"
	assert maxiter>0, "maxiter>0 expected"

	root, lst =_pydll.c_root_itp(
			py_object(f), 
			c_double(a), 
			c_double(b),
			c_double(k1),
			c_double(k2), 
			c_double(tol), 
			c_int(maxiter))
	
	return root, Info(lst[0], lst[1], lst[2], lst[3])



#-----------------------------------------

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

	assert isinstance(tol, _numbers.Real), "tol must be Real number"
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int"
	assert maxiter>0, "maxiter>0 expected"

	root, lst = _pydll.c_root_brentq(f, c_double(a), c_double(b), c_double(tol), c_int(maxiter))

	return root, Info(None, lst[0], lst[1], lst[2])




#-----------------------------------------

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

	assert isinstance(tol, _numbers.Real), "tol must be Real number"
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int"
	assert maxiter>0, "maxiter>0 expected"
	
	root, lst = _pydll.c_root_muller(f, x0, h, x1, x2, c_double(tol), c_int(maxiter))

	return root, Info(None, lst[0], lst[1], lst[2])



#-----------------------------------------

def newton(
	f:_types.FunctionType, 
	x0:float, 
	x1=None, 
	fprime=None, 
	fprime2=None,
	tol=1E-5, 
	maxiter=100)->tuple[float, Info]:
	"""
	- fprime != None, Newton-Raphson is used,
	- fprime2 != None, Halley's method is used,
	- fprime == None, x1 must be provided and Secant method is used.

	## Inputs:
	f: A unary function 
	fprime: derivative of f 
	fprime2: second derivative of f 
	x0, x1: Initial guesses 
	tol: tolerance for error 
	maxiter: Max number of iterations
	"""
	assert isinstance(f, _types.FunctionType), "f must be function."
	assert isinstance(x0, _numbers.Real), "x0 must be Real number"

	assert isinstance(tol, _numbers.Real), "tol must be Real number"
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int"
	assert maxiter>0, "maxiter>0 expected"

	if(fprime == None):
		assert isinstance(x1, _numbers.Real), "If fprime not provided, x1 must be a real number"
	else:
		assert isinstance(fprime, _types.FunctionType), "If not None, fprime must be function."

	if fprime2 != None:
		assert isinstance(fprime2, _types.FunctionType), "If not None, fprime2 must be function."

	root, lst = _pydll.c_root_newton(
								py_object(f), 
								c_double(x0), 
								py_object(x1), 
								py_object(fprime), 
								py_object(fprime2),
								c_double(tol), 
								c_int(maxiter))

	return root, Info(lst[0], lst[1], lst[2], lst[3])



#-----------------------------------------

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
	assert isinstance(f, _types.FunctionType), "f must be function."
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"

	assert isinstance(tol, _numbers.Real), "tol must be Real number"
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int"
	assert maxiter>0, "maxiter>0 expected"
	
	root, lst = _pydll.c_root_ridder(f, c_double(a), c_double(b), c_double(tol), c_int(maxiter))

	return root, Info(None, lst[0], lst[1], lst[2])



#-----------------------------------------

def toms748(
	f:_types.FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100)->tuple[float, Info]:
	"""
	Algorithm TOMS 748: Alefeld, Potra and Shi: Enclosing zeros of continuous functions

	f: A unary function whose root is sought after
	a, b: The interval where root lies in,
	tol: tolerance for error
	maxiter: Maximum number of iterations during the search for the root

	## Reference:
	https://beta.boost.org/doc/libs/1_82_0/libs/math/doc/html/math_toolkit/roots_noderiv/TOMS748.html
	"""
	assert isinstance(f, _types.FunctionType), "f must be function."
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"
	assert a<b, "a<b expected"

	assert isinstance(tol, _numbers.Real), "tol must be Real number"
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int"
	assert maxiter>0, "maxiter>0 expected"
	

	result = _pydll.c_root_toms748(f, c_double(a), c_double(b), c_double(tol), c_int(maxiter))
	r1, r2 = result[0], result[1]

	if isinstance(result, tuple):
		return float(r1 + r2)/2.0, Info(err=abs(r1-r2), iter=-1, conv=True, msg="")
	
	# did not converge
	return 0.0, Info(err=_sys.float_info.max, iter=-1, conv=False, msg="")



#-----------------------------------------

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
	v = _np.asarray(x0, dtype=_np.float64)
      
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


