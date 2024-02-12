#pragma once

#include <Python.h>
#include <string>

#include "wrapperfuncs.h"

#include <wx/wx.h>

#include <plotter/charts/chartbase.h>
#include <plotter/charts/scatterchart.h>

#include <plotter/elems/chartelement.h>
#include <plotter/elems/trendline.h>



static std::wstring CheckString(PyObject* Obj, const char* ErrMsg)
{
	if (!PyUnicode_Check(Obj))
		throw std::exception(ErrMsg);

	return PyUnicode_AsWideCharString(Obj, nullptr);		
}


static int CheckInt(PyObject* Obj, const char* ErrMsg)
{
	if (!PyLong_CheckExact(Obj))
		throw std::exception(ErrMsg);

	return PyLong_AsLong(Obj);
}


static double CheckNumber(PyObject* Obj, const char* ErrMsg)
{
	if (!IsExactTypeRealNumber(Obj))
		throw std::exception(ErrMsg);

	return ExtractRealNumber(Obj).value();
}



static bool CheckBool(PyObject* Obj, const char* ErrMsg)
{
	if (!IsExactTypeBool(Obj))
		throw std::exception(ErrMsg);

	return PyObject_IsTrue(Obj);
}



static std::pair<wxColor, std::string> StringToColor(PyObject* Obj)
{
	if (!PyUnicode_Check(Obj))
		return std::make_pair(wxNullColour, "color must be string.");

	std::string ColorStr = PyUnicode_AsUTF8(Obj);
	std::stringstream ss(ColorStr);

	std::vector<int> rgb;
	int c;
	while (ss >> c)
	{
		if (c > 255 || c < 0)
			return std::make_pair(wxNullColour, "RGB must be in [0, 255].");

		rgb.push_back(c);
	}

	if (rgb.size() != 3)
		return std::make_pair(wxNullColour, "Ill-formed color.");

	return std::make_pair(wxColor(rgb[0], rgb[1], rgb[2]), "");
}



static wxColor CheckColor(PyObject* Obj)
{
	auto Color = StringToColor(Obj);
	if (Color.first == wxNullColour)
		throw std::exception(Color.second.c_str());

	return Color.first;
}



static std::vector<wxColor> CheckColors(PyObject* Obj)
{
	PyObject* iterator = PyObject_GetIter(Obj);
	if (!iterator)
		throw std::exception("An iterable object expected.");

	std::vector<wxColor> retColors;
	PyObject* item{ nullptr };
	while ((item = PyIter_Next(iterator)) != nullptr)
	{
		auto Color = CheckColor(item);
		retColors.push_back(Color);

		Py_DECREF(item);
	}

	Py_DECREF(iterator);

	return retColors;
}



static std::vector<int> ExplodeDataPoints(PyObject* Obj)
{
	PyObject* iterator = PyObject_GetIter(Obj);
	if (!iterator)
		throw std::exception("An iterable object expected.");

	std::vector<int> DP;
	PyObject* item{ nullptr };
	while ((item = PyIter_Next(iterator)) != nullptr)
	{
		int Value = CheckInt(item, "explode must contain only integer items.");

		if (Value < 0 || Value>10)
			throw std::exception("explode point: [0, 10] expected.");

		DP.push_back(Value);

		Py_DECREF(item);
	}

	Py_DECREF(iterator);

	return DP;
}





//if properties are not defined in the dictionary then use the default color, width and style
static void PreparePen(PyObject* Dict, wxPen& pen)
{
	if (!Dict)
		return;
	
	
	PyObject* ObjKey, * ObjValue;
	Py_ssize_t pos = 0;

	while (PyDict_Next(Dict, &pos, &ObjKey, &ObjValue))
	{
		std::string key = PyUnicode_AsUTF8(ObjKey);

		if (ObjValue != Py_None && (key == "color" || key == "colour"))
		{
			auto Color = CheckColor(ObjValue);
			pen.SetColour(Color);
		}

		else if (ObjValue != Py_None && key == "width")
		{
			int Width = CheckInt(ObjValue, "width must be int.");
			if (Width < 0)
				throw std::exception("Width of the line must be int and >0.");

			pen.SetWidth(Width);
		}

		else if (ObjValue != Py_None && key == "style")
		{
			int Style = CheckInt(ObjValue, "pen style must be int.");
			pen.SetStyle((wxPenStyle)Style);
		}
	}	
}




//if properties are not defined in the dictionary then use the default color and style
static void PrepareBrush(PyObject* Dict, wxBrush& brush)
{
	if (!Dict) return;
	
	PyObject* ObjKey, * ObjValue;
	Py_ssize_t pos = 0;

	while (PyDict_Next(Dict, &pos, &ObjKey, &ObjValue))
	{
		std::string key = PyUnicode_AsUTF8(ObjKey);

		if (ObjValue != Py_None && (key == "color" || key == "colour"))
		{
			auto Fill = CheckColor(ObjValue);
			brush.SetColour(Fill);
		}

		else if (ObjValue != Py_None && key == "style")
		{
			auto Style = CheckInt(ObjValue, "brush style must be int.");
			brush.SetStyle((wxBrushStyle)Style);
		}
	}
}



//read from dictionary and set the marker properties of Series
static void PrepareMarker(PyObject* Dict, charts::CSeriesBase* Series)
{
	if (!Dict)
		return;

	Series->SetMarkerType((int)charts::IMarker::TYPE::CIRCLE);

	PyObject* ObjKey, * ObjValue;
	Py_ssize_t pos = 0;

	while (PyDict_Next(Dict, &pos, &ObjKey, &ObjValue))
	{
		std::string key = PyUnicode_AsUTF8(ObjKey);

		if (ObjValue != Py_None && key == "style")
		{
			auto Type = CheckString(ObjValue, "'style' must be string.");

			if (Type == "s")
				Series->SetMarkerType((int)charts::IMarker::TYPE::RECT);
			else if (Type == "t")
				Series->SetMarkerType((int)charts::IMarker::TYPE::TRIANGLE);
			else if (Type == "x")
				Series->SetMarkerType((int)charts::IMarker::TYPE::XMARKER);
		}

		else if (ObjValue != Py_None && key == "size")
		{
			int Size = CheckInt(ObjValue, "'size' must be int.");
			if (Size <= 0)
				throw std::exception("'size'>0 expected.");
			Series->SetMarkerSize(Size);
		}

		else if (ObjValue != Py_None && key == "fill")
		{
			auto Brush = Series->GetBrush();
			PrepareBrush(ObjValue, Brush);
			Series->SetBrush(Brush);
		}

		else if (ObjValue != Py_None && key == "line")
		{
			auto Pen = Series->GetPen();
			PreparePen(ObjValue, Pen);
			Series->SetPen(Pen);
		}
	}	
}



//read from dictionary and set trendline properties of Series
static void PrepareTrendline(
	PyObject* Dict, 
	wxColor DefaultColor, 
	charts::CScatterSeriesBase* Series)
{
	std::wstring style = L"linear";
	std::wstring Label{};
	int Degree = 2;
	std::optional<double> Intercept = std::nullopt;
	bool show_stats = false, show_equation = false;

	wxPen pen(DefaultColor, LINETHICK);
	pen.SetStyle(wxPenStyle::wxPENSTYLE_LONG_DASH);

	PyObject* ObjKey, * ObjValue;
	Py_ssize_t pos = 0;

	while (PyDict_Next(Dict, &pos, &ObjKey, &ObjValue))
	{
		std::string key = PyUnicode_AsUTF8(ObjKey);

		if (ObjValue != Py_None && key == "style")
			style = CheckString(ObjValue, "'style' must be string.");

		else if (ObjValue != Py_None && key == "degree")
			Degree = CheckInt(ObjValue, "'degree' must be int.");

		else if (ObjValue != Py_None && key == "intercept")
			Intercept = CheckNumber(ObjValue, "intercept must be real number.");

		else if (ObjValue != Py_None && key == "line")
			PreparePen(ObjValue, pen);

		else if (key == "label")
			Label = CheckString(ObjValue, "trendline name must be string.");

		else if (key == "show_stats")
			show_stats = CheckBool(ObjValue, "'show_stats' must be bool.");

		else if (key == "show_equation")
			show_equation = CheckBool(ObjValue, "'show_equation' must be bool.");
	}

	std::shared_ptr<charts::CTrendline> tline = nullptr;
	try
	{
		if (style == "exp")
			tline = std::make_shared<charts::CExpTrendline>(Series, pen, Intercept);

		else if (style == "linear")
			tline = std::make_shared<charts::CLinearTrendline>(Series, pen, Intercept);

		else if (style == "log")
			tline = std::make_shared<charts::CLogTrendline>(Series, pen);

		else if (style == "poly")
			tline = std::make_shared<charts::CPolyTrendline>(Series, pen, Degree, Intercept);

		else if (style == "pow")
			tline = std::make_shared<charts::CPowerTrendline>(Series, pen);
	}
	catch (std::exception& e)
	{
		throw e;
	}

	tline->SetName(Label);
	tline->ShowInfo(show_equation, show_stats);
	Series->AddTrendline(tline);
}