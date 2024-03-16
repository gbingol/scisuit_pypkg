#pragma once

#include <Python.h>
#include <string>

#include "wrapperfuncs.h"

#include <wx/wx.h>

#include <plotter/charts/chartbase.h>
#include <plotter/charts/numericcharts.h>

#include <plotter/elems/chartelement.h>
#include <plotter/elems/trendline.h>



static double CheckNumber(PyObject* Obj, const char* ErrMsg)
{
	if (!IsExactTypeRealNumber(Obj))
		throw std::exception(ErrMsg);

	return ExtractRealNumber(Obj).value();
}



static wxColour StringToColor(const char* Obj)
{
	std::string S = Obj;
	std::vector<int> rgb;

	if(S.at(0) != '#')
	{
		std::stringstream ss(S);
		int c;
		while (ss >> c)
		{
			if (c > 255 || c < 0)
				throw std::runtime_error("RGB must be in [0, 255].");

			rgb.push_back(c);
		}
	}

	else
	{
		// # + 6 characters
		if(S.size()<7)
			throw std::runtime_error("Hex str must be at least 6 characters.");

		S.erase(S.begin()); //remove #
		
		int i = 0;
		while (i < S.size())
		{
			auto str = S.substr(i, 2);
			char * p;
			long ColorVal = strtoul(str.c_str(), & p, 16 ); 
			if(*p!=0)
				throw std::runtime_error("Malformed hex string");
			
			if (ColorVal > 255 || ColorVal < 0)
					throw std::runtime_error("RGB must be in [0, 255].");

			rgb.push_back(ColorVal);

			i = i + 2;
		}
	}

	if (rgb.size() < 3)
			throw std::runtime_error("Ill-formed color.");

	return wxColor(rgb[0], rgb[1], rgb[2]);
}


static wxColour MakeColor(PyObject* Obj)
{
	if(PyUnicode_Check(Obj))
	{
		auto ColorStr = PyUnicode_AsUTF8(Obj);
		return StringToColor(ColorStr);
	}

	else if(PyTuple_Check(Obj) || PyList_Check(Obj))
	{
		std::vector<int> rgb;

		auto len = PyObject_Size(Obj);
		for (decltype(len) i = 0; i < len; ++i)
		{
			auto item = PyObject_GetItem(Obj, Py_BuildValue("i", i));
			if(!PyLong_Check(item))
			{
				PyErr_SetString(PyExc_RuntimeError, "RGB elements must be int");
				return wxNullColour;
			}

			int value = PyLong_AsLong(item);
			if(value < 0 || value > 255)
			{
				PyErr_SetString(PyExc_ValueError, "RGB values must be in [0, 255]");
				return wxNullColour;
			}
			rgb.push_back(value);
		}

		return wxColor(rgb[0], rgb[1], rgb[2]);
	}

	return wxNullColour;
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
		auto Color = MakeColor(item);
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
		{
			//We dont want to change the lightness but only change RGB components
			auto UserColor = MakeColor(ObjValue);
			auto penColor =  pen.GetColour() != wxNullColour ? pen.GetColour() : wxColour(0, 0, 255);
			penColor.SetRGB(UserColor.GetRGB());

			pen.SetColour(penColor);
		}

		else if (ObjValue != Py_None && key == "alpha")
		{
			//User supplies value in accordance with matplotlib 
			auto Alpha = PyFloat_AsDouble(ObjValue);

			/*
				wxWidgets: 0 completely black, 200 completely , 100 returns the same colour
				Matplotlib: <1 more transparent, >1 more dark
			*/
			int Lightness = 200 - Alpha * 100;
			auto Color = pen.GetColour() != wxNullColour ? pen.GetColour() : wxColour(0, 0, 255);
			pen.SetColour(Color.ChangeLightness(Lightness));
		}

		else if (ObjValue != Py_None && key == "width")
			pen.SetWidth(PyLong_AsLong(ObjValue));

		else if (ObjValue != Py_None && key == "style")
		{
			std::vector<std::pair<std::string, int>> v{
				{"-", 100}, {":", 101}, {"---", 102}, {"--", 103}, {"-.", 104}, {"", 106}};

			std::string style = PyUnicode_AsUTF8(ObjValue);
			for(const auto& s: v)
			{
				if(s.first == style)
				{
					pen.SetStyle((wxPenStyle)s.second);
					break;
				}
			}
		}
	}//while
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
			//We dont want to change the lightness but only change RGB components
			auto UserColor = MakeColor(ObjValue);
			auto brushColor = brush.GetColour() != wxNullColour ? brush.GetColour() : wxColour(255, 255, 255);
			brushColor.SetRGB(UserColor.GetRGB());

			brush.SetColour(brushColor);
		}

		else if (ObjValue != Py_None && key == "alpha")
		{
			//User supplies value in accordance with matplotlib 
			auto Alpha = PyFloat_AsDouble(ObjValue);

			/*
				wxWidgets: 0 completely black, 200 completely , 100 returns the same colour
				Matplotlib: <1 more transparent, >1 more dark
			*/
			int Lightness = 200 - Alpha * 100;
			auto Color = brush.GetColour() != wxNullColour ? brush.GetColour() : wxColour(255, 255, 255);
			brush.SetColour(Color.ChangeLightness(Lightness));
		}

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

		else if (ObjValue != Py_None && key == "style")
		{
			std::string style = PyUnicode_AsUTF8(ObjValue);
			if(style == "italic")
				font.MakeItalic();
			if(style == "oblique")
				font.SetStyle(wxFontStyle::wxFONTSTYLE_SLANT);
		}

		else if (ObjValue != Py_None && key == "weight")
		{
			std::string weight = PyUnicode_AsUTF8(ObjValue);
			if(weight == "bold")
				font.MakeBold();
			else if(weight == "light")
				font.SetWeight(wxFontWeight::wxFONTWEIGHT_LIGHT);
			else if(weight == "heavy")
				font.SetWeight(wxFontWeight::wxFONTWEIGHT_HEAVY);
			else if(weight == "ultrabold")
				font.SetWeight(wxFontWeight::wxFONTWEIGHT_EXTRAHEAVY);
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
	charts::CScatterSeries* Series)
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