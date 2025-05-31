#pragma once
#include <Python.h>

#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND


EXTERN PyObject* c_stat_rolling(PyObject* X, PyObject* Y, int Period = 2);


#undef EXTERN