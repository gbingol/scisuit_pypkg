#pragma once
#include <Python.h>

#include "../../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_stat_essential_correlation(
	PyObject* X, 
	PyObject* Y, 
	double conflevel = 0.95,
	const char* method = "pearson");



#undef EXTERN