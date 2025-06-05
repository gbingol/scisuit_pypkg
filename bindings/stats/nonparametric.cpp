#include "nonparametric.h"

#include <core/stats/nonparam/nonparametric.h>

#include "../wrapperfuncs.hpp"


using namespace core::stats;




PyObject* c_stat_nonparam_signtest(
	PyObject* Obj, 
	double md, 
	bool confint,
	double conflevel, 
	const char* alternative)
{
	using namespace core::stats::tests::nonparametric;
	using core::stats::ALTERNATIVE;

	auto Data = Iterable_As1DVector(Obj);	

	ALTERNATIVE alter = ALTERNATIVE::TWOSIDED;

	if(strcmp(alternative, "less") == 0)
		alter = ALTERNATIVE::LESS;
	else if(strcmp(alternative, "greater") == 0)
		alter = ALTERNATIVE::GREATER;
	
	TRYBLOCK();

	auto result = test_sign(Data, md, confint, conflevel, alter);

	auto Dict = PyDict_New();
	PyDict_SetItemString(Dict, "pvalue", Py_BuildValue("d", result.pval));

	if(confint)
	{
		PyDict_SetItemString(Dict, "acl1", Py_BuildValue("d", result.acl1));
		PyDict_SetItemString(Dict, "acl2", Py_BuildValue("d", result.acl2));

		PyDict_SetItemString(Dict, "ci1_first", Py_BuildValue("d", result.ci1.first));
		PyDict_SetItemString(Dict, "ci1_second", Py_BuildValue("d", result.ci1.second));

		PyDict_SetItemString(Dict, "ci2_first", Py_BuildValue("d", result.ci2.first));
		PyDict_SetItemString(Dict, "ci2_second", Py_BuildValue("d", result.ci2.second));

		PyDict_SetItemString(Dict, "ici_first", Py_BuildValue("d", result.interpci.first));
		PyDict_SetItemString(Dict, "ici_second", Py_BuildValue("d", result.interpci.second));
	}

	return Dict;

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_stat_nonparam_wilcox_signedrank(
	PyObject* Obj, 
	double md, 
	bool confint,
	double conflevel, 
	const char* alternative)
{
	using namespace core::stats::tests::nonparametric;
	using core::stats::ALTERNATIVE;

	auto Data = Iterable_As1DVector(Obj);	

	ALTERNATIVE alter = ALTERNATIVE::TWOSIDED;

	if(strcmp(alternative, "less") == 0)
		alter = ALTERNATIVE::LESS;
	else if(strcmp(alternative, "greater") == 0)
		alter = ALTERNATIVE::GREATER;
	
	
	TRYBLOCK();

	auto result = wilcox_signedrank(Data, md, confint, conflevel, alter);

	auto Dict = PyDict_New();
	PyDict_SetItemString(Dict, "pvalue", Py_BuildValue("d", result.pval));

	if(confint)
	{
		PyDict_SetItemString(Dict, "acl", Py_BuildValue("d", result.acl));

		PyDict_SetItemString(Dict, "ci_first", Py_BuildValue("d", result.ci.first));
		PyDict_SetItemString(Dict, "ci_second", Py_BuildValue("d", result.ci.second));
	}

	return Dict;

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}





PyObject* c_stat_nonparam_mannwhitney(
	PyObject* X, 
	PyObject* Y,
	double md, 
	bool confint,
	double conflevel, 
	const char* alternative)
{
	using namespace core::stats::tests::nonparametric;
	using core::stats::ALTERNATIVE;

	auto DataX = Iterable_As1DVector(X);
	auto DataY = Iterable_As1DVector(Y);	

	ALTERNATIVE alter = ALTERNATIVE::TWOSIDED;

	if(strcmp(alternative, "less") == 0)
		alter = ALTERNATIVE::LESS;
	else if(strcmp(alternative, "greater") == 0)
		alter = ALTERNATIVE::GREATER;
	
	
	TRYBLOCK();

	auto result = mannwhitney(DataX, DataY, md, confint, conflevel, alter);

	auto Dict = PyDict_New();
	PyDict_SetItemString(Dict, "pvalue", Py_BuildValue("d", result.pval));
	PyDict_SetItemString(Dict, "statistics_u", Py_BuildValue("d", result.statistics_U));
	PyDict_SetItemString(Dict, "statistics_w", Py_BuildValue("d", result.statistic_W));

	PyDict_SetItemString(Dict, "median_x", Py_BuildValue("d", result.median_x));
	PyDict_SetItemString(Dict, "median_y", Py_BuildValue("d", result.median_y));

	if(confint)
	{
		PyDict_SetItemString(Dict, "acl", Py_BuildValue("d", result.acl));

		PyDict_SetItemString(Dict, "ci_first", Py_BuildValue("d", result.ci.first));
		PyDict_SetItemString(Dict, "ci_second", Py_BuildValue("d", result.ci.second));
	}

	return Dict;

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



 PyObject* c_stat_nonparam_kruskalwallis(PyObject* responses, PyObject* factors)
{	
	using namespace core::stats::tests::nonparametric;

	auto Resp = Iterable_As1DVector(responses);
	auto Fact = Iterable_As1DVector<std::string>(factors);	

	
	TRYBLOCK();
	
	auto result = kruskalwallis(Resp, Fact);

	auto Dict = PyDict_New();
	PyDict_SetItemString(Dict, "pvalue", Py_BuildValue("d", result.pvalue));
	PyDict_SetItemString(Dict, "statistic", Py_BuildValue("d", result.statistic));
	
	PyDict_SetItemString(Dict, "zvalues", List_FromVector(result.zvalues));
	PyDict_SetItemString(Dict, "counts", List_FromVector(result.counts));

	PyDict_SetItemString(Dict, "ranks", List_FromVector(result.ranks));
	PyDict_SetItemString(Dict, "uniqueFactors", List_FromVector(result.uniqueFactors));

	return Dict;

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_stat_nonparam_friedman(
	PyObject* responses, 
	PyObject* factors,
	PyObject* groups)
{
	using namespace core::stats::tests::nonparametric;

	auto Resp = Iterable_As1DVector(responses);
	auto Fact = Iterable_As1DVector<std::string>(factors);	
	auto Group = Iterable_As1DVector<std::string>(groups);
	
	TRYBLOCK();
	
	auto result = friedman(Resp, Fact, Group);

	auto Dict = PyDict_New();
	PyDict_SetItemString(Dict, "pvalue", Py_BuildValue("d", result.pvalue));
	PyDict_SetItemString(Dict, "statistic", Py_BuildValue("d", result.statistic));

	PyDict_SetItemString(Dict, "quantile_25", List_FromVector(result.quantile_25));
	PyDict_SetItemString(Dict, "quantile_75", List_FromVector(result.quantile_75));

	PyDict_SetItemString(Dict, "counts", List_FromVector(result.counts));
	PyDict_SetItemString(Dict, "medians", List_FromVector(result.medians));
	
	PyDict_SetItemString(Dict, "ranksums", List_FromVector(result.ranksums));
	PyDict_SetItemString(Dict, "uniqueFactors", List_FromVector(result.uniqueFactors));

	return Dict;

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}