#include "core.h"

#include <algorithm>
#include <unordered_map>

#include <core/core_funcs.h>
#include <core/math/fitting.h>
#include <core/math/integrate.h>
#include <core/math/optimize.h>
#include <core/eng/psychrometry.h>

#include <boost/math/tools/minima.hpp>

#include "../wrapperfuncs.h"

using namespace core::math;


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
		Intercept = GetAsRealNumber(InterceptObj);

	auto Coeffs = fitting::expfit(core::CVector(x), core::CVector(y), Intercept);

	return List_FromVector(Coeffs.data());
	
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

	auto Coeffs = fitting::logfit(core::CVector(x), core::CVector(y));
	return List_FromVector(Coeffs.data());
	
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
		Limit = GetAsRealNumber(LimitObj);

	auto Coeffs = fitting::logistfit(core::CVector(x), core::CVector(y), Limit);

	return List_FromVector(Coeffs.data());
	
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
	return List_FromVector(Coeffs.data());
	
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

	IF_PYERR(x.size() != y.size(), PyExc_RuntimeError, "x and y must have same lengths");

	auto Polynomials = fitting::spline_polynomials(x, y);

	PyObject *MainList = PyList_New(Polynomials.size());
	for (size_t i = 0; const auto &poly : Polynomials)
	{
		auto Coeffs = poly.data();
		std::reverse(Coeffs.begin(), Coeffs.end());

		PyObject *SubList = PyList_New(3);
		PyList_SetItem(SubList, 0, List_FromVector(Coeffs));
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



/************************   OPTIMIZE ****************************/



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






/******************************   ENGINEERING    **************************************/

PyObject* c_eng_psychrometry(PyObject* kwargs)
{
	size_t argc = PyDict_GET_SIZE(kwargs);

	IF_PYERR(argc != 3, PyExc_TypeError, "3 out of (Tdb=, Twb=, Tdp=, RH=, H=, V=, W=, P=) expected");

	PyObject* ObjKey, * ObjValue;
	Py_ssize_t pos = 0;

	TRYBLOCK();

	std::unordered_map<std::string, double> Values;

	while (PyDict_Next(kwargs, &pos, &ObjKey, &ObjValue))
	{
		std::string key = _PyUnicode_AsString(ObjKey);
		std::transform(key.begin(), key.end(), key.begin(), ::tolower);

		double val = PyFloat_AsDouble(ObjValue);
		Values[key] = key == "p" ? val * 1000 : val;
	}

	::core::eng::Psychrometry psy;
	psy.Compute(Values);

	CHECKRANGE_RET(psy.getRH(), 0.0, 100.0, "RH is out of range");
	IF_PYERR(psy.getP()<=0, PyExc_ValueError, "P <= 0.0");
	IF_PYERR(psy.getW() < 0.0, PyExc_ValueError, "W < 0.0")

	PyObject* Dict = PyDict_New();
	auto SetItem = [Dict](const char* Prop, double Val) {
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