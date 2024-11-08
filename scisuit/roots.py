from dataclasses import dataclass
from numbers import Real, Complex
from types import FunctionType

import numpy as _np

from ctypes import py_object, c_double, c_int, c_char_p, c_bool
from ._ctypeslib import pydll as _pydll



__all__ = ['bisect','itp', 'brentq', 'muller', 'newton', 'ridder', 'fsolve', "Info", "toms748"]



_pydll.c_root_bisect.argtypes = [py_object, c_double, c_double, c_double, c_int, c_char_p, c_bool]
_pydll.c_root_bisect.restype = py_object

_pydll.c_root_itp.argtypes = [py_object, c_double, c_double, c_double, c_double,c_int, c_double, c_int]
_pydll.c_root_itp.restype = py_object

_pydll.c_root_brentq.argtypes = [py_object, c_double, c_double, c_double, c_int]
_pydll.c_root_brentq.restype = py_object

_pydll.c_root_muller.argtypes = [py_object, py_object, py_object, py_object, py_object, c_double, c_int]
_pydll.c_root_muller.restype = py_object

_pydll.c_root_newton.argtypes = [ py_object, c_double, py_object, py_object, py_object, c_double, c_int ]
_pydll.c_root_newton.restype = py_object

_pydll.c_root_ridder.argtypes = [py_object, c_double, c_double, c_double, c_int]
_pydll.c_root_ridder.restype = py_object

_pydll.c_root_toms748.argtypes = [py_object, c_double, c_double, c_double, c_int]
_pydll.c_root_toms748.restype = py_object





#--------------------------------------------------------------------
#--------------------------------------------------------------------

@dataclass
class bisect_result:
	root:float
	iter:int
	conv:bool
	msg:str
	err:float
	method:tuple

	def __str__(self):
		s = "Bisection using " + ("brute-force" if self.method[0]=="bf" else "regula falsi") + " method \n"
		s += "Using Modified regula-falsi \n" if self.method[1] else ""
		if not self.conv:
			s += "Could not converge to a root."
			s += self.msg
			return s
		s += f"Root={self.root:.5f}, Error={self.err:.2e} ({self.iter} iterations)."
		return s


def bisect(
	f:FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100, 
	method:tuple[str, bool]=("bf", False)
	)->bisect_result:
	"""
	Finds the root using bisection method

	f: A unary function  
	a, b: The interval where the root lies in  
	tol: tolerance for error  
	maxiter: Maximum number of iterations  
	method: ("bf" or "rf", for brute-force/regula falsi , True modified rf).
	"""
	assert isinstance(f, FunctionType), "f must be function"
	assert isinstance(a, Real), "a must be real number."
	assert isinstance(b, Real), "b must be real number."
	assert method[0] in ["bf", "rf"], "method must be 'bf' or 'rf' ."

	dct:dict =_pydll.c_root_bisect(f, c_double(a), c_double(b), 
			c_double(tol), 
			c_int(maxiter), 
			c_char_p(method[0].lower().encode('utf-8')),
			c_bool(method[1]))
	
	return bisect_result(root = dct["root"],
						conv=dct["conv"],
						iter=dct["iter"],
						msg=dct["msg"],
						err=dct["err"],
						method=method)




#-----------------------------------------
#--------------------------------------------------------------------


@dataclass
class itp_result:
	root:float
	err:float
	iter:int
	conv:bool
	msg:str

	def __str__(self):
		s = "ITP method \n"
		if not self.conv:
			s += "Could not converge to a root."
			s += self.msg
			return s
		s += f"Root={self.root:.5f}, Error={self.err:.2e} ({self.iter} iterations)."
		return s


def itp(
	f:FunctionType, 
	a:Real, 
	b:Real, 
	k1:Real = -1.0,
	k2:Real = 2.0,
	n0:int=1,
	tol:Real=1E-5, 
	maxiter:int=100)->itp_result:
	"""
	Finds the root using itp (interpolation, truncation, projection) method

	f: A unary function  
	a, b: The interval where the root lies in  
	k1, k2: parameters to control interpolation phase  
	tol: tolerance for error  
	maxiter: Maximum number of iterations  

	## Reference:
	- Oliveira IFD & Takahashi RHC (2020). An Enhancement of the Bisection Method Average 
	  Performance Preserving Minmax Optimality, ACM Transactions on Mathematical Software, 47:1
	"""
	assert isinstance(f, FunctionType), "f must be function."
	assert isinstance(a, Real), "a must be real number."
	assert isinstance(b, Real), "b must be real number"

	assert isinstance(k1, Real), "k1 must be real number."
	assert isinstance(k2, Real), "k2 must be real number."
	SQRT_5 = 2.23606797749979
	assert 1.0< k2 < (1 + (1 + SQRT_5) / 2), f"k2 must be in (1.0, {(1 + (1 + SQRT_5) / 2)})"

	assert isinstance(tol, Real), "tol must be Real number."
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int."
	assert maxiter>0, "maxiter>0 expected"

	dct:dict =_pydll.c_root_itp(py_object(f), 
						c_double(a), 
						c_double(b),
						c_double(k1 if k1>0 else 0.1/(b-a)),
						c_double(k2), 
						c_int(n0),
						c_double(tol), 
						c_int(maxiter))
	
	return itp_result(root = dct["root"],
					conv=dct["conv"],
					iter=dct["iter"],
					msg=dct["msg"],
					err=dct["err"] )




#-----------------------------------------
#--------------------------------------------------------------------


@dataclass
class brentq_result:
	root:float
	iter:int
	conv:bool
	msg:str

	def __str__(self):
		s = "Brent's method (inverse quadratic interpolation) \n"
		if not self.conv:
			s += "Could not converge to a root."
			s += self.msg
			return s
		s += f"Root={self.root:.5f}, ({self.iter} iterations)."
		return s



def brentq(
	f:FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100)->brentq_result:
	"""
	Uses the Brent's method (1973) to find the root of the function 
	using inverse quadratic interpolation

	f: A unary function whose root is sought after  
	a, b: The interval where root lies in  
	tol: tolerance for error  
	maxiter: Maximum number of iterations during the search for the root
	"""
	assert isinstance(f, FunctionType), "f must be function."
	assert isinstance(a, Real), "a must be real number."
	assert isinstance(b, Real), "b must be real number."

	assert isinstance(tol, Real), "tol must be Real number."
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int."
	assert maxiter>0, "maxiter>0 expected"

	dct:dict = _pydll.c_root_brentq(f, c_double(a), c_double(b), c_double(tol), c_int(maxiter))

	return brentq_result(root = dct["root"],
						conv=dct["conv"],
						iter=dct["iter"],
						msg=dct["msg"] )





#-----------------------------------------
#--------------------------------------------------------------------

@dataclass
class muller_result:
	root:float
	iter:int
	conv:bool
	msg:str

	def __str__(self):
		s = "Muller method \n"
		if not self.conv:
			s += "Could not converge to a root."
			s += self.msg
			return s
		s += f"Root={self.root} ({self.iter} iterations)."
		return s


def muller(
	f:FunctionType, 
	x0:Complex, 
	h=None, 
	x1=None, 
	x2=None, 
	tol=1E-5, 
	maxiter=100)->muller_result:
	"""
	Finds root of an equation using Muller method
	
	f: A unary function  
	x0, x1, x2:	Initial guesses  
	h: Step length  
	tol: tolerance for error  
	maxiter: Max number of iterations
	"""
	assert isinstance(f, FunctionType), "f must be function."
	assert isinstance(x0, Complex), "x0 must be a Complex/Real number."

	assert isinstance(tol, Real), "tol must be Real number."
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int."
	assert maxiter>0, "maxiter>0 expected."

	if h != None:
		assert x1 == None, "if h defined, x1 cannot be defined"
		assert x2 == None, "if h defined, x2 cannot be defined"
	
	if x1 != None or x2 != None:
		assert x2 != None, "if x1 defined, x2 must also be defined"
		assert x1 != None, "if x2 defined, x1 must also be defined"
	
	dct:dict = _pydll.c_root_muller(f, x0, h, x1, x2, c_double(tol), c_int(maxiter))

	return muller_result(root = dct["root"],
					conv=dct["conv"],
					iter=dct["iter"],
					msg=dct["msg"] )





