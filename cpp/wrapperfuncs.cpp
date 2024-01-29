#include "wrapperfuncs.h"

#include <core/core_funcs.h>
#include <core/dtypes/mathdtypes.h>
#include <core/dtypes/array.h>



std::optional<double> ExtractRealNumber(PyObject* obj)
{
    if (!obj)
        return std::nullopt;

    if (IsSubTypeFloat(obj))
        return PyFloat_AsDouble(obj);

    else if (IsSubTypeLong(obj))
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


core::CArray Iterable_AsArray(PyObject* Obj)
{
    core::CArray retArr;

    PyObject* iterator = PyObject_GetIter(Obj);
    if (!iterator)
        throw std::exception("An iterable object expected");

    PyObject* item{ nullptr };
    while ((item = PyIter_Next(iterator)) != nullptr)
    {
        if (auto Variant = PyObject_AsCObject(item))
            retArr.push_back(std::move(Variant));
        else
        {
            Py_DECREF(item);
            Py_DECREF(iterator);
            throw std::exception("expected int/float/string/complex");
        }

        Py_DECREF(item);
    }

    Py_DECREF(iterator);

    return retArr;
}




std::unique_ptr<core::CObject> PyObject_AsCObject(PyObject* Obj)
{
    if (IsSubTypeNone(Obj))
    {
        return std::make_unique<core::CNone>();
    }

    else if (IsSubTypeRealNumber(Obj))
    {
        if (PyLong_CheckExact(Obj))
        {
            int Val = PyLong_AsLong(Obj);
            return std::make_unique<core::CInteger>(Val);
        }

        else if (PyFloat_CheckExact(Obj))
        {
            double Val = PyFloat_AsDouble(Obj);
            return std::make_unique<core::CDouble>(Val);
        }
    }

    else if (IsExactTypeString(Obj))
    {
        return std::make_unique<core::CString>(PyUnicode_AsWideCharString(Obj, nullptr));
    }

    else if (PyComplex_Check(Obj))
    {
        auto CComplex = PyComplex_AsCComplex(Obj);
        auto Complex = core::CComplexNumber(CComplex.real, CComplex.imag);

        return std::make_unique<core::CComplexNumber>(Complex);
    }

    return nullptr;
}



PyObject* PyObject_FromCObject(const core::CObject* variant)
{
    if (variant->GetType() == (int)core::CObject::TYPE::DOUBLE)
        return Py_BuildValue("d", variant->to_double().value());

    else if (variant->GetType() == (int)core::CObject::TYPE::INT)
        return Py_BuildValue("i", variant->to_int().value());

    else if (variant->GetType() == (int)core::CObject::TYPE::STRING)
    {
        auto str = variant->to_string();
        return Py_BuildValue("u", str.c_str());
    }

    else if (variant->GetType() == (int)core::CObject::TYPE::COMPLEX)
    {
        std::complex<double> Complex = variant->to_complex().value();
        return PyComplex_FromDoubles(Complex.real(), Complex.imag());
    }

    else if (variant->GetType() == (int)core::CObject::TYPE::NONE)
        return Py_BuildValue("");


    return nullptr;
}