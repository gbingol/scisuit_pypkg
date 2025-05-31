#include "nonparametric.h"


#include <core/stats/nonparam/nonparametric.h>

#include "../wrapperfuncs.hpp"


using namespace core::stats;




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