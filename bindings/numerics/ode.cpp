#include "ode.h"

#include <core/math/ode.h>
#include "../wrapperfuncs.hpp"


using namespace core::math;

PyObject * c_core_ode_euler(
	PyObject * FuncObj,
	PyObject* t_span,
	double y0,
	PyObject* t_eval)
{
	auto func = Make2DFunction(FuncObj);
	auto tspan_vec = Iterable_As1DVector(t_span);
	IF_PYERR(tspan_vec.size()!=2, PyExc_ValueError, "t_span must have exactly two values.");

	TRYBLOCK();

	ode::ode_res result;

	std::pair<double, double> tspan ={tspan_vec[0], tspan_vec[1]};
	
	//Either a step size or t_eval must be provided (checked from Python side)
	if(PyFloat_Check(t_eval))
		result = ode::euler(func, tspan , y0, PyFloat_AS_DOUBLE(t_eval));
	else
	{
		auto teval = Iterable_As1DVector(t_eval);
		result = ode::euler(func, tspan, y0, std::nullopt, teval);
	}


	PyObject* Dict = PyDict_New();
	PyDict_SetItemString(Dict, "t", List_FromVector(result.t));
	PyDict_SetItemString(Dict, "y", List_FromVector(result.y));

	return Dict;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject * c_core_ode_heun(
	PyObject * FuncObj,
	PyObject* t_span,
	double y0,
	PyObject* t_eval,
	size_t	Repeat)
{
	auto func = Make2DFunction(FuncObj);
	auto tspan_vec = Iterable_As1DVector(t_span);
	IF_PYERR(tspan_vec.size()!=2, PyExc_ValueError, "t_span must have exactly two values.");

	TRYBLOCK();

	ode::ode_res result;

	std::pair<double, double> tspan ={tspan_vec[0], tspan_vec[1]};
	
	//Either h or t_eval must be provided (checked from Python side)
	if(PyFloat_Check(t_eval))
		result = ode::heun(func, tspan , y0, PyFloat_AS_DOUBLE(t_eval), std::nullopt, Repeat);
	else if(!Py_IsNone(t_eval))
	{
		auto teval = Iterable_As1DVector(t_eval);
		result = ode::heun(func, tspan, y0, std::nullopt, teval, Repeat);
	}


	PyObject* Dict = PyDict_New();
	PyDict_SetItemString(Dict, "t", List_FromVector(result.t));
	PyDict_SetItemString(Dict, "y", List_FromVector(result.y));

	return Dict;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject * c_core_ode_rungekutta(
	PyObject * FuncObj,
	PyObject* t_span,
	double y0,
	PyObject* t_eval,
	uint8_t Order)
{
	auto func = Make2DFunction(FuncObj);
	auto tspan_vec = Iterable_As1DVector(t_span);
	IF_PYERR(tspan_vec.size()!=2, PyExc_ValueError, "t_span must have exactly two values.");

	TRYBLOCK();

	ode::ode_res result;

	std::pair<double, double> tspan ={tspan_vec[0], tspan_vec[1]};
	
	//Either h or t_eval must be provided (checked from Python side)
	if(PyFloat_Check(t_eval))
		result = ode::runge_kutta(func, tspan , y0, PyFloat_AS_DOUBLE(t_eval), std::nullopt, Order);
	else if(!Py_IsNone(t_eval))
	{
		auto teval = Iterable_As1DVector(t_eval);
		result = ode::runge_kutta(func, tspan, y0, std::nullopt, teval, Order);
	}


	PyObject* Dict = PyDict_New();
	PyDict_SetItemString(Dict, "t", List_FromVector(result.t));
	PyDict_SetItemString(Dict, "y", List_FromVector(result.y));

	return Dict;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}