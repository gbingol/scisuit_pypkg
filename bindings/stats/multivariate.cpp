#include "multivariate.h"

#include <core/stats/multivariate/pca.h>
#include <core/stats/multivariate/cronbach.h>

#include "../wrapperfuncs.hpp"


using namespace core::stats;



PyObject* c_stat_test_multivariate_pca(PyObject* Obj, bool outliers, bool scores)
{
	auto N = PyList_Size(Obj);
	IF_PYERR(N<3, PyExc_ValueError, "At least 3 levels expected.");

	std::vector<std::vector<double>> variables;
	for(size_t i=0; i<N; i++)
	{
		auto Item = PyList_GET_ITEM(Obj, i);
		auto v = Iterable_As1DVector(Item);
		variables.push_back(v);
	}

	auto R = tests::multivariate::pca::pca_cor(variables, outliers, scores);

	
	auto eigs = R.Eigs;
	auto EigList = PyList_New(eigs.size());
	for(std::size_t i=0; const auto elem: eigs)
	{
		auto Tuple = PyTuple_New(2);
		PyTuple_SetItem(Tuple, 0, Py_BuildValue("d", elem.value));
		PyTuple_SetItem(Tuple, 1, List_FromVector(elem.vector));

		PyList_SET_ITEM(EigList, i++, Tuple);
	}

	auto Dict = PyDict_New();

	PyDict_SetItemString(Dict, "eigs", EigList);

	if(outliers)
	{
		IF_PYERR(R.ErrMsg != "", PyExc_RuntimeError, R.ErrMsg.c_str());

		auto Outlier = R.outliers;
		PyDict_SetItemString(Dict, "mahalanobis", List_FromVector(Outlier.mahalanobis));
		PyDict_SetItemString(Dict, "reference", Py_BuildValue("d", Outlier.reference));
	}

	if(scores)
	{
		auto Score = R.scores;

		auto ScoreList = PyList_New(Score.size());

		for(std::size_t i=0; const auto elem: Score)
		{
			auto Tuple = PyTuple_New(2);
			PyTuple_SetItem(Tuple, 0, Py_BuildValue("d", elem.firstComp));
			PyTuple_SetItem(Tuple, 1, Py_BuildValue("d", elem.secondComp));

			PyList_SET_ITEM(ScoreList, i++, Tuple);
		}

		PyDict_SetItemString(Dict, "scores", ScoreList);
	}

	
	return Dict;
}


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