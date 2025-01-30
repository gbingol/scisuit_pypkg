#include "engineering.h"

#include <algorithm>
#include <unordered_map>

#include <core/core_funcs.hpp>
#include <core/eng/psychrometry.h>

#include "../wrapperfuncs.h"




PyObject* c_eng_psychrometry(PyObject* kwargs)
{
	size_t argc = PyDict_GET_SIZE(kwargs);

	IF_PYERR(argc != 3, PyExc_TypeError, "3 out of (Tdb=, Twb=, Tdp=, RH=, H=, V=, W=, P=) expected");

	PyObject* ObjKey, * ObjValue;
	Py_ssize_t pos = 0;

	TRYBLOCK();

	std::unordered_map<std::string, double> Values;

	while (PyDict_Next(kwargs, &pos, &ObjKey, &ObjValue))
	{
		std::string key = _PyUnicode_AsString(ObjKey);
		std::transform(key.begin(), key.end(), key.begin(), ::tolower);

		double val = PyFloat_AsDouble(ObjValue);
		Values[key] = key == "p" ? val * 1000 : val;
	}

	::core::eng::Psychrometry psy;
	psy.Compute(Values);

	CHECKRANGE_RET(psy.getRH(), 0.0, 100.0, "RH is out of range");
	IF_PYERR(psy.getP()<=0, PyExc_ValueError, "P <= 0.0");
	IF_PYERR(psy.getW() < 0.0, PyExc_ValueError, "W < 0.0")

	PyObject* Dict = PyDict_New();
	auto SetItem = [Dict](const char* Prop, double Val) {
		PyDict_SetItemString(Dict, Prop, PyFloat_FromDouble(Val));
	};

	SetItem("Tdb", psy.getTdb());
	SetItem("Twb", psy.getTwb());
	SetItem("Tdp", psy.getTdp());
	SetItem("P", psy.getP() / 1000);
	SetItem("Pw", psy.getPw() / 1000);
	SetItem("Pws", psy.getPws() / 1000);
	SetItem("W", psy.getW());

	if (psy.getWs() >= 0)
		SetItem("Ws", psy.getWs());

	SetItem("RH", psy.getRH());
	SetItem("H", psy.getH());
	SetItem("V", psy.getV());

	return Dict;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}