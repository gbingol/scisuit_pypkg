#include "integration.h"


#include <core/math/integrate.hpp>

#include "../wrapperfuncs.h"

using namespace core::math;



/*******************************   INTEGRATION   ****************************************/

PyObject* c_integ_simpson(PyObject* X, PyObject* Y)
{
	TRYBLOCK();

	auto x = Iterable_As1DVector(X);
	auto y = Iterable_As1DVector(Y);

	IF_PYERR(x.size() != y.size(), PyExc_RuntimeError, "x and y must have same lengths");

	return Py_BuildValue("d", integrate::simpson(x, y));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_integ_romberg(
	PyObject* FuncObj, 
	double a, 
	double b, 
	double tol,
	int maxiter)
{
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	return Py_BuildValue("d", integrate::romberg(func, a, b, maxiter, tol));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_integ_fixed_quad(
	PyObject* FuncObj, 
	double a, 
	double b, 
	int n)
{
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	return Py_BuildValue("d", integrate::fixed_quad(func, a, b, n));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



