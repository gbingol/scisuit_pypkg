#include "fitting.h"

#include <algorithm>

#include <core/math/fitting.h>

#include "../wrapperfuncs.h"





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

	auto Coeffs = core::math::fitting::expfit(core::CVector(x), core::CVector(y), Intercept);

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

	return Py_BuildValue("d", core::math::fitting::lagrange(x, y, Value));
	
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

	auto Coeffs = core::math::fitting::logfit(core::CVector(x), core::CVector(y));
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

	auto Coeffs = core::math::fitting::logistfit(core::CVector(x), core::CVector(y), Limit);

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

	auto Coeffs = core::math::fitting::powfit(core::CVector(x), core::CVector(y));
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

	auto Polynomials = core::math::fitting::spline_polynomials(x, y);

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


