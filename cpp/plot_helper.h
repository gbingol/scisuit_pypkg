#pragma once

#include <Python.h>
#include <string>

#include "wrapperfuncs.h"

#include <wx/wx.h>

#include <plotter/charts/chartbase.h>
#include <plotter/charts/scatterchart.h>

#include <plotter/elems/chartelement.h>
#include <plotter/elems/trendline.h>



static double CheckNumber(PyObject* Obj, const char* ErrMsg)
{
	if (!IsExactTypeRealNumber(Obj))
		throw std::exception(ErrMsg);

	return ExtractRealNumber(Obj).value();
}



static wxColour StringToColor(PyObject* Obj)
{
	std::string ColorStr = PyUnicode_AsUTF8(Obj);
	std::stringstream ss(ColorStr);

	std::vector<int> rgb;
	int c;
	while (ss >> c)
	{
		if (c > 255 || c < 0)
			throw std::runtime_error("RGB must be in [0, 255].");

		rgb.push_back(c);
	}

	if (rgb.size() != 3)
		throw std::runtime_error("Ill-formed color.");

	return wxColor(rgb[0], rgb[1], rgb[2]);
}

static wxColour StringToColor(const char* Obj)
{
	std::string ColorStr = Obj;
	std::stringstream ss(ColorStr);

	std::vector<int> rgb;
	int c;
	while (ss >> c)
	{
		if (c > 255 || c < 0)
			throw std::runtime_error("RGB must be in [0, 255].");

		rgb.push_back(c);
	}

	if (rgb.size() != 3)
		throw std::runtime_error("Ill-formed color.");

	return wxColor(rgb[0], rgb[1], rgb[2]);
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
		auto Color = StringToColor(item);
		retColors.push_back(Color);

		Py_DECREF(item);
	}

	Py_DECREF(iterator);

	return retColors;
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
			pen.SetColour(StringToColor(ObjValue));

		else if (ObjValue != Py_None && key == "width")
			pen.SetWidth(PyLong_AsLong(ObjValue));

		else if (ObjValue != Py_None && key == "style")
			pen.SetStyle((wxPenStyle) PyLong_AsLong(ObjValue));
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
			brush.SetColour(StringToColor(ObjValue));

		else if (ObjValue != Py_None && key == "style")
			brush.SetStyle((wxBrushStyle)PyLong_AsLong(ObjValue));
	}
}


//if properties are not defined in the dictionary then use the default color and style
static void PrepareFont(PyObject* Dict, wxFont& font)
{
	if (!Dict) return;
	
	PyObject* ObjKey, * ObjValue;
	Py_ssize_t pos = 0;

	while (PyDict_Next(Dict, &pos, &ObjKey, &ObjValue))
	{
		std::string key = PyUnicode_AsUTF8(ObjKey);

		if (ObjValue != Py_None && key == "facename")
			font.SetFaceName(PyUnicode_AsUTF8(ObjValue));

		else if (ObjValue != Py_None && key == "size")
			font.SetPointSize(PyLong_AsLong(ObjValue));

		else if (ObjValue != Py_None && key == "italic")
		{
			if(Py_IsTrue(ObjValue))
				font.MakeItalic();
		}

		else if (ObjValue != Py_None && key == "bold")
		{
			if(Py_IsTrue(ObjValue))
				font.MakeBold();
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
			std::string Type = PyUnicode_AsUTF8(ObjValue);

			if (Type == "s")
				Series->SetMarkerType((int)charts::IMarker::TYPE::RECT);
			else if (Type == "t")
				Series->SetMarkerType((int)charts::IMarker::TYPE::TRIANGLE);
			else if (Type == "x")
				Series->SetMarkerType((int)charts::IMarker::TYPE::XMARKER);
		}

		else if (ObjValue != Py_None && key == "size")
			Series->SetMarkerSize(PyLong_AsLong(ObjValue));

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
	std::string style = "linear";
	std::string Label{};
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
			style = PyUnicode_AsUTF8(ObjValue);

		else if (ObjValue != Py_None && key == "degree")
			Degree = PyLong_AsLong(ObjValue);

		else if (ObjValue != Py_None && key == "intercept")
			Intercept = CheckNumber(ObjValue, "intercept must be real number.");

		else if (ObjValue != Py_None && key == "line")
			PreparePen(ObjValue, pen);

		else if (key == "label")
			Label = PyUnicode_AsUTF8(ObjValue);

		else if (key == "show_stats")
			show_stats = PyObject_IsTrue(ObjValue);

		else if (key == "show_equation")
			show_equation = PyObject_IsTrue(ObjValue);
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