#include "stat_tests.h"

#include <core/stats/basictests/normality.h>
#include <core/stats/nonparam/nonparametric.h>
#include <core/stats/anova/aov.h>
#include <core/stats/anova/aov2.h>

#include <core/math/fitting.h>


#include "../wrapperfuncs.hpp"


using namespace core::stats;



PyObject* c_stat_rolling(PyObject* X, PyObject* Y, int Period) 
{
	IF_PYERR(Period <= 0, PyExc_ValueError, "period must be >0");
	IF_PYERR(Period < 2, PyExc_ValueError, "period must be >=2");

	auto xvec = Iterable_As1DVector(X);
	auto yvec = Iterable_As1DVector(Y);

	TRYBLOCK();
	
	auto Rolling = core::math::fitting::rolling(xvec, yvec, Period);

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



PyObject* c_stat_test_norm_ad(PyObject* Obj)
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


PyObject* c_stat_test_shapirowilkinson(PyObject* Obj)
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



PyObject* c_stat_test_nonparam_signtest(PyObject* Obj, double md, double conflevel, const char* alternative)
{
	using core::stats::ALTERNATIVE;
	auto Data = Iterable_As1DVector(Obj);	

	ALTERNATIVE alter = ALTERNATIVE::TWOSIDED;

	if(strcmp(alternative, "less") == 0)
		alter = ALTERNATIVE::LESS;
	else if(strcmp(alternative, "greater") == 0)
		alter = ALTERNATIVE::GREATER;
	

	auto result = core::stats::tests::nonparametric::test_sign(Data, md, true, conflevel, alter);

	auto Dict = PyDict_New();
	PyDict_SetItemString(Dict, "pvalue", Py_BuildValue("d", result.pval));

	PyDict_SetItemString(Dict, "acl1", Py_BuildValue("d", result.acl1));
	PyDict_SetItemString(Dict, "acl2", Py_BuildValue("d", result.acl2));

	PyDict_SetItemString(Dict, "ci1_first", Py_BuildValue("d", result.ci1.first));
	PyDict_SetItemString(Dict, "ci1_second", Py_BuildValue("d", result.ci1.second));

	PyDict_SetItemString(Dict, "ci2_first", Py_BuildValue("d", result.ci2.first));
	PyDict_SetItemString(Dict, "ci2_second", Py_BuildValue("d", result.ci2.second));

	PyDict_SetItemString(Dict, "ici_first", Py_BuildValue("d", result.interpci.first));
	PyDict_SetItemString(Dict, "ici_second", Py_BuildValue("d", result.interpci.second));

	return Dict;
}