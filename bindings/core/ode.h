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
	PyObject* t_eval);


EXTERN PyObject * c_core_ode_heun(
	PyObject * FuncObj,
	PyObject* t_span,
	double y0,
	PyObject* t_eval,
	size_t	Repeat = 1);




#undef EXTERN