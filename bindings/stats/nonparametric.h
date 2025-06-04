#pragma once
#include <Python.h>

#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_stat_nonparam_signtest(
	PyObject* Obj, 
	double md, 
	bool confint,
	double conflevel, 
	const char* alternative);


EXTERN PyObject* c_stat_nonparam_wilcox_signedrank(
	PyObject* Obj, 
	double md, 
	bool confint,
	double conflevel, 
	const char* alternative);



EXTERN PyObject* c_stat_nonparam_mannwhitney(
	PyObject* X, 
	PyObject* Y,
	double md, 
	bool confint,
	double conflevel, 
	const char* alternative);


EXTERN PyObject* c_stat_nonparam_kruskalwallis(
	PyObject* responses, 
	PyObject* factors);

#undef EXTERN