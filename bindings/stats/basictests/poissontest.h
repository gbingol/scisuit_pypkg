#pragma once

#include <Python.h>

#include "../../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_stat_essential_poisson1samplen(
		PyObject* sample, PyObject* frequency,
		PyObject* samplesize, PyObject* totaloccur,
		double length = 1,
		bool hypotest = false,
		double hyporate = 0.0,
		double conflevel = 0.95,
		const char* method = "normal",
		const char* alternative = "two.sided");



#undef EXTERN