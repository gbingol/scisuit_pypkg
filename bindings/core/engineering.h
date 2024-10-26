#pragma once


#include <Python.h>

#include "../dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject * c_eng_psychrometry(PyObject * kwargs);




#undef EXTERN