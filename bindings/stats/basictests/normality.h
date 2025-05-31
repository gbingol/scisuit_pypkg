#pragma once
#include <Python.h>

#include "../../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_stat_normality_ad(PyObject* Obj);

EXTERN PyObject* c_stat_normality_shapirowilk(PyObject* Obj);


#undef EXTERN