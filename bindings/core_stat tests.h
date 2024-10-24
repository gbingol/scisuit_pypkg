#pragma once
#include <Python.h>

#include "dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND


EXTERN PyObject* c_stat_rolling(
	PyObject* X, 
	PyObject* Y, 
	int Period = 2);

EXTERN PyObject* c_stat_test_norm_ad(PyObject* Obj);

EXTERN PyObject* c_stat_test_shapirowilkinson(PyObject* Obj);

EXTERN PyObject* c_stat_test_aov(PyObject* Obj);

#undef EXTERN