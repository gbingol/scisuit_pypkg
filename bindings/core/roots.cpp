#include "roots.h"

#include <algorithm>
#include <cmath>

#include <core/core_funcs.h>
#include <core/math/roots.h>

#include "../wrapperfuncs.h"

using namespace core::math;


namespace
{
	//Extracts real/complex value from Obj and assign the value to CompNum
	bool AssignComplexValue(
		PyObject* Obj, 
		std::complex<double>* CompNum, 
		std::string& ErrMsg)
	{
		if (IsRealNum(Obj))
		{
			if (auto Elem = GetAsRealNumber(Obj))
				*CompNum = *Elem;
		}
		else if (PyComplex_CheckExact(Obj))
		{
			auto Comp = PyComplex_AsCComplex(Obj);
			*CompNum = std::complex<double>(Comp.real, Comp.imag);
		}
		else
		{
			ErrMsg = "Complex/real number expected";
			return false;
		}

		return true;
	}
}






/******************************   ROOTS    **************************************/

PyObject* c_root_bisect(
	PyObject* FuncObj, 
	double a, 
	double b, 
	double tol, 
	int maxiter, 
	const char* method, 
	bool modified)
{
	auto func = Make1DFunction(FuncObj);

	std::string METHOD(method);
	std::transform(METHOD.begin(), METHOD.end(), METHOD.begin(), ::tolower);

	TRYBLOCK();
	
	roots::bisect_res res;

	if (METHOD == "bf") //brute force
		res = roots::bisection_bf(func, a, b, tol, maxiter);

	else if (METHOD == "rf") //regula falsi (false position)
		res = roots::bisection_rf(func, a, b, tol, maxiter, modified);

	else 
	{
		PyErr_SetString(PyExc_ValueError, "method must be \"bf\" or \"rf\""); 
		return nullptr;
	}


	PyObject* Dict = PyDict_New();
	PyDict_SetItemString(Dict, "root", Py_BuildValue("d", res.Root));
	PyDict_SetItemString(Dict, "error", Py_BuildValue("d", res.Error));
	PyDict_SetItemString(Dict, "iter", Py_BuildValue("i", res.NIter));
	PyDict_SetItemString(Dict, "conv", Py_BuildValue("O", res.Converged ? Py_True : Py_False));
	PyDict_SetItemString(Dict, "msg", Py_BuildValue("s", res.Msg.c_str()));

	return Dict;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_root_itp(
	PyObject * FuncObj,
	double a,
	double b,
	double k1,
	double k2,
	double TOLERANCE,
	size_t MAXITERATIONS)
{
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	auto res = roots::itp(func, a, b, k1, k2, TOLERANCE, MAXITERATIONS);

	PyObject* List = PyList_New(4);
	PyList_SetItem(List, 0, Py_BuildValue("d", res.Error));
	PyList_SetItem(List, 1, Py_BuildValue("i", res.NIter));
	PyList_SetItem(List, 2, Py_BuildValue("O", res.Converged ? Py_True : Py_False));
	PyList_SetItem(List, 3, Py_BuildValue("s", res.Msg.c_str()));

	PyObject* TupleObj = PyTuple_New(2);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", res.Root));
	PyTuple_SetItem(TupleObj, 1, List);

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




PyObject* c_root_brentq(
	PyObject* FuncObj, 
	double a, 
	double b, 
	double tol, 
	int maxiter)
{
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	auto res = roots::brentq(func, a, b, tol, maxiter);

	PyObject* List = PyList_New(3);
	PyList_SetItem(List, 0, Py_BuildValue("i", res.NIter));
	PyList_SetItem(List, 1, Py_BuildValue("O", res.Converged ? Py_True : Py_False));
	PyList_SetItem(List, 2, Py_BuildValue("s", res.Msg.c_str()));

	PyObject* TupleObj = PyTuple_New(2);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", res.Root));
	PyTuple_SetItem(TupleObj, 1, List);

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_root_muller(
	PyObject* FuncObj, 
	PyObject* X0Obj, 
	PyObject* hObj, 
	PyObject* X1Obj, 
	PyObject* X2Obj, 
	double tol, 
	int maxiter)
{
	std::complex<double> h, X1, X2; //optional
	std::complex<double> X0; //must be provided

	std::string ErrMsg;

	auto func = MakeComplexFunction(FuncObj);

	IF_PYERR(X0Obj == nullptr, PyExc_ValueError, "A value must be assigned to x0");

	bool res = AssignComplexValue(X0Obj, &X0, ErrMsg);
	IF_PYERR(res == false, PyExc_RuntimeError, ErrMsg.c_str());


	if (hObj != Py_None)
	{
		IF_PYERR(X1Obj != Py_None, PyExc_ValueError, "if h defined, x1 cannot be defined");
		IF_PYERR(X2Obj != Py_None, PyExc_ValueError, "if h defined, x2 cannot be defined");

		bool res = AssignComplexValue(hObj, &h, ErrMsg);
		IF_PYERR(res == false, PyExc_RuntimeError, ErrMsg.c_str());
	}
	else
		h = 0.5;

	if (X1Obj != Py_None)
	{
		IF_PYERR(X2Obj == Py_None, PyExc_ValueError, "if x1 defined, x2 must also be defined");

		bool res = AssignComplexValue(X1Obj, &X1, ErrMsg);
		IF_PYERR(res == false, PyExc_RuntimeError, ErrMsg.c_str());
	}

	if (X2Obj != Py_None)
	{
		IF_PYERR(X1Obj == Py_None, PyExc_ValueError, "if x2 defined, x1 must also be defined");

		bool res = AssignComplexValue(X2Obj, &X2, ErrMsg);
		IF_PYERR(res == false, PyExc_RuntimeError, ErrMsg.c_str());
	}

	TRYBLOCK();

	roots::muller_res res;

	if (X1Obj == Py_None && X2Obj == Py_None)
		res = roots::muller_x0(func, X0, h, tol, maxiter);
	else
		res = roots::muller_x012(func, X0, X1, X2, tol, maxiter);

	Py_complex RetComp{};
	RetComp.real = res.Root.real();
	RetComp.imag = res.Root.imag();
	PyObject* CompObj = PyComplex_FromCComplex(RetComp);

	PyObject* List = PyList_New(3);
	PyList_SetItem(List, 0, Py_BuildValue("i", res.NIter));
	PyList_SetItem(List, 1, Py_BuildValue("O", res.Converged ? Py_True : Py_False));
	PyList_SetItem(List, 2, Py_BuildValue("s", res.Msg.c_str()));

	PyObject* TupleObj = PyTuple_New(2);
	PyTuple_SetItem(TupleObj, 0, CompObj);
	PyTuple_SetItem(TupleObj, 1, List);

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_root_newton(
	PyObject* FuncObj, 
	double X0, 
	PyObject* X1, 
	PyObject* FPrimeObj, 
	PyObject *FPrime2Obj,
	double tol, 
	int maxiter)
{
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	roots::newton_res res;

	if (FPrimeObj != Py_None)
	{
		auto func_prime = Make1DFunction(FPrimeObj);

		if (FPrime2Obj != Py_None)
		{
			auto func_prime2 = Make1DFunction(FPrime2Obj);
			res = roots::halley(func, X0, func_prime, func_prime2, tol, maxiter);
		}
		else
			res = roots::newtonraphson(func, X0, func_prime, tol, maxiter);
	}
	else
	{
		IF_PYERR(X1 == Py_None, PyExc_ValueError, "if fprime is not provided, x1 must be defined");
		res = roots::secant(func, X0, PyFloat_AsDouble(X1), tol, maxiter);
	}

	PyObject* List = PyList_New(4);
	PyList_SetItem(List, 0, Py_BuildValue("d", res.Error));
	PyList_SetItem(List, 1, Py_BuildValue("i", res.NIter));
	PyList_SetItem(List, 2, Py_BuildValue("O", res.Converged ? Py_True : Py_False));
	PyList_SetItem(List, 3, Py_BuildValue("s", res.Msg.c_str()));

	PyObject* TupleObj = PyTuple_New(2);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", res.Root));
	PyTuple_SetItem(TupleObj, 1, List);

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_root_ridder(
	PyObject* FuncObj, 
	double a, 
	double b, 
	double tol, 
	int maxiter)
{
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	auto res = roots::ridder(func, a, b, tol, maxiter);

	PyObject *List = PyList_New(3);
	PyList_SetItem(List, 0, Py_BuildValue("i", res.NIter));
	PyList_SetItem(List, 1, Py_BuildValue("O", res.Converged ? Py_True : Py_False));
	PyList_SetItem(List, 2, Py_BuildValue("s", res.Msg.c_str()));

	PyObject *TupleObj = PyTuple_New(2);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", res.Root));
	PyTuple_SetItem(TupleObj, 1, List);

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_root_toms748(
	PyObject* FuncObj, 
	double a, 
	double b, 
	double tol, 
	int maxiter)
{
	auto func = Make1DFunction(FuncObj);

	try
	{
		auto bitTol = 1.0 - std::log10(tol) / std::log10(2);
		auto tolboost = boost::math::tools::eps_tolerance<double>(bitTol);
		
		auto res = roots::toms748(func, a, b, tolboost, maxiter);

		PyObject *TupleObj = PyTuple_New(2);
		PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", res.first));
		PyTuple_SetItem(TupleObj, 1, Py_BuildValue("d", res.second));

		return TupleObj;
	}
	catch(const std::exception& e)
	{
		return Py_BuildValue("O", Py_False);
	}
	
	Py_RETURN_NONE;
}