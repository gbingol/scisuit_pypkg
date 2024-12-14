#pragma once

#include <Python.h>

#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND




/******************************   ODE    **************************************/

EXTERN PyObject * c_core_ode_euler(
	PyObject * FuncObj,
	PyObject* t_span,
	double y0,
	PyObject* h = nullptr,
	PyObject* t_eval=nullptr);


#undef EXTERN