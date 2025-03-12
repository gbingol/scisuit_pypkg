#pragma once

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


EXTERN PyObject *c_root_itp(
	PyObject * FuncObj,
	double a,
	double b,
	double k1=0.1,
	double k2=2.5656733089749,
	size_t n0=1,
	double TOLERANCE = 1E-5,
	size_t MAXITERATIONS = 100);


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


#undef EXTERN