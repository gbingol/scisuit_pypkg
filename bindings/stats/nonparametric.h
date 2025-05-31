#pragma once
#include <Python.h>

#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_stat_test_nonparam_signtest(PyObject* Obj, double md, double conflevel, const char* alternative);

#undef EXTERN