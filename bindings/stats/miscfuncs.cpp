#include "miscfuncs.h"


#include <core/math/fitting.h>


#include "../wrapperfuncs.hpp"




PyObject* c_stat_rolling(PyObject* X, PyObject* Y, int Period) 
{
	using namespace core::math::fitting;

	IF_PYERR(Period <= 0, PyExc_ValueError, "period must be >0");
	IF_PYERR(Period < 2, PyExc_ValueError, "period must be >=2");

	auto xvec = Iterable_As1DVector(X);
	auto yvec = Iterable_As1DVector(Y);

	TRYBLOCK();
	
	auto Rolling = rolling(xvec, yvec, Period);

	auto DataList = PyList_New(Rolling.m_Data.size());
	for (size_t i = 0; const auto & V : Rolling.m_Data)
	{
		auto Item = List_FromVector(V.data());
		PyList_SetItem(DataList, i++, Item);
	}

	PyObject* Tuple = PyTuple_New(2);
	PyTuple_SetItem(Tuple, 0, List_FromVector(Rolling.m_X));
	PyTuple_SetItem(Tuple, 1, DataList);

	return Tuple;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}
