import types as _types

def forward(f:_types.FunctionType, x:float, dx=1E-5)->float:
	assert dx>0, "dx>0 expected"

	return (f(x+dx) - f(x))/dx


def backward(f:_types.FunctionType, x:float, dx=1E-5)->float:
	assert dx>0, "dx>0 expected"
	
	return (f(x-dx) - f(x))/dx


def central(f:_types.FunctionType, x:float, dx=1E-5)->float:
	assert dx>0, "dx>0 expected"

	return (f(x+dx) - f(x-dx))/(2*dx)

