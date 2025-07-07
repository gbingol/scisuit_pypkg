#pragma once
#include <Python.h>

#include "../../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND

#define NOTHROW \
	__attribute__((nothrow))



EXTERN PyObject* c_stat_test_multivariate_pca(PyObject* Obj, bool outliers, bool scores);



#undef EXTERN
#undef NOTHROW