#include "core.h"

#include <algorithm>
#include <cmath>

#include <core/core_funcs.h>
#include <core/math/fitting.h>
#include <core/math/integrate.h>
#include <core/math/roots.h>
#include <core/eng/psychrometry.h>

#include "wrapperfuncs.h"

using namespace core::math;


namespace
{
	//Extracts real/complex value from Obj and assign the value to CompNum
	bool AssignComplexValue(
		PyObject* Obj, 
		std::complex<double>* CompNum, 
		std::string& ErrMsg)
	{
		if (IsSubTypeRealNumber(Obj))
		{
			if (auto Elem = ExtractRealNumber(Obj))
				*CompNum = Elem.value();
			else
			{
				ErrMsg = "Invalid real number.";
				return false;
			}
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
	ASSERT_CALLABLE_RET(FuncObj, "First parameter must be callable.");
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
	ASSERT_CALLABLE_RET(FuncObj, "First parameter must be callable.");
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

	ASSERT_CALLABLE_RET(FuncObj, "First parameter must be callable.");
	auto func = MakeComplexFunction(FuncObj);

	IF_PYERRVALUE_RET(X0Obj == nullptr, "A value must be assigned to x0");

	bool res = AssignComplexValue(X0Obj, &X0, ErrMsg);
	IF_PYERRRUNTIME_RET(res == false, ErrMsg.c_str());


	if (hObj != Py_None)
	{
		IF_PYERRVALUE_RET(X1Obj != Py_None, "if h defined, x1 cannot be defined");
		IF_PYERRVALUE_RET(X2Obj != Py_None, "if h defined, x2 cannot be defined");

		bool res = AssignComplexValue(hObj, &h, ErrMsg);
		IF_PYERRRUNTIME_RET(res == false, ErrMsg.c_str());
	}
	else
		h = 0.5;

	if (X1Obj != Py_None)
	{
		IF_PYERRVALUE_RET(X2Obj == Py_None, "if x1 defined, x2 must also be defined");

		bool res = AssignComplexValue(X1Obj, &X1, ErrMsg);
		IF_PYERRRUNTIME_RET(res == false, ErrMsg.c_str());
	}

	if (X2Obj != Py_None)
	{
		IF_PYERRVALUE_RET(X1Obj == Py_None, "if x2 defined, x1 must also be defined");

		bool res = AssignComplexValue(X2Obj, &X2, ErrMsg);
		IF_PYERRRUNTIME_RET(res == false, ErrMsg.c_str());
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
	double tol, 
	int maxiter)
{
	ASSERT_CALLABLE_RET(FuncObj, "f must be callable.");
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	roots::newton_res res;

	if (FPrimeObj != Py_None)
	{
		ASSERT_CALLABLE_RET(FPrimeObj, "fprime must be callable.");
		auto func_prime = Make1DFunction(FPrimeObj);
		res = roots::newtonraphson(func, X0, func_prime, tol, maxiter);
	}
	else
	{
		IF_PYERRVALUE_RET(X1 == Py_None, "if fprime is not provided, x1 must be defined");
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
	ASSERT_CALLABLE_RET(FuncObj, "f must be a function.");
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





/**********************************    FITTING    *********************************/

PyObject* c_fit_expfit(
	PyObject* X, 
	PyObject* Y, 
	PyObject* InterceptObj)
{
	TRYBLOCK();

	auto x = Iterable_As1DVector(X);
	auto y = Iterable_As1DVector(Y);

	std::optional<double> Intercept;

	if (InterceptObj != Py_None)
		Intercept = ExtractRealNumber(InterceptObj);

	auto Coefficients = fitting::expfit(core::CVector(x), core::CVector(y), Intercept);

	return List_FromCVector(Coefficients);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_fit_lagrange(
	PyObject* X, 
	PyObject* Y, 
	double Value)
{
	TRYBLOCK();

	auto x = Iterable_As1DVector(X);
	auto y = Iterable_As1DVector(Y);

	return Py_BuildValue("d", fitting::lagrange(x, y, Value));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_fit_logfit(
	PyObject* X, 
	PyObject* Y)
{
	TRYBLOCK();

	auto x = Iterable_As1DVector(X);
	auto y = Iterable_As1DVector(Y);

	auto Coefficients = fitting::logfit(core::CVector(x), core::CVector(y));
	return List_FromCVector(Coefficients);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_fit_logistfit(
	PyObject* X, 
	PyObject* Y, 
	PyObject* LimitObj)
{
	TRYBLOCK();

	auto x = Iterable_As1DVector(X);
	auto y = Iterable_As1DVector(Y);

	std::optional<double> Limit;

	if (LimitObj != Py_None)
		Limit = ExtractRealNumber(LimitObj);

	auto Coefficients = fitting::logistfit(core::CVector(x), core::CVector(y), Limit);

	return List_FromCVector(Coefficients);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}





PyObject* c_fit_powfit(
	PyObject* X, 
	PyObject* Y)
{
	TRYBLOCK();

	auto x = Iterable_As1DVector(X);
	auto y = Iterable_As1DVector(Y);

	auto Coeffs = fitting::powfit(core::CVector(x), core::CVector(y));
	return List_FromCVector(Coeffs);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_fit_spline(
	PyObject* X, 
	PyObject* Y)
{
	TRYBLOCK();

	auto x = Iterable_As1DVector(X);
	auto y = Iterable_As1DVector(Y);

	IF_PYERR_RET(x.size() != y.size(), PyExc_RuntimeError, "x and y must have same lengths");

	auto Polynomials = fitting::spline_polynomials(x, y);

	PyObject *MainList = PyList_New(Polynomials.size());
	for (size_t i = 0; const auto &poly : Polynomials)
	{
		auto Coeffs = poly.data();
		std::reverse(Coeffs.begin(), Coeffs.end());

		PyObject *SubList = PyList_New(3);
		PyList_SetItem(SubList, 0, List_FromCVector(Coeffs));
		PyList_SetItem(SubList, 1, PyFloat_FromDouble(x[i]));
		PyList_SetItem(SubList, 2, PyFloat_FromDouble(x[i + 1]));

		PyList_SetItem(MainList, i++, SubList);
	}

		return MainList;

	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*******************************   INTEGRATION   ****************************************/

PyObject* c_integ_simpson(PyObject* X, PyObject* Y)
{
	TRYBLOCK();

	auto x = Iterable_As1DVector(X);
	auto y = Iterable_As1DVector(Y);

	IF_PYERR_RET(x.size() != y.size(), PyExc_RuntimeError, "x and y must have same lengths");

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
	ASSERT_CALLABLE_RET(FuncObj, "f must be callable.");
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
	ASSERT_CALLABLE_RET(FuncObj, "f must be callable.");
	auto func = Make1DFunction(FuncObj);

	TRYBLOCK();

	return Py_BuildValue("d", integrate::fixed_quad(func, a, b, n));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}





/******************************   ENGINEERING    **************************************/


PyObject* c_eng_psychrometry(PyObject* kwargs)
{
	std::vector<std::string> Keys;
	std::vector<double> Vals;

	size_t argc = PyDict_GET_SIZE(kwargs);

	IF_PYERR_RET(argc != 3, PyExc_TypeError, "3 out of (Tdb=, Twb=, Tdp=, RH=, H=, V=, W=, P=) expected");

	PyObject* ObjKey, * ObjValue;
	Py_ssize_t pos = 0;

	TRYBLOCK();

	while (PyDict_Next(kwargs, &pos, &ObjKey, &ObjValue))
	{
		std::string key = _PyUnicode_AsString(ObjKey);
		std::transform(key.begin(), key.end(), key.begin(), ::tolower);
		double val = PyFloat_AsDouble(ObjValue);

		if (key == "tdb" || key == "twb" || key == "tdp" || key == "rh" || key == "h" || key == "v" || key == "w")
		{
		}

		else if (key == "p")
			val = val * 1000; // Take parameter as kPa and convert to Pa

		else
		{
			PyErr_SetString(PyExc_TypeError, "Keys: P, Tdb, Twb, Tdp, W, H, RH");
			return nullptr;
		}

		Keys.push_back(key);
		Vals.push_back(val);
	}

	::core::eng::Psychrometry psy;
	psy.Compute(Keys, Vals);

	CHECKRANGE_RET(psy.getRH(), 0.0, 100.0, "RH is out of range");
	CHECKPOSITIVE_RET(psy.getP(), "P <= 0.0");
	CHECKNONNEGATIVE_RET(psy.getP(), "W < 0.0");

	PyObject* Dict = PyDict_New();
	auto SetItem = [Dict](const char* Prop, double Val) 
	{
		PyDict_SetItemString(Dict, Prop, PyFloat_FromDouble(Val));
	};

	SetItem("Tdb", psy.getTdb());
	SetItem("Twb", psy.getTwb());
	SetItem("Tdp", psy.getTdp());
	SetItem("P", psy.getP() / 1000);
	SetItem("Pw", psy.getPw() / 1000);
	SetItem("Pws", psy.getPws() / 1000);
	SetItem("W", psy.getW());

	if (psy.getWs() >= 0)
		SetItem("Ws", psy.getWs());

	SetItem("RH", psy.getRH());
	SetItem("H", psy.getH());
	SetItem("V", psy.getV());

	return Dict;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}