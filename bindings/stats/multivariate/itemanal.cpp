#include "itemanal.h"

#include <core/stats/multivariate/cronbach.h>

#include "../../wrapperfuncs.hpp"


using namespace core::stats;




PyObject* c_stat_test_multivariate_cronbach(PyObject* Obj, bool standardize)
{
	auto N = PyList_Size(Obj);
	IF_PYERR(N<3, PyExc_ValueError, "At least 3 levels expected.");

	std::vector<std::vector<double>> Items;
	for(size_t i=0; i<N; i++)
	{
		auto Item = PyList_GET_ITEM(Obj, i);
		auto v = Iterable_As1DVector(Item);
		Items.push_back(v);
	}

	auto R = tests::multivariate::itemanalysis::cronbach(Items, standardize);
	
	auto Dict = PyDict_New();
	PyDict_SetItemString(Dict, "alpha", Py_BuildValue("d", R.alpha));
	PyDict_SetItemString(Dict, "omitted", List_FromVector(R.omitted));

	return Dict;
}



PyObject* c_stat_test_multivariate_itemanal_squaredmultcorrel(PyObject* Obj)
{
	auto N = PyList_Size(Obj);
	IF_PYERR(N<3, PyExc_ValueError, "At least 3 levels expected.");

	std::vector<std::vector<double>> Items;
	for(size_t i=0; i<N; i++)
	{
		auto Item = PyList_GET_ITEM(Obj, i);
		auto v = Iterable_As1DVector(Item);
		Items.push_back(v);
	}
	
	return List_FromVector(tests::multivariate::itemanalysis::SquaredMultCorrels(Items));
}



PyObject* c_stat_test_multivariate_itemanal_adjtotalcorrel(PyObject* Obj)
{
	auto N = PyList_Size(Obj);
	IF_PYERR(N<3, PyExc_ValueError, "At least 3 levels expected.");

	std::vector<std::vector<double>> Items;
	for(size_t i=0; i<N; i++)
	{
		auto Item = PyList_GET_ITEM(Obj, i);
		auto v = Iterable_As1DVector(Item);
		Items.push_back(v);
	}

	return List_FromVector(tests::multivariate::itemanalysis::AdjTotalCorrels(Items));
}