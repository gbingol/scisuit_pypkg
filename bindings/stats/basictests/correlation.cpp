#include "correlation.h"

#include <core/stats/basictests/correlation.h>

#include "../../wrapperfuncs.hpp"


using namespace core::stats;




PyObject* c_stat_essential_correlation(
	PyObject* X, 
	PyObject* Y, 
	double conflevel,
	const char* method)
{
	auto DataX = Iterable_As1DVector(X);
	auto DataY = Iterable_As1DVector(Y);
	TRYBLOCK();
	
	auto Result = tests::correlation::correlation(DataX, DataY, conflevel, method);

	auto TupleObj = PyTuple_New(3);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", Result.coeff));
	PyTuple_SetItem(TupleObj, 1, Py_BuildValue("d", Result.CI_lower));
	PyTuple_SetItem(TupleObj, 2, Py_BuildValue("d", Result.CI_upper));

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



