#pragma once

#include <cstdint>
#include <Python.h>

#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND




/************************   OPTIMIZE ****************************/

EXTERN PyObject* c_optimize_bracket(
	PyObject* FuncObj,
	double a,
	double b,
	double growlimit = 100,
	std::uint32_t maxiter = 1000);


EXTERN PyObject* c_optimize_golden(
	PyObject* FuncObj,
	double xlow,
	double xhigh,
	double tol = 1E-6,
	std::uint32_t maxiter = 1000);


EXTERN PyObject* c_optimize_parabolic(
	PyObject* FuncObj,
	double xa,
	double xb,
	PyObject* xc,
	double tol = 1E-6,
	std::uint32_t maxiter = 1000);


EXTERN PyObject* c_optimize_brent(
	PyObject* FuncObj,
	double xlow,
	double xhigh,
	std::uintmax_t maxiter = 1000);





#undef EXTERN