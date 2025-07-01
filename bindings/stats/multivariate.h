#pragma once
#include <Python.h>

#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_stat_test_multivariate_pca(PyObject* Obj, bool outliers, bool scores);



#undef EXTERN