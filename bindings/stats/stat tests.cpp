#include "stat tests.h"

#include <core/stats/basictests/normality.h>
#include <core/stats/anova/aov.h>
#include <core/stats/anova/aov2.h>
#include <core/math/fitting.h>


#include "../wrapperfuncs.h"


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


PyObject* c_stat_test_anova_aov(PyObject* Obj)
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


PyObject* c_stat_test_anova_tukey(double alpha, PyObject* Obj)
{
	TRYBLOCK()

	tests::anova::aov_Result aovresult;
	aovresult.Averages = Iterable_As1DVector(PyDict_GetItemString(Obj, "Averages"));
	aovresult.SampleSizes = Iterable_As1DVector(PyDict_GetItemString(Obj, "SampleSizes"));
	aovresult.Treat_DF = PyLong_AsLong(PyDict_GetItemString(Obj, "Treat_DF"));
	aovresult.Error_DF = PyLong_AsLong(PyDict_GetItemString(Obj, "Error_DF"));
	aovresult.Error_MS = PyFloat_AS_DOUBLE(PyDict_GetItemString(Obj, "Error_MS"));

	IF_PYERR(aovresult.Averages.size()==0, PyExc_RuntimeError, "Averages size is 0.")

	auto Comparisons = tests::anova::tukey(alpha, aovresult);

	IF_PYERR(Comparisons.size()==0, PyExc_RuntimeError, "No comparisons obtained.");

	auto lst = PyList_New(Comparisons.size());
	for(size_t i=0; const auto& comp:Comparisons)
	{
		auto dct = PyDict_New();
		PyDict_SetItemString(dct, "a", Py_BuildValue("i", comp.a));
		PyDict_SetItemString(dct, "b", Py_BuildValue("i", comp.b));
		PyDict_SetItemString(dct, "diff", Py_BuildValue("d", comp.Diff));
		PyDict_SetItemString(dct, "CILow", Py_BuildValue("d", comp.CILow));
		PyDict_SetItemString(dct, "CIHigh", Py_BuildValue("d", comp.CIHigh));

		PyList_SetItem(lst, i++, dct);
	}

	return lst;

	CATCHRUNTIMEEXCEPTION(nullptr)

	Py_RETURN_NONE;
}


PyObject* c_stat_test_anova_aov2(PyObject* YObsObj, PyObject* X1Obj, PyObject* X2Obj)
{
	auto YObs = Iterable_As1DVector(YObsObj);
	auto X1 = Iterable_As1DVector<std::string>(X1Obj);
	auto X2 = Iterable_As1DVector<std::string>(X2Obj);
		
	auto R = tests::anova::aov2(YObs, X1, X2);

	auto Dict = PyDict_New();

	PyDict_SetItemString(Dict, "DFError", Py_BuildValue("i", R.DFError));
	PyDict_SetItemString(Dict, "DFFact1", Py_BuildValue("i", R.DFFact1));
	PyDict_SetItemString(Dict, "DFFact2", Py_BuildValue("i", R.DFFact2));

	PyDict_SetItemString(Dict, "FvalFact1", Py_BuildValue("d", R.FvalFact1));
	PyDict_SetItemString(Dict, "FvalFact2", Py_BuildValue("d", R.FvalFact2));

	PyDict_SetItemString(Dict, "MSError", Py_BuildValue("i", R.MSError));
	PyDict_SetItemString(Dict, "MSFact1", Py_BuildValue("d", R.MSFact1));
	PyDict_SetItemString(Dict, "MSFact2", Py_BuildValue("d", R.MSFact2));
	
	PyDict_SetItemString(Dict, "pvalFact1", Py_BuildValue("d", R.pvalFact1));
	PyDict_SetItemString(Dict, "pvalFact2", Py_BuildValue("d", R.pvalFact2));
	
	PyDict_SetItemString(Dict, "SSError", Py_BuildValue("d", R.SSError));
	PyDict_SetItemString(Dict, "SSFact1", Py_BuildValue("d", R.SSFact1));
	PyDict_SetItemString(Dict, "SSFact2", Py_BuildValue("d", R.SSFact2));
	
	//when repetitions involved, there is interaction terms (if one has value the others must have)
	if(R.DFinteract>0)
	{
		PyDict_SetItemString(Dict, "DFinteract", Py_BuildValue("i", R.DFinteract));
		PyDict_SetItemString(Dict, "Fvalinteract", Py_BuildValue("d", *R.Fvalinteract));
		PyDict_SetItemString(Dict, "MSinteract", Py_BuildValue("d", *R.MSinteract));
		PyDict_SetItemString(Dict, "pvalinteract", Py_BuildValue("d", *R.pvalinteract));
		PyDict_SetItemString(Dict, "SSinteract", Py_BuildValue("d", *R.SSinteract));
	}

	if(R.Residuals.size()>0)
	{
		PyDict_SetItemString(Dict, "Residuals", List_FromVector(R.Residuals));
		PyDict_SetItemString(Dict, "Fits", List_FromVector(R.Fits));
	}

	return Dict;
}