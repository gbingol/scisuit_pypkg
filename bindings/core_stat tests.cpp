#include "core_stat tests.h"


#include <core/core_funcs.h>
#include <core/stats/basictests/normality.h>
#include <core/stats/anova/aov.h>
#include <core/math/fitting.h>

#include "wrapperfuncs.h"


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
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", Result.first));
	PyTuple_SetItem(TupleObj, 1, Py_BuildValue("d", Result.second));

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


PyObject* c_stat_test_aov(PyObject* Obj)
{
	auto N = PyTuple_Size(Obj);
	IF_PYERR(N<3, PyExc_ValueError, "At least 3 levels expected.");

	std::vector<std::vector<double>> args;
	for(size_t i=0; i<N; i++)
	{
		auto Item = PyTuple_GET_ITEM(Obj, i);
		auto v = Iterable_As1DVector(Item);
		args.push_back(v);
	}

	auto R = tests::anova::aov(args);

	auto Dict = PyDict_New();
	PyDict_SetItemString(Dict, "Averages", List_FromVector(R.Averages));
	PyDict_SetItemString(Dict, "SampleSizes", List_FromVector(R.SampleSizes));

	PyDict_SetItemString(Dict, "Error_DF", Py_BuildValue("i", R.Error_DF));
	PyDict_SetItemString(Dict, "Error_MS", Py_BuildValue("d", R.Error_MS));
	PyDict_SetItemString(Dict, "Error_SS", Py_BuildValue("d", R.Error_SS));

	PyDict_SetItemString(Dict, "Total_DF", Py_BuildValue("i", R.Total_DF));
	PyDict_SetItemString(Dict, "Total_MS", Py_BuildValue("d", R.Total_MS));
	PyDict_SetItemString(Dict, "Total_SS", Py_BuildValue("d", R.Total_SS));

	PyDict_SetItemString(Dict, "Treat_DF", Py_BuildValue("i", R.Treat_DF));
	PyDict_SetItemString(Dict, "Treat_MS", Py_BuildValue("d", R.Treat_MS));
	PyDict_SetItemString(Dict, "Treat_SS", Py_BuildValue("d", R.Treat_SS));

	PyDict_SetItemString(Dict, "Fvalue", Py_BuildValue("d", R.Fvalue));
	PyDict_SetItemString(Dict, "pvalue", Py_BuildValue("d", R.pvalue));

	return Dict;
}