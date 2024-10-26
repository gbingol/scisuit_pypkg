#include "optimization.h"

#include <core/math/optimize.h>
#include <boost/math/tools/minima.hpp>

#include "../wrapperfuncs.h"




PyObject* c_optimize_bracket(
	PyObject* FuncObj,
	double a,
	double b,
	double growlimit,
	std::uint32_t maxiter)
{
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	auto R = core::math::optimize::bracket(func, a, b, growlimit, maxiter);
	auto dict = PyDict_New();
	PyDict_SetItemString(dict, "a", Py_BuildValue("d", R.a));
	PyDict_SetItemString(dict, "b", Py_BuildValue("d", R.b));
	PyDict_SetItemString(dict, "c", Py_BuildValue("d", R.c));

	PyDict_SetItemString(dict, "fa", Py_BuildValue("d", R.fa));
	PyDict_SetItemString(dict, "fb", Py_BuildValue("d", R.fb));
	PyDict_SetItemString(dict, "fc", Py_BuildValue("d", R.fc));

	return dict;

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_optimize_golden(
	PyObject* FuncObj,
	double xlow,
	double xhigh,
	double tol,
	std::uint32_t maxiter)
{
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	auto R = core::math::optimize::golden(func, xlow, xhigh, maxiter, tol);
	auto tuple = PyTuple_New(3);
	PyTuple_SetItem(tuple, 0,  Py_BuildValue("d", R.xopt));
	PyTuple_SetItem(tuple, 1, Py_BuildValue("d", R.error));
	PyTuple_SetItem(tuple, 2, Py_BuildValue("i", R.iter));

	return tuple;

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_optimize_parabolic(
	PyObject* FuncObj,
	double xa,
	double xb,
	PyObject* xc,
	double tol,
	std::uint32_t maxiter)
{
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	std::optional<double> c = std::nullopt;
	if(!Py_IsNone(xc))
		c = PyFloat_AsDouble(xc);

	auto R = core::math::optimize::parabolic(func, xa, xb,c, maxiter, tol);
	auto tuple = PyTuple_New(3);
	PyTuple_SetItem(tuple, 0,  Py_BuildValue("d", R.xopt));
	PyTuple_SetItem(tuple, 1, Py_BuildValue("d", R.error));
	PyTuple_SetItem(tuple, 2, Py_BuildValue("i", R.iter));

	return tuple;

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_optimize_brent(
	PyObject* FuncObj,
	double xlow,
	double xhigh,
	std::uintmax_t maxiter)
{
	auto func = Make1DFunction(FuncObj);
	const int double_bits = std::numeric_limits<double>::digits;
    auto maxit = maxiter;

	TRYBLOCK();

	auto R = boost::math::tools::brent_find_minima(func, xlow, xhigh, double_bits, maxit);
	if(maxit == maxiter)
		throw std::runtime_error("maxiter exceeded");

	auto tuple = PyTuple_New(3);
	PyTuple_SetItem(tuple, 0,  Py_BuildValue("d", R.first)); //xopt 
	PyTuple_SetItem(tuple, 1, Py_BuildValue("d", R.second)); // f(xopt)
	PyTuple_SetItem(tuple, 2, Py_BuildValue("i", maxit)); //number of iterations

	return tuple;

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}

