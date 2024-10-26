#pragma once


#include <Python.h>
#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



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






#undef EXTERN