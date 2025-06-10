#include "poissontest.h"

#include <core/stats/basictests/poisson.h>

#include "../../wrapperfuncs.hpp"


using namespace core::stats;
using namespace core::stats::tests::poisson;



PyObject* c_stat_essential_poisson1samplen(
	PyObject* sample, PyObject* frequency,
	PyObject* samplesize, PyObject* totaloccur,
	double length,
	bool hypotest,
	double hyporate,
	double conflevel,
	const char* method,
	const char* alternative)
{

	ALTERNATIVE alter = ALTERNATIVE::TWOSIDED;

	if(strcmp(alternative, "less") == 0)
		alter = ALTERNATIVE::LESS;
	else if(strcmp(alternative, "greater") == 0)
		alter = ALTERNATIVE::GREATER;
	

	onesample_Result Result;
	TRYBLOCK();

	if(!Py_IsNone(sample))
	{
		auto SampleVec = Iterable_As1DVector<std::size_t>(sample);
		
		std::vector<std::size_t> FreqVec;
		if(!Py_IsNone(frequency))
			auto FreVec = Iterable_As1DVector<std::size_t>(frequency);

		Result = onesample_freq(
					SampleVec, 
					FreqVec, 
					length, 
					hypotest, 
					hyporate, 
					conflevel, 
					method, 
					alter);
	}
	
	else if(!Py_IsNone(samplesize))
		Result = onesample_sizes(
					PyLong_AsLongLong(samplesize), 
					PyLong_AsLongLong(totaloccur), 
					length, 
					hypotest, 
					hyporate, 
					conflevel, 
					method, 
					alter);

	auto Dict = PyDict_New();

	PyDict_SetItemString(Dict, "pvalue", Py_BuildValue("d", Result.pvalue));
	PyDict_SetItemString(Dict, "zvalue", Py_BuildValue("d", Result.zvalue));
	PyDict_SetItemString(Dict, "CI_lower", Py_BuildValue("d", Result.CI_lower));
	PyDict_SetItemString(Dict, "CI_upper", Py_BuildValue("d", Result.CI_upper));
	PyDict_SetItemString(Dict, "mean", Py_BuildValue("d", Result.mean));

	PyDict_SetItemString(Dict, "N", Py_BuildValue("i", Result.N));
	PyDict_SetItemString(Dict, "TotalOccurences", Py_BuildValue("i", Result.TotalOccurences));

	return Dict;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



