#pragma once


#include <Python.h>

#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



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



#undef EXTERN