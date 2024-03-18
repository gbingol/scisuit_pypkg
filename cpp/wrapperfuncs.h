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




namespace core
{
    class CObject;
    class CVector;
    class CArray;
}

extern PyTypeObject PythPoly_Type;



DLLPYBIND bool IsNumpyInt(PyObject* obj);
DLLPYBIND bool IsNumpyFloat(PyObject* obj);

//extract real number (float or integer) from obj
DLLPYBIND std::optional<double> ExtractRealNumber(PyObject* obj);


//Is obj a Python subtype None
static bool IsSubTypeNone(PyObject* obj)
{
    return PyType_IsSubtype(obj->ob_type, &_PyNone_Type) == 0 ? false : true;
}


//Is obj a Python subtype bool
static bool IsSubTypeBool(PyObject* obj)
{
    return PyType_IsSubtype(obj->ob_type, &PyBool_Type) == 0 ? false : true;
}


static bool IsExactTypeBool(PyObject* obj)
{
    std::string TypeName = obj->ob_type->tp_name;
    return std::strcmp(TypeName.c_str(), "bool") == 0 ? true : false;
}


//Is obj a Python long
static bool IsSubTypeLong(PyObject* obj)
{
    return PyType_IsSubtype(obj->ob_type, &PyLong_Type) == 0 ? false : true;
}


static bool IsExactTypeLong(PyObject* obj)
{
    return PyLong_CheckExact(obj);
}


//is obj a Python float 
static bool IsSubTypeFloat(PyObject* obj)
{
    return PyType_IsSubtype(obj->ob_type, &PyFloat_Type) == 0 ? false : true;
}


static bool IsExactTypeFloat(PyObject* obj)
{
    return PyFloat_CheckExact(obj);
}


//is obj a real number (Python float or Python integer or bool)
static bool IsSubTypeRealNumber(PyObject* obj)
{
    return IsSubTypeLong(obj) || IsSubTypeFloat(obj);
}



//is obj a real number
static bool IsExactTypeRealNumber(PyObject* obj)
{
    return IsExactTypeLong(obj) || IsExactTypeFloat(obj);
}


//is obj a str
static bool IsExactTypeString(PyObject* obj)
{
    std::string TypeName = obj->ob_type->tp_name;
    return std::strcmp(TypeName.c_str(), "str") == 0 ? true : false;
}



PyObject* List_FromCVector(const core::CVector& Vec);

template <typename T=double>
std::vector<T> Iterable_As1DVector(PyObject* Obj)
{
    std::vector<T> Vec;

    PyObject* iterator = PyObject_GetIter(Obj);
    if (!iterator)
        throw std::exception("An iterable object expected");

    PyObject* item{ nullptr };
    while ((item = PyIter_Next(iterator)) != nullptr)
    {
        if constexpr (std::is_floating_point_v<T>)
        {
            if (auto Num = ExtractRealNumber(item))
                Vec.push_back(Num.value());
        }

        else if constexpr (std::is_integral_v<T>)
        {
            if (IsSubTypeLong(item))
                Vec.push_back(PyLong_AsLong(item));
        }

		else if constexpr(std::is_same_v<T, std::string>)
		{
			auto UnicodeObj = PyObject_Str(item);
			Vec.push_back(std::string(PyUnicode_AsUTF8(UnicodeObj)));
		}

        Py_DECREF(item);
    }

    Py_DECREF(iterator);

    return Vec;
}



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
