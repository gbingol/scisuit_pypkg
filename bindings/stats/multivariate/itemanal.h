#pragma once
#include <Python.h>

#include "../../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND





EXTERN PyObject* c_stat_test_multivariate_cronbach(PyObject* Obj, bool standardize);



/**
 * @brief Computes Squared Multiple Correlations for all omitted items
 * 
 * @param Obj Whose sub-lists are columns of a table
 */
EXTERN PyObject* c_stat_test_multivariate_itemanal_squaredmultcorrel(PyObject* Obj);




/**
 * @brief Computes Squared Multiple Correlations for all omitted items
 * 
 * @param Obj Whose sub-lists are columns of a table
 */
EXTERN PyObject* c_stat_test_multivariate_itemanal_adjtotalcorrel(PyObject* Obj);


#undef EXTERN