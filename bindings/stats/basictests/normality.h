#pragma once
#include <Python.h>

#include "../../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_stat_normality_ad(PyObject* Obj);

EXTERN PyObject* c_stat_normality_shapirowilk(PyObject* Obj);

//Kolmogorov-Smirnov 1-sample test is already implemented in Python


#undef EXTERN