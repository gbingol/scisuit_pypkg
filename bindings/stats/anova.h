#pragma once
#include <Python.h>

#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_stat_test_anova_aov(PyObject* Obj);
EXTERN PyObject* c_stat_test_anova_posthoc(double alpha, PyObject* Obj, const char* method);
EXTERN PyObject* c_stat_test_anova_aov2(PyObject* YObsObj, PyObject* X1Obj, PyObject* X2Obj);


#undef EXTERN