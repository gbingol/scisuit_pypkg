import types as _types
import math


class Derivative:
	"""
	Computes the nth derivative of a function using forward, backward or central
	finite difference methods 
	"""
	def __init__(self, f:_types.FunctionType, x:float, dx=1E-4, n=1) -> None:
		assert dx>0, "dx>0 expected"
		self._func = f
		self._x = x
		self._dx = x*dx
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




if __name__ == "__main__":
	f = lambda x: x**5 
	d = Derivative(f, 2, n=1)
	print(d.forward())
	print(d.backward())
	print(d.central())