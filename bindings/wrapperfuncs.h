#pragma once


#include <Python.h>

#include <vector>
#include <optional>
#include <string>
#include <complex>





/*
    funcObj: Python callable object.
    return value is passed to another function which takes a functional.
    Ex: double result = math::simpson(func, a, b, iter);
*/
inline auto Make1DFunction(PyObject* funcObj)
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


/*
    callableObj: Python callable object.
    return value is passed to another function which takes a functional.
*/
inline auto MakeComplexFunction(PyObject* callableObj)
{
	auto func = [=](std::complex<double> x) 
	{
        PyObject* ObjX = PyComplex_FromDoubles(x.real(), x.imag());

        PyObject* ResultObj = PyObject_CallFunction(callableObj, "O", ObjX);
        Py_DECREF(ObjX);

        if (!ResultObj) {
			auto args = std::to_string(x.real()) + " + " + std::to_string(x.imag()) + "j";
			throw std::exception(("f(" + args + ") is invalid.").c_str());
		}

        auto CompRet = PyComplex_AsCComplex(ResultObj);
        Py_DECREF(ResultObj);

        return std::complex(CompRet.real, CompRet.imag);
    };

    return func;
}



template <typename T=double>
std::optional<T> GetAsRealNumber(PyObject* obj)
{
	if (!obj)
		return std::nullopt;
	
	if constexpr (std::is_floating_point_v<T>)
	{
		if (PyFloat_Check(obj))
			return PyFloat_AsDouble(obj);

		else if (PyLong_Check(obj))
			return (double)PyLong_AsLong(obj);
	}
	else if constexpr (std::is_integral_v<T>)
	{
		if (PyFloat_Check(obj))
			return static_cast<T>(PyFloat_AsDouble(obj));

		else if (PyLong_Check(obj))
			return PyLong_AsLong(obj);
	}

	return std::nullopt;
}


static bool IsRealNum(PyObject* obj)
{
    return PyLong_Check(obj) || PyFloat_Check(obj);
}


template <typename T=double>
PyObject* List_FromVector(const std::vector<T>& Vec)
{
	if (Vec.size() == 0)
		return nullptr;

	auto List = PyList_New(Vec.size());

	for (size_t i = 0; const auto& v: Vec)
	{
		if constexpr (std::is_floating_point_v<T>)
		 	PyList_SetItem(List, i, Py_BuildValue("d", v));
		else if constexpr (std::is_integral_v<T>)
			PyList_SetItem(List, i, Py_BuildValue("i", v));
		else if constexpr(std::is_same_v<T, std::string>)
			PyList_SetItem(List, i, Py_BuildValue("s", v.c_str()));
		else
			PyList_SetItem(List, i, Py_None);
		i++;
	}

	return List;
}




template <typename T=double>
std::vector<T> Iterable_As1DVector(PyObject* Obj)
{
    std::vector<T> Vec;
    PyObject* iterator{nullptr};
    PyObject* ResultObj{nullptr};

    //if it is a numpy array (or an obje), call tolist function and work with list and numpy data types
    auto ToList = PyObject_HasAttrString(Obj, "tolist");
    if(ToList)
    {
        auto Func = PyObject_GetAttrString(Obj, "tolist");
        ResultObj = PyObject_CallNoArgs(Func);
        Py_DECREF(Func);

        iterator = PyObject_GetIter(ResultObj);
    }

    if(!iterator)
        iterator = PyObject_GetIter(Obj);

    if (!iterator)
        throw std::exception("An iterable object expected");

    PyObject* item{ nullptr };
    while ((item = PyIter_Next(iterator)) != nullptr)
    {
		if constexpr (std::is_floating_point_v<T>)
		{
			if (auto Num = GetAsRealNumber(item))
				Vec.push_back(*Num);
		}

		else if constexpr (std::is_integral_v<T>)
		{
			if (PyLong_Check(item))
				Vec.push_back(PyLong_AsLong(item));
		}

		else if constexpr(std::is_same_v<T, std::string>)
		{
			auto UnicodeObj = PyObject_Str(item);
			Vec.push_back(PyUnicode_AsUTF8(UnicodeObj));
            
            Py_DECREF(UnicodeObj);
		}

        Py_DECREF(item);
    }

    Py_DECREF(iterator);
    Py_XDECREF(ResultObj);

    return Vec;
}




#ifndef IF_PYERR
#define IF_PYERR(EXPRESSION, ERROR, ERRMSG)	\
	if((EXPRESSION)){							\
		PyErr_SetString(ERROR, ERRMSG);	\
		return nullptr;									\
	}
#endif



#ifndef CHECKRANGE_RET
#define CHECKRANGE_RET(OBJ, MIN, MAX, ERRMSG)										\
	if ((OBJ) < 0 || (OBJ) > MAX){													\
		PyErr_SetString(PyExc_ValueError, ERRMSG);								\
		return nullptr;															\
	}
#endif



#ifndef NOTHING
#define NOTHING
#endif

#ifndef TRYBLOCK
#define TRYBLOCK()								\
	try \
	{
#endif


#ifndef CATCHRUNTIMEEXCEPTION
#define CATCHRUNTIMEEXCEPTION(retVal)								\
	}catch (std::exception& e){								\
		PyErr_SetString(PyExc_RuntimeError, e.what());		\
		return retVal; \
	}
#endif