#-----------------------------------------
#--------------------------------------------------------------------

@dataclass
class newton_result:
	root:float
	err:float
	iter:int
	conv:bool
	msg:str
	method:str

	def __str__(self):
		s = "Newton method (" + self.method + ") \n"
		if not self.conv:
			s += "Could not converge to a root."
			s += self.msg
			return s
		s += f"Root={self.root:.5f}, Error={self.err:.2e} ({self.iter} iterations)."
		return s


def newton(
	f:FunctionType, 
	x0:float, 
	x1=None, 
	fprime=None, 
	fprime2=None,
	tol=1E-5, 
	maxiter=100)->newton_result:
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
	assert isinstance(f, FunctionType), "f must be function."
	assert isinstance(x0, Real), "x0 must be Real number."

	assert isinstance(tol, Real), "tol must be Real number."
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int."
	assert maxiter>0, "maxiter>0 expected."

	methodName = "Newton-Raphson"

	if(fprime == None):
		assert isinstance(x1, Real), "If fprime not provided, x1 must be a real number."
		methodName="Secant"
	else:
		assert isinstance(fprime, FunctionType), "If not None, fprime must be function."

	if fprime2 != None:
		assert isinstance(fprime2, FunctionType), "If not None, fprime2 must be function."
		methodName="Halley"

	dct:dict = _pydll.c_root_newton(
								py_object(f), 
								c_double(x0), 
								py_object(x1), 
								py_object(fprime), 
								py_object(fprime2),
								c_double(tol), 
								c_int(maxiter))

	return newton_result(root = dct["root"],
						conv=dct["conv"],
						iter=dct["iter"],
						msg=dct["msg"],
						err=dct["err"],
						method=methodName )





#-----------------------------------------
#--------------------------------------------------------------------

@dataclass
class ridder_result:
	root:float
	iter:int = -1
	conv:bool = False
	msg:str =""

	def __str__(self):
		s = "Ridder's method \n"
		if not self.conv:
			s += "Could not converge to a root."
			s += self.msg
			return s
		s += f"Root={self.root:.5f}, ({self.iter} iterations)."
		return s


def ridder(
	f:FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100)->ridder_result:
	"""
	Uses Ridder's method.

	f: A unary function  
	a, b: The interval where the root lies in  
	tol: tolerance for error  
	maxiter: Maximum number of iterations
	"""
	assert isinstance(f, FunctionType), "f must be function."
	assert isinstance(a, Real), "a must be real number."
	assert isinstance(b, Real), "b must be real number."

	assert isinstance(tol, Real), "tol must be Real number."
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int."
	assert maxiter>0, "maxiter>0 expected."
	
	dct:dict = _pydll.c_root_ridder(f, c_double(a), c_double(b), c_double(tol), c_int(maxiter))

	return ridder_result(root = dct["root"],
						conv=dct["conv"],
						iter=dct["iter"],
						msg=dct["msg"] )





#-----------------------------------------
#--------------------------------------------------------------------

@dataclass
class toms748_result:
	root:float
	err:float
	conv:bool
	root:float

	def __str__(self):
		s = "Algorithm TOMS 748 \n"
		if not self.conv:
			s += "Could not converge to a root."
			return s
		s += f"Root={self.root:.5f}, Error={self.err:.2e} ."
		return s


def toms748(
	f:FunctionType, 
	a:float, 
	b:float, 
	tol=1E-5, 
	maxiter=100)->toms748_result:
	"""
	Algorithm TOMS 748: Alefeld, Potra and Shi: Enclosing zeros of continuous functions

	f: A unary function whose root is sought after  
	a, b: The interval where root lies in  
	tol: tolerance for error  
	maxiter: Maximum number of iterations during the search for the root

	## Reference:
	https://beta.boost.org/doc/libs/1_82_0/libs/math/doc/html/math_toolkit/roots_noderiv/TOMS748.html
	"""
	assert isinstance(f, FunctionType), "f must be function."
	assert isinstance(a, Real), "a must be real number."
	assert isinstance(b, Real), "b must be real number."
	assert a<b, "a<b expected"

	assert isinstance(tol, Real), "tol must be Real number."
	assert tol>0, "tol>0 expected"

	assert isinstance(maxiter, int), "maxiter must be int."
	assert maxiter>0, "maxiter>0 expected"
	

	res:dict = _pydll.c_root_toms748(f, c_double(a), c_double(b), c_double(tol), c_int(maxiter))

	return toms748_result(root=res["root"], err=res["err"], conv=res["conv"])
	





#-----------------------------------------
#--------------------------------------------------------------------


@dataclass
class fsolve_result:
	roots:list[float]
	iter:int

	def __str__(self):
		s = "Solving Set of Equations \n"
		if len(self.roots)>1:
			s += f"Converged to roots after {self.iter} iterations. \n"
			for i, root in enumerate(self.roots):
				s += f"Root #{i}={root:.4f} \n"
		else:
			s += f"Could not converge after {self.iter} iterations."
		return s


def fsolve(
		F:list[FunctionType], 
		x0:list[float], 
		tol=1E-5, 
		maxiter=100 )->fsolve_result:
	"""
	Solves a system of non-linear equations using Newton's approach.  
	Functions are in the format of f(x1,x2,...)=0

	## Inputs:
	F: a list of functions  
	x0: a list of initial guesses  

	## EXAMPLE
	x^2 + y^2 = 5  
	x^2 - y^2 = 1  

	First define the functions, F(x, y) = 0:  

	def f1(t):  
		return t[0]**2 + t[1]**2 - 5  

	def f2(t):  
		return t[0]**2 - t[1]**2 - 1  
	
	roots, iter=fsolve( [f1,f2], [1,1] )  
	
	print(roots, "  iter:", iter)  
	1.73205	1.41421	iter:5  

	print(f1(roots), " ", f2(roots))  
	9.428e-09    9.377e-09 
	
	"""
	assert isinstance(F, list), "F must be a list of functions."
	assert isinstance(x0, list), "x0 must be a list of numbers."

	assert isinstance(tol, Real) and tol>0, "tol must be Real and tol>0 expected."
	assert isinstance(maxiter, int) and maxiter>0, "maxiter>0 expected."

	dim = len(F)

	assert dim>=2, "At least 2 functions are required."
	assert dim == len(x0), "F and x0 must have same length."


	#solution vector as floating point
	v = _np.asarray(x0, dtype=_np.float64)
      
	#values of each function	
	Fvals = _np.zeros(dim)
	Jacobi = _np.zeros((dim, dim)) 

	for iter in range(maxiter):
		maxfuncval = 0 #convergence criteria
	
		for i in range(dim):
			func = F[i]     #function
			assert isinstance(func, FunctionType), "F must have functions of form f(t)=0."
			
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
				
				if abs(maxfuncval) < abs(f_xi): 
					maxfuncval = abs(f_xi) 
				
				#register the derivative with respect to xi to Jacobian matrix
				Jacobi[i, j] = (f_dxi - f_xi) / tol


		#return solution vector and number of iterations
		if abs(maxfuncval) < tol: 
			return fsolve_result(roots=v.tolist(),  iter=iter)

		#Jacobi Determinant
		DetJ = abs(_np.linalg.det(Jacobi))
		if DetJ <= tol:
			raise RuntimeError(f"At iter={iter} Jacobi Det={DetJ}.") 
			
		v = v - _np.linalg.solve(Jacobi, Fvals)


