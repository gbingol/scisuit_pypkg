#pragma once


#include <Python.h>

#include <vector>
#include <list>
#include <optional>
#include <string>
#include <memory>
#include <complex>
#include <functional>


#include "dllimpexp.h"





/*
    callableObj: Python callable object.
    return value is passed to another function which takes a functional.
    Ex: double result = math::simpson(func, a, b, iter);
*/
std::function<double(double)> Make1DFunction(PyObject* callableObj);


/*
    callableObj: Python callable object.
    return value is passed to another function which takes a functional.
*/
std::function<std::complex<double>(std::complex<double>)>
    MakeComplexFunction(PyObject* callableObj);



static std::optional<double> GetAsRealNumber(PyObject* obj)
{
	if (!obj)
		return std::nullopt;

	if (PyFloat_Check(obj))
		return PyFloat_AsDouble(obj);

	else if (PyLong_Check(obj))
		return (double)PyLong_AsLong(obj);

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




#ifndef IF_PYERR_RET
#define IF_PYERR_RET(EXPRESSION, ERROR, ERRMSG)	\
	if((EXPRESSION)){							\
		PyErr_SetString(ERROR, ERRMSG);	\
		return nullptr;									\
	}
#endif



#ifndef IF_PYERRRUNTIME_RET
#define IF_PYERRRUNTIME_RET(EXPRESSION, ERRMSG)	\
	IF_PYERR_RET(EXPRESSION, PyExc_RuntimeError, ERRMSG)
#endif 


#ifndef IF_PYERRVALUE_RET
#define IF_PYERRVALUE_RET(EXPRESSION, ERRMSG)	\
	IF_PYERR_RET(EXPRESSION, PyExc_ValueError, ERRMSG)
#endif // !ASSERTEXPRESSION


#ifndef CHECKPOSITIVE_RET
#define CHECKPOSITIVE_RET(OBJ, ERRMSG)		\
	IF_PYERR_RET(OBJ <= 0, PyExc_ValueError, ERRMSG)	
#endif

#ifndef CHECKNONNEGATIVE_RET
#define CHECKNONNEGATIVE_RET(OBJ, ERRMSG)								\
	IF_PYERR_RET(OBJ < 0.0, PyExc_ValueError, ERRMSG)
#endif


#ifndef CHECKRANGE_RET
#define CHECKRANGE_RET(OBJ, MIN, MAX, ERRMSG)										\
	if ((OBJ) < 0 || (OBJ) > MAX){													\
		PyErr_SetString(PyExc_ValueError, ERRMSG);								\
		return nullptr;															\
	}
#endif


#ifndef ASSERT_CALLABLE_RET
#define ASSERT_CALLABLE_RET(OBJ, ERRMSG) \
    if (PyCallable_Check((OBJ)) == false){ \
        PyErr_SetString(PyExc_TypeError, (ERRMSG));     \
        return nullptr;                                  \
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
