#include "wrapperfuncs.h"

#include <core/core_funcs.h>
#include <core/dtypes.h>


std::optional<double> GetAsRealNumber(PyObject* obj)
{
    if (!obj)
        return std::nullopt;

    if (PyFloat_Check(obj))
        return PyFloat_AsDouble(obj);

    else if (PyLong_Check(obj))
        return (double)PyLong_AsLong(obj);

    return std::nullopt;
}



PyObject* List_FromCVector(const core::CVector& Vec)
{
    if (Vec.size() == 0)
        return nullptr;

    auto RetList = PyList_New(Vec.size());

    for (size_t i = 0; i < Vec.size(); ++i)
        PyList_SetItem(RetList, i, Py_BuildValue("d", Vec[i]));

    return RetList;
}



std::function<double(double)> Make1DFunction(PyObject* funcObj)
{
    auto func = [=](double x)
    {
        PyObject* ObjX = PyFloat_FromDouble(x);

        if (!ObjX)
		{
            auto StrObj = PyObject_Str(ObjX);
			auto err = std::string("Attempted to convert to real number: ") + PyUnicode_AsUTF8(StrObj);
            Py_DECREF(StrObj);

			throw std::exception(err.c_str());
		}

        PyObject* pArgs = PyTuple_Pack(1, ObjX);
        Py_DECREF(ObjX);

        PyObject* ResultObj = PyObject_CallObject(funcObj, pArgs);
        Py_DECREF(pArgs);

        if (!ResultObj)
		{
            auto StrObj = PyObject_Str(funcObj);
			auto err = std::string("Could not evaluate ") + PyUnicode_AsUTF8(StrObj);
			err += " at : " + std::to_string(x);

             Py_DECREF(StrObj);
						
			throw std::exception(err.c_str());
		}

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

