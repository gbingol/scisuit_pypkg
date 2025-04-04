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

EXTERN PyObject* c_stat_test_anova_aov(PyObject* Obj);
EXTERN PyObject* c_stat_test_anova_tukey(double alpha, PyObject* Obj);

EXTERN PyObject* c_stat_test_anova_aov2(PyObject* YObsObj, PyObject* X1Obj, PyObject* X2Obj);

/**************************************** */


EXTERN PyObject* c_stat_test_nonparam_signtest(PyObject* Obj, double md, double conflevel, const char* alternative);

#undef EXTERN