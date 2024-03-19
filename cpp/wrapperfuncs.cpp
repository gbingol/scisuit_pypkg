#include "wrapperfuncs.h"

#include <core/core_funcs.h>
#include <core/dtypes.h>


bool IsNumpyInt(PyObject* obj)
{
	auto TpNm = obj->ob_type->tp_name;
	bool Int32 = std::strcmp(TpNm, "numpy.int32") == 0 ? true : false;
	bool Int64 = std::strcmp(TpNm, "numpy.int64") == 0 ? true : false;

	return Int32 || Int64;
}


bool IsNumpyFloat(PyObject* obj)
{
	auto TpNm = obj->ob_type->tp_name;
	bool Float32 = std::strcmp(TpNm, "numpy.float32") == 0 ? true : false;
	bool Float64 = std::strcmp(TpNm, "numpy.float64") == 0 ? true : false;

	return Float32 || Float64;
}


std::optional<double> ExtractRealNumber(PyObject* obj)
{
    if (!obj)
        return std::nullopt;

    if (IsSubTypeFloat(obj) || IsNumpyFloat(obj))
        return PyFloat_AsDouble(obj);

    else if (IsSubTypeLong(obj) || IsNumpyInt(obj))
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
    std::function<double(double)> func = [=](double x)
    {
        PyObject* ObjX = PyFloat_FromDouble(x);

        if (!ObjX)
            throw std::exception("Can not make real number");

        PyObject* pArgs = PyTuple_Pack(1, ObjX);
        PyObject* pValue = PyObject_CallObject(funcObj, pArgs);

        if (!pValue)
            throw std::exception("Malformed function: cannot handle real numbers");

        double retVal = PyFloat_AsDouble(pValue);

        Py_DECREF(ObjX);
        Py_DECREF(pArgs);
        Py_DECREF(pValue);

        return retVal;
    };

    return func;
}




std::function<std::complex<double>(std::complex<double>)> MakeComplexFunction(PyObject* callableObj)
{
    std::function<std::complex<double>(std::complex<double>)> func = [=](std::complex<double> x)
    {
        PyObject* ObjX = PyComplex_FromDoubles(x.real(), x.imag());

        if (!ObjX)
            throw std::exception("Can not make complex number");

        PyObject* pValue = PyObject_CallFunction(callableObj, "O", ObjX);

        if (!pValue)
            throw std::exception("Malformed function: cannot handle complex numbers");

        auto ComplexReturn = PyComplex_AsCComplex(pValue);
        std::complex<double> retVal(ComplexReturn.real, ComplexReturn.imag);


        Py_DECREF(ObjX);
        Py_DECREF(pValue);

        return retVal;
    };

    return func;
}

