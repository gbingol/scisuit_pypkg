#include "normality.h"

#include <core/stats/basictests/normality.h>

#include "../../wrapperfuncs.hpp"


using namespace core::stats;




PyObject* c_stat_normality_ad(PyObject* Obj)
{
	auto Data = Iterable_As1DVector(Obj);
	TRYBLOCK();
	
	auto Result = tests::normality::AndersonDarling(Data);

	auto TupleObj = PyTuple_New(2);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", Result.pvalue));
	PyTuple_SetItem(TupleObj, 1, Py_BuildValue("d", Result.AD));

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	return nullptr;
}


PyObject* c_stat_normality_shapirowilk(PyObject* Obj)
{
	auto Data = Iterable_As1DVector(Obj);
	TRYBLOCK();
	
	auto Result = tests::normality::ShapiroWilkinson(Data);

	auto TupleObj = PyTuple_New(3);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", Result.w));
	PyTuple_SetItem(TupleObj, 1, Py_BuildValue("d", Result.pw));
	PyTuple_SetItem(TupleObj, 2, Py_BuildValue("s", Result.msg.c_str()));

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	return nullptr;
}
