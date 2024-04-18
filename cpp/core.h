#pragma once

#include <cstdint>
#include <Python.h>

#include "dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND




/******************************   ROOTS    **************************************/


EXTERN PyObject * c_root_bisect(
	PyObject * FuncObj,
	double a,
	double b,
	double tol = 1e-5,
	int maxiter = 100,
	const char* method = "bf",
	bool modified = false);


EXTERN PyObject * c_root_brentq(
	PyObject * FuncObj,
	double a,
	double b,
	double tol = 1e-5,
	int maxiter = 100);


EXTERN PyObject * c_root_muller(
	PyObject * FuncObj,
	PyObject * x0,
	PyObject * h = nullptr,
	PyObject * x1 = nullptr,
	PyObject * x2 = nullptr,
	double tol = 1e-5,
	int maxiter = 100);


EXTERN PyObject * c_root_newton(PyObject * FuncObj,
	double X0,
	PyObject * X1,
	PyObject * FPrimeObj,
	PyObject *FPrime2Obj,
	double tol = 1e-5,
	int maxiter = 100);


EXTERN PyObject * c_root_ridder(PyObject * FuncObj,
	double a,
	double b,
	double tol = 1e-5,
	int maxiter = 100);


EXTERN PyObject * c_root_toms748(
	PyObject * FuncObj,
	double a,
	double b,
	double tol = 1e-5,
	int maxiter = 100);



/*******************************   FITTING   ****************************************/
EXTERN PyObject* c_fit_expfit(
	PyObject* X, 
	PyObject* Y, 
	PyObject* InterceptObj);


EXTERN PyObject* c_fit_lagrange(
	PyObject* X, 
	PyObject* Y, 
	double Value);

EXTERN PyObject* c_fit_logfit(
	PyObject* X, 
	PyObject* Y);


EXTERN PyObject* c_fit_logistfit(
	PyObject* X, 
	PyObject* Y, 
	PyObject* LimitObj);


EXTERN PyObject* c_fit_powfit(
	PyObject* X, 
	PyObject* Y);


EXTERN PyObject* c_fit_spline(
	PyObject* X, 
	PyObject* Y);



/*******************************   INTEGRATION   ****************************************/
EXTERN PyObject* c_integ_simpson(
	PyObject* X, 
	PyObject* Y);


EXTERN PyObject* c_integ_romberg(
	PyObject* FuncObj,
	double a,
	double b,
	double tol = 1e-5,
	int maxiter = 100);


EXTERN PyObject* c_integ_fixed_quad(
	PyObject* FuncObj,
	double a,
	double b,
	int n = 5);






/************************   OPTIMIZE ****************************/

EXTERN PyObject* c_optimize_bracket(
	PyObject* FuncObj,
	double a,
	double b,
	double growlimit = 100,
	std::uint32_t maxiter = 1000);


EXTERN PyObject* c_optimize_golden(
	PyObject* FuncObj,
	double xlow,
	double xhigh,
	double tol = 1E-6,
	std::uint32_t maxiter = 1000);


EXTERN PyObject* c_optimize_brent(
	PyObject* FuncObj,
	double xlow,
	double xhigh,
	std::uintmax_t maxiter = 1000);


/******************************   ENGINEERING    **************************************/

EXTERN PyObject * c_eng_psychrometry(PyObject * kwargs);




#undef EXTERN