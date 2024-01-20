import types as _types
import math


class FiniteDiff:
	"""
	Computes the nth derivative of a function using forward, backward or central
	finite difference methods 
	"""
	def __init__(self, f:_types.FunctionType, x:float, dx=1E-4, n=1) -> None:
		assert dx>0, "dx>0 expected"
		self._func = f
		self._x = x
		self._dx = dx
		self._n = n


	def forward(self)->float:
		f = self._func
		x = self._x
		dx = self._dx
		n = self._n

		numerator = 0
		for i in range(n+1):
			numerator += (-1)**(n-i)*math.comb(n, i)*f(x+i*dx)
		
		return numerator/dx**n

		
	def backward(self)->float:
		f = self._func
		x = self._x
		dx = self._dx
		n = self._n

		numerator = 0
		for i in range(n+1):
			numerator += (-1)**(i)*math.comb(n, i)*f(x-i*dx)
		
		return numerator/dx**n


	def central(self)->float:
		f = self._func
		x = self._x
		dx = self._dx
		n = self._n

		numerator = 0
		for i in range(n+1):
			numerator += (-1)**(i)*math.comb(n, i)*f(x + (n/2-i)*dx)
		
		return numerator/dx**n



def richardson(f:_types.FunctionType, x:float, dx=1E-1, n=1)->float:
	"""
	Richardson Extrapolation for 1st order derivative
	Uses central differences
	"""
	h = dx
	d1 = FiniteDiff(f, x, n=n, dx=h)
	d2 = FiniteDiff(f, x, n=n, dx=h/2)

	return 4/3*d2.central() - 1/3*d1.central()




if __name__ == "__main__":
	f = lambda x: -0.1*x**4 - 0.15*x**3 - 0.5*x**2 - 0.25*x + 1.2
	f2 = lambda x: x**5
	d = FiniteDiff(f, x=0.5, n=1, dx=0.25)
	print(d.forward())
	print(d.backward())
	print(d.central())

	print(richardson(f2, x=2, n=4, dx=0.25))