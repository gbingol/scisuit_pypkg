from ._ctypeslib import coreDLL as _core
import ctypes as _ct
import numbers as _numbers
import types as _types
import numpy as _np


__all__ = ['bisect', 'brentq', 'muller', 'newton', 'ridder', 'fsolve']


def bisect(f:_types.FunctionType, a:float, b:float, tol=1E-5, maxiter=100, method="bf", modified=False)->tuple:
	"""
	Finds the root using bisection method.

	## Inputs:
	f: A unary function \n
	a, b:	The interval where the root lies in \n
	tol:	tolerance for error \n
	maxiter: Maximum number of iterations \n
	method: "bf" for brute-force (halving)  \n
	"rf" for regula falsi (false position)  \n
	modified: True for modified regula falsi method.
	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"

	return _core.c_root_bisect(f, _ct.c_double(a), _ct.c_double(b), 
			_ct.c_double(tol), 
			_ct.c_int(maxiter), 
			_ct.c_char_p(method.encode('utf-8')),
			_ct.c_bool(modified))



def brentq(f:_types.FunctionType, a:float, b:float, tol=1E-5, maxiter=100)->tuple:
	"""
	Uses the Brent's method (1973) to find the root of the function 
	using inverse quadratic interpolation.

	## Inputs:
	f: A unary function whose root is sought after \n
	a, b: The interval where root lies in \n
	tol: tolerance for error \n
	maxiter: Maximum number of iterations during the search for the root

	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"

	return _core.c_root_brentq(f, _ct.c_double(a), _ct.c_double(b), _ct.c_double(tol), _ct.c_int(maxiter))




def muller(f:_types.FunctionType, x0:_numbers.Complex, h=None, x1=None, x2=None, tol=1E-5, maxiter=100)->tuple:
	"""
	## Inputs:
	f: A unary function \n
	x0, x1, x2:	Initial guesses \n
	h: Step length \n
	tol: tolerance for error \n
	maxiter: Max number of iterations
	"""
	assert callable(f), "f must be function"
	assert isinstance(x0, _numbers.Complex), "x0 must be a Complex/Real number"
	
	return _core.c_root_muller(f, x0, h, x1, x2, _ct.c_double(tol), _ct.c_int(maxiter))



def newton(f:_types.FunctionType, x0:float, x1=None, fprime=None, tol=1E-5, maxiter=100)->tuple:
	"""
	If fprime is provided then uses Newton-Raphson method  \n
	If fprime is not provided, then x1 must be provided uses Secant method.

	## Inputs:
	f: A unary function \n
	fprime: derivative of f \n
	x0, x1: Initial guesses \n
	tol: tolerance for error \n
	maxiter: Max number of iterations
	"""
	assert callable(f), "f must be function"
	assert isinstance(x0, _numbers.Real)
	if(fprime == None):
		assert isinstance(x1, _numbers.Real), "If fprime not provided, x1 must be a real number"
	else:
		assert callable(fprime), "If fprime is provided, it must be of type function."

	return _core.c_root_newton(f, _ct.c_double(x0), x1, fprime, _ct.c_double(tol), _ct.c_int(maxiter))




def ridder(f:_types.FunctionType, a:float, b:float, tol=1E-5, maxiter=100)->tuple:
	"""
	Uses Ridder's method.

	## Inputs:
	f: A unary function \n
	a, b:	The interval where the root lies in \n
	tol: tolerance for error \n
	maxiter: Maximum number of iterations
	"""
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"
	
	return _core.c_root_ridder(f, _ct.c_double(a), _ct.c_double(b), _ct.c_double(tol), _ct.c_int(maxiter))




def fsolve(F:list, x0:list, tol=1E-5, maxiter=100 )->tuple:
	"""
	Solves a system of non-linear equations using Newton's approach. \n
	Functions are in the format of f(x1,x2,...)=0
	

	## Inputs:
	F: a list of functions \n
	x0: a list of initial guesses \n


	## USAGE EXAMPLE
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
	assert isinstance(x0, list), "a must be a number"

	assert isinstance(tol, _numbers.Number) and tol>0, "tol must be a positive number"
	assert isinstance(maxiter, int) and maxiter>0, "maxiter must be a positive integer"

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


