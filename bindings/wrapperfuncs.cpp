#include "wrapperfuncs.h"

#include <core/core_funcs.h>
#include <core/dtypes.h>




std::function<double(double)> Make1DFunction(PyObject* funcObj)
{
    auto func = [=](double x)
    {
        PyObject* ObjX = PyFloat_FromDouble(x);

        PyObject* pArgs = PyTuple_Pack(1, ObjX);
        Py_DECREF(ObjX);

        PyObject* ResultObj = PyObject_CallObject(funcObj, pArgs);
        Py_DECREF(pArgs);

		//If the function can not be evaluated (for example a function not returning a real number)
        if (!ResultObj)
			throw std::exception(("f(" + std::to_string(x) + ") is invalid.").c_str());

        double retVal = PyFloat_AsDouble(ResultObj);
        Py_DECREF(ResultObj);

        return retVal;
    };

    return func;
}




std::function<std::complex<double>(std::complex<double>)> MakeComplexFunction(PyObject* callableObj)
{
    auto func = [=](std::complex<double> x)
    {
        PyObject* ObjX = PyComplex_FromDoubles(x.real(), x.imag());

        if (!ObjX)
            throw std::exception("Can not make complex number");

        PyObject* ResultObj = PyObject_CallFunction(callableObj, "O", ObjX);
        Py_DECREF(ObjX);

        if (!ResultObj)
            throw std::exception("Malformed function: cannot handle complex numbers");

        auto ComplexReturn = PyComplex_AsCComplex(ResultObj);
        Py_DECREF(ResultObj);

        std::complex<double> retVal(ComplexReturn.real, ComplexReturn.imag);
        return retVal;
    };

    return func;
}

