#include "plot.h"

#include <list>
#include <numeric>

#include <wx/wx.h>


#include <plotter/charts/numericcharts.h>
#include <plotter/charts/psychrochart.h>

#include <plotter/windows/frmplot.h>
#include <plotter/elems/chartelement.h>
#include <plotter/elems/trendline.h>
#include <plotter/elems/plotareabase.h>
#include <plotter/elems/legend.h>


#include "wrapperfuncs.h"
#include "plot_helper.h"




using namespace charts;

static wxApp* s_APP = nullptr;
static constinit CFrmPlot* s_CurPlotWnd = nullptr;
static std::list< CFrmPlot*> s_PlotWndList;

//Layout
static constinit int s_NROWS = 1, s_NCOLS = 1;


/*
	After each call to charts s_SubPlotInfo is reset
	this is not a problem if the following happens:
	>>subplot(0,0) ; scatter()
	>>subplot(1,1); scatter()

	However, it might seem a problem if:
	>> subplot(0,0)
	>> scatter(); histogram()

	Here the mixed plot works because histogram has
	pointer access to scatter (both inherits from CNumericChart):
	>> auto Chart = (CHistogramChart*)frmPlot->GetActiveChart();
*/
static constinit SubPlotInfo s_SubPlotInfo = SubPlotInfo();





PyObject* c_plot_boxplot(PyObject* args, PyObject* kwargs)
{
	CBoxWhiskerChart* BW_Chrt = nullptr;

	PyObject* DataObj = Py_None, * NameObj = Py_None;
	PyObject* FillObj = Py_None, *LineObj = Py_None;

	const char* kwlist[] = { "data", "name", "fill", "line", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOO", const_cast<char**>(kwlist),
		&DataObj, &NameObj, &FillObj, &LineObj)) 
	{
		return nullptr;
	}

	auto Data = Iterable_As1DVector(DataObj);
	IF_PYERRVALUE_RET(Data.size() == 0, "Data does not contain any numeric element.");


	TRYBLOCK();

	CFrmPlot *frmPlot = nullptr;

	if (!s_CurPlotWnd || (s_SubPlotInfo.row >= 0 && s_SubPlotInfo.col >= 0))
	{
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPlot(nullptr, s_NROWS, s_NCOLS);
			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Rect = frmPlot->GetRect(s_SubPlotInfo);
		auto BW_Chrt = std::make_unique<CBoxWhiskerChart>(frmPlot, Rect);
		frmPlot->AddChart(std::move(BW_Chrt));
	}
	else
		frmPlot = s_CurPlotWnd;


	auto Chart = (CBoxWhiskerChart*)frmPlot->GetActiveChart();

	auto DataTbl = std::make_unique<charts::CRealDataTable>();
	auto NumData = std::make_shared<charts::CRealColData>(Data);
	DataTbl->append_col(NumData);

	auto series = std::make_unique<CBoxWhiskerSeries>(Chart, std::move(DataTbl));

	if (LineObj != Py_None)
	{
		wxPen Pen = series->GetPen();
		PreparePen(LineObj, Pen);
		series->SetPen(Pen);
	}

	if (FillObj != Py_None)
	{
		wxBrush Brush = series->GetBrush();
		PrepareBrush(FillObj, Brush);
		series->SetBrush(Brush);
	}

	if (NameObj != Py_None)
		series->SetName(PyUnicode_AsUTF8(NameObj));

	Chart->AddSeries(std::move(series));

	s_SubPlotInfo = SubPlotInfo();

	return PyCapsule_New((void*)Chart, nullptr, nullptr);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}





/**************************************************************************************/

PyObject* c_plot_histogram(PyObject* args, PyObject* kwargs)
{
	PyObject* DataObj; 
	PyObject* ModeObj = Py_None; //  string
	PyObject* CumulObj = Py_None; //  bool
	PyObject* BreaksObj = Py_None; //  int/list/Vector
	PyObject* FillObj = Py_None;
	PyObject* LineObj = Py_None;

	const char* kwlist[] = { "data", "mode", "cumulative", "breaks", "fill", "line", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOOOO", const_cast<char**>(kwlist),
		&DataObj, &ModeObj, &CumulObj, &BreaksObj, &FillObj, &LineObj))
	{
		return nullptr;
	}


	auto Data = Iterable_As1DVector(DataObj);
	IF_PYERRVALUE_RET(Data.size() == 0, "data does not have any numeric element.");

	TRYBLOCK();

	CFrmPlot *frmPlot{nullptr};
	if (!s_CurPlotWnd || (s_SubPlotInfo.row >= 0 && s_SubPlotInfo.col >= 0))
	{
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPlot(nullptr, s_NROWS, s_NCOLS);
			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Rect = frmPlot->GetRect(s_SubPlotInfo);
		auto Histogram = std::make_unique<CHistogramChart>(frmPlot, Rect);
		frmPlot->AddChart(std::move(Histogram));
	}
	else
		frmPlot = s_CurPlotWnd;

	auto Chart = (CHistogramChart*)frmPlot->GetActiveChart();
	

	auto NumData = std::make_shared<charts::CRealColData>(Data);
	auto DataTbl = std::make_unique<charts::CRealDataTable>();
	DataTbl->append_col(NumData);

	auto series = std::make_unique<CHistogramSeries>(Chart, std::move(DataTbl));

	wxPen Pen = series->GetPen();
	if (LineObj != Py_None)
		PreparePen(LineObj, Pen);
	series->SetPen(Pen);


	wxBrush Brush = series->GetBrush();
	if (FillObj != Py_None)
		PrepareBrush(FillObj, Brush);
	series->SetBrush(Brush);


	//From Python side value is either "f" or "d"
	auto BinMode = CHistogramSeries::Mode::Frequency;
	if (strcmp(PyUnicode_AsUTF8(ModeObj), "d") == 0) 
		BinMode = CHistogramSeries::Mode::Density;
	
	series->SetMode(BinMode);

	//Guaranteed to have bool value from Python side
	series->MakeCumulative(PyObject_IsTrue(CumulObj));


	if (BreaksObj != Py_None)
	{
		if (PyLong_CheckExact(BreaksObj))
		{
			int Breaks = (int)PyLong_AsLong(BreaksObj);
			int NBins = Breaks + 1;

			IF_PYERRRUNTIME_RET(series->SetNumberOfBins(NBins) == false, "Invalid number of breaks.");
		}
		else{
			auto Breaks = std::move(Iterable_As1DVector(BreaksObj));
			IF_PYERRRUNTIME_RET(series->SetBreakPoints(Breaks) == false, "Invalid break points.");
		}
	}

	series->PrepareForDrawing();
	Chart->AddSeries(std::move(series), false);

	s_SubPlotInfo = SubPlotInfo();

	return PyCapsule_New((void*)Chart, nullptr, nullptr);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



	
/**************************************************************************************/

PyObject* c_plot_psychrometry(PyObject* args, PyObject* kwargs)
{
	PyObject* TdbObj = nullptr; //list
	std::pair<double, double> Tdb{ 0, 90 };

	PyObject* RHObj = nullptr; //list
	std::vector<double> RH = { 10, 20, 30, 40, 50, 60, 70, 80, 90, 99.9 };

	double P = 101325;

	const char* kwlist[] = { "Tdb", "RH", "P",  NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|OOd", const_cast<char**>(kwlist), &TdbObj, &RHObj, &P))
	{
		return nullptr;
	}

	TRYBLOCK();

	if (TdbObj && TdbObj != Py_None)
	{
		auto Tdb_ = Iterable_As1DVector(TdbObj);
		IF_PYERRVALUE_RET(Tdb_.size() != 2, "Tdb must contain exactly 2 real numbers.");

		auto MinMax = std::ranges::minmax(Tdb_);
		Tdb = {MinMax.min, MinMax.max};
	}

	if (RHObj && RHObj != Py_None)
	{
		RH = Iterable_As1DVector(RHObj);
		IF_PYERRVALUE_RET(RH.size() < 2, "RH must contain at least 2 numeric values.");
	}

	auto frmPlot = new CFrmPlot(nullptr);
	auto PsyChart = std::make_unique<charts::CPsychrometricChart>(frmPlot, Tdb, RH, P);
	frmPlot->AddChart(std::move(PsyChart));

	s_CurPlotWnd = frmPlot;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/**************************************************************************************/

PyObject* c_plot_scatter(PyObject* args, PyObject* kwargs)
{
	PyObject* XObj = nullptr, * YObj = nullptr;
	PyObject* NameObj = nullptr;
	PyObject* SmoothObj = nullptr, *MarkerObj = nullptr;
	PyObject* LineObj = nullptr;

	const char* kwlist[] = { "x","y", "name", "smooth", "marker", "line", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|OOOO", const_cast<char**>(kwlist),
		&XObj, &YObj, &NameObj, &SmoothObj,&MarkerObj, &LineObj))
	{
		return nullptr;
	}

	auto xdata = Iterable_As1DVector(XObj);
	auto ydata = Iterable_As1DVector(YObj);

	IF_PYERRRUNTIME_RET(xdata.size() == 0, "'x' has no valid numeric data.");
	IF_PYERRRUNTIME_RET(ydata.size() == 0, "'y' has no valid numeric data.");

	IF_PYERRRUNTIME_RET(xdata.size() != ydata.size(), "'x' and 'y' must have same number of numeric data.");

	TRYBLOCK();

	CFrmPlot *frmPlot = nullptr;

	if (!s_CurPlotWnd || (s_SubPlotInfo.row >= 0 && s_SubPlotInfo.col >= 0))
	{
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPlot(nullptr, s_NROWS, s_NCOLS);
			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Rect = frmPlot->GetRect(s_SubPlotInfo);
		auto Scatter = std::make_unique<CScatterChart>(frmPlot, Rect);
		frmPlot->AddChart(std::move(Scatter));
	}
	else
		frmPlot = s_CurPlotWnd;

	auto Chart = (CScatterChart*)frmPlot->GetActiveChart();
				
	auto YData = std::make_shared<charts::CRealColData>(ydata);
	auto XData = std::make_shared<charts::CRealColData>(xdata);

	auto DTbl = std::make_unique<charts::CRealDataTable>();
	DTbl->append_col(XData);
	DTbl->append_col(YData);

	auto series = std::make_unique<CScatterSeries>(Chart, std::move(DTbl));

	bool IsSmooth = false;
	if (SmoothObj && SmoothObj != Py_None)
		IsSmooth = PyObject_IsTrue(SmoothObj);

	bool MarkerDef = MarkerObj && MarkerObj != Py_None;
	bool LineDef = LineObj && LineObj != Py_None;

	//Has the user defined marker or line properties
	bool MarkerLine = MarkerDef || LineDef;

	//if no marker or line defined, then show marker with default properties
	if (MarkerLine == false)
		MarkerDef = true;

	if (MarkerDef)
	{
		//give a default marker size (otherwise it is 0)	
		series->SetMarkerSize(MARKERSIZE);

		//user can modify however they want
		PrepareMarker(MarkerObj, series.get());
	}

	if (LineDef)
	{
		wxPen LinePen = series->GetLinePen();
		PreparePen(LineObj, LinePen);
		series->SetLinePen(LinePen);

		if (MarkerDef == false)
			series->SetMarkerSize(0);

		series->EnableSmoothing(IsSmooth);
	}
			
	if (NameObj && PyUnicode_Check(NameObj))
	{
		auto SeriesName = PyUnicode_AsUTF8(NameObj);
		series->SetName(SeriesName);
	}

	Chart->AddSeries(std::move(series));

	s_SubPlotInfo = SubPlotInfo();

	return PyCapsule_New((void*)Chart, nullptr, nullptr);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/****************************** Canvas Chart ***************************************/

PyObject* c_plot_canvas(
	PyObject* X, 
	PyObject* Y,
	bool ShHAxis, 
	bool ShVAxis,
	bool ShHGrid,
	bool ShVGrid)
{
	
	auto xdata = Iterable_As1DVector(X);
	auto ydata = Iterable_As1DVector(Y);
	IF_PYERRRUNTIME_RET(xdata.size() != 2, "'x' must have exactly 2 points.");
	IF_PYERRRUNTIME_RET(ydata.size() != 2, "'y' must have exactly 2 points.");
	
	TRYBLOCK();

	CFrmPlot *frmPlot = nullptr;

	if (!s_CurPlotWnd || (s_SubPlotInfo.row >= 0 && s_SubPlotInfo.col >= 0))
	{
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPlot(nullptr, s_NROWS, s_NCOLS);
			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Rect = frmPlot->GetRect(s_SubPlotInfo);
		auto Canvas = std::make_unique<CCanvasChart>(frmPlot, Rect);
		frmPlot->AddChart(std::move(Canvas));
	}
	else
		frmPlot = s_CurPlotWnd;

	auto Chart = (CCanvasChart*)frmPlot->GetActiveChart();
				
	auto YData = std::make_shared<charts::CRealColData>(ydata);
	auto XData = std::make_shared<charts::CRealColData>(xdata);

	auto DTbl = std::make_unique<charts::CRealDataTable>();
	DTbl->append_col(XData);
	DTbl->append_col(YData);

	auto series = std::make_unique<CCanvasSeries>(Chart, std::move(DTbl), ShHAxis, ShVAxis, ShHGrid, ShVGrid);

	Chart->AddSeries(std::move(series));

	s_SubPlotInfo = SubPlotInfo();
	
	return PyCapsule_New((void*)Chart, nullptr, nullptr);

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}







/*
************************************************************************************
************************************************************************************
*/

void c_plot_gdi_arrow(
	double x1,
	double y1,
	double x2,
	double y2,
	double angle,
	double length,
	PyObject* PenObj)
{
	if (s_CurPlotWnd == nullptr)
		return;

	//default pen (black, width=2 pixels, solid)
	wxPen pen = wxPen(wxColour(0, 0, 0), 2);
	PreparePen(PenObj, pen);

	auto Chart = s_CurPlotWnd->GetActiveChart();	
	auto NumChart = dynamic_cast<CNumericChart*>(Chart);

	if(NumChart == nullptr) 
	{
		PyErr_SetString(PyExc_RuntimeError, "drawing functions are only supported by Numeric Charts");
		return;
	};

	NumChart->DrawArrow(x1, y1, x2, y2, angle, length, pen);
}


void c_plot_gdi_line(
	double x1,
	double y1,
	double x2,
	double y2,
	PyObject* PenObj)
{
	if (s_CurPlotWnd == nullptr)
		return;

	//default pen (black, width=2 pixels, solid)
	wxPen pen = wxPen(wxColour(0, 0, 0), 2);
	PreparePen(PenObj, pen);

	auto Chart = s_CurPlotWnd->GetActiveChart();	
	auto NumChart = dynamic_cast<CNumericChart*>(Chart);

	if(NumChart == nullptr) 
	{
		PyErr_SetString(PyExc_RuntimeError, "drawing functions are only supported by Numeric Charts");
		return;
	};

	NumChart->DrawLine(x1, y1, x2, y2, pen);
}


//(x, y) bottom-left
void c_plot_gdi_rect(
	double x,
	double y,
	double width,
	double height,
	PyObject* PenObj,
	PyObject* BrushObj)
{
	if (s_CurPlotWnd == nullptr)
		return;

	//default pen (black, width=1 pixels, solid)
	wxPen pen = wxPen(wxColour(0, 0, 0), 1);
	PreparePen(PenObj, pen);

	//default brush (white and transparent)
	wxBrush brush = wxBrush(wxColour(255, 255, 255), wxBRUSHSTYLE_TRANSPARENT);
	PrepareBrush(BrushObj, brush);

	auto Chart = s_CurPlotWnd->GetActiveChart();	
	auto NumChart = dynamic_cast<CNumericChart*>(Chart);

	if(NumChart == nullptr) 
	{
		PyErr_SetString(PyExc_RuntimeError, "drawing functions are only supported by Numeric Charts");
		return;
	};

	NumChart->DrawRect(x, y, width, height, pen, brush);
}


//(x, y) center
void c_plot_gdi_ellipse(
	double x,
	double y,
	double width, //half width
	double height, //half height
	PyObject* PenObj,
	PyObject* BrushObj)
{
	if (s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();
	// default pen (black, width=1 pixels, solid)
	wxPen pen = wxPen(wxColour(0, 0, 0), 1);
	PreparePen(PenObj, pen);

	// default brush (white and transparent)
	wxBrush brush = wxBrush(wxColour(255, 255, 255), wxBRUSHSTYLE_TRANSPARENT);
	PrepareBrush(BrushObj, brush);

	auto Chart = s_CurPlotWnd->GetActiveChart();
	auto NumChart = dynamic_cast<CNumericChart *>(Chart);

	if (NumChart == nullptr)
	{
		PyErr_SetString(PyExc_RuntimeError, "drawing functions are only supported by Numeric Charts");
		return;
	}

	NumChart->DrawEllipse(x, y, width, height, pen, brush);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}



void c_plot_gdi_text(
	double x,
	double y,
	const char* text, 
	double angle,//positive angles are counterclockwise; the full angle is 360 degrees
	char hanchor,
	char vanchor,
	const char* color,
	PyObject* FontObj)

{
	if (s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	wxFont font(wxFontInfo(11).FaceName("Arial"));
	PrepareFont(FontObj, font);

	wxColor textColor = StringToColor(color);

	auto Chart = s_CurPlotWnd->GetActiveChart();	
	auto NumChart = dynamic_cast<CNumericChart*>(Chart);

	if(NumChart == nullptr) 
	{
		PyErr_SetString(PyExc_RuntimeError, "drawing functions are only supported by Numeric Charts");
		return;
	};

	NumChart->DrawText(x, y, text, angle, hanchor, vanchor, font, textColor);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_gdi_arc(
	double x1,
	double y1,
	double x2,
	double y2,
	double xc,
	double yc,
	PyObject* PenObj,
	PyObject* BrushObj)
{
	if (s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	//default pen (black, width=2 pixels, solid)
	wxPen pen = wxPen(wxColour(0, 0, 0), 2);
	PreparePen(PenObj, pen);

	//default brush (white and transparent)
	wxBrush brush = wxBrush(wxColour(255, 255, 255), wxBRUSHSTYLE_TRANSPARENT);
	PrepareBrush(BrushObj, brush);

	auto Chart = s_CurPlotWnd->GetActiveChart();	
	auto NumChart = dynamic_cast<CNumericChart*>(Chart);

	if(NumChart == nullptr) 
	{
		PyErr_SetString(PyExc_RuntimeError, "drawing functions are only supported by Numeric Charts");
		return;
	};

	NumChart->DrawArc(x1, y1, x2, y2, xc, yc, pen, brush);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_gdi_curve(
	PyObject* XObj,
	PyObject* YObj,
	PyObject* PenObj)
{
	if (s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	//default pen (black, width=2 pixels, solid)
	wxPen pen = wxPen(wxColour(0, 0, 0), 2);
	PreparePen(PenObj, pen);

	auto X = Iterable_As1DVector(XObj);
	auto Y = Iterable_As1DVector(YObj);

	auto Chart = s_CurPlotWnd->GetActiveChart();	
	auto NumChart = dynamic_cast<CNumericChart*>(Chart);

	if(NumChart == nullptr) 
	{
		PyErr_SetString(PyExc_RuntimeError, "drawing functions are only supported by Numeric Charts");
		return;
	};

	NumChart->DrawCurve(X, Y, pen);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_gdi_polygon(
	PyObject* XObj,
	PyObject* YObj,
	PyObject* PenObj,
	PyObject* BrushObj)
{
	if (s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	//default pen (black, width=2 pixels, solid)
	auto pen = wxPen(wxColour(0, 0, 0), 2);
	PreparePen(PenObj, pen);

	//default brush (white and transparent)
	auto brush = wxBrush(wxColour(255, 255, 255), wxBRUSHSTYLE_TRANSPARENT);
	PrepareBrush(BrushObj, brush);

	auto X = Iterable_As1DVector(XObj);
	auto Y = Iterable_As1DVector(YObj);

	auto Chart = s_CurPlotWnd->GetActiveChart();	
	auto NumChart = dynamic_cast<CNumericChart*>(Chart);

	if(NumChart == nullptr) 
	{
		PyErr_SetString(PyExc_RuntimeError, "drawing functions are only supported by Numeric Charts");
		return;
	};

	NumChart->DrawPolygon(X, Y, pen, brush);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_gdi_marker(
	double x, 
	double y, 
	const char *Type, 
	std::uint8_t Size, 
	PyObject *PenObj, 
	PyObject *BrushObj)
{
	if (s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	//default pen (black, width=2 pixels, solid)
	wxPen pen = wxPen(wxColour(0, 0, 0), 2);
	PreparePen(PenObj, pen);

	//default brush (white and transparent)
	wxBrush brush = wxBrush(wxColour(255, 255, 255), wxBRUSHSTYLE_TRANSPARENT);
	PrepareBrush(BrushObj, brush);

	auto Chart = s_CurPlotWnd->GetActiveChart();	
	auto NumChart = dynamic_cast<CNumericChart*>(Chart);

	if(NumChart == nullptr) 
	{
		PyErr_SetString(PyExc_RuntimeError, "drawing functions are only supported by Numeric Charts");
		return;
	};

	NumChart->DrawMarker(x, y, Type, Size, pen, brush);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}

/*
************************************************************************************
************************************************************************************
*/

void c_plot_layout(
	int nrows, 
	int ncols)
{
	s_NROWS = nrows;
	s_NCOLS = ncols;

	s_CurPlotWnd = nullptr;
}


void c_plot_subplot(
	int row,
	int col,
	int nrows,
	int ncols)
{
	s_SubPlotInfo.row = row;
	s_SubPlotInfo.col = col;
	s_SubPlotInfo.nrows = nrows;
	s_SubPlotInfo.ncols = ncols;
}


void c_plot_figure()
{
	s_PlotWndList.push_back(s_CurPlotWnd);

	//Reset plot window so that a new plot window will be created by the calling chart
	s_CurPlotWnd = nullptr;

	//reset static variables
	s_NROWS = s_NCOLS = 1;
}

	
void c_plot_show()
{
	TRYBLOCK();

	if (!s_CurPlotWnd)
		return;

	s_PlotWndList.push_back(s_CurPlotWnd);

	for (auto Wnd : s_PlotWndList)
		Wnd->Show();

	s_PlotWndList.clear();
	s_CurPlotWnd = nullptr;

	//reset static variables
	s_NROWS = s_NCOLS = 1;

	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_title(const char* Label)
{
	if (Label == nullptr || s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	auto Chart = s_CurPlotWnd->GetActiveChart();

	auto TextBox = Chart->GetChartTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::TITLE);
		TextBox = Chart->GetChartTitle();
	}

	TextBox->SetText(Label);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_xlabel(const char* Label)
{
	if (Label == nullptr || s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();


	auto Chart = s_CurPlotWnd->GetActiveChart();

	auto TextBox = Chart->GetHorizAxisTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::HAXISTITLE);
		TextBox = Chart->GetHorizAxisTitle();
	}

	TextBox->SetText(Label);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_ylabel(const char* Label)
{
	if (Label == nullptr || s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	auto Chart = s_CurPlotWnd->GetActiveChart();
	auto TextBox = Chart->GetVertAxisTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::VAXISTITLE);
		TextBox = Chart->GetVertAxisTitle();
	}

	TextBox->SetText(Label);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_legend(
	PyObject* nrows, 
	PyObject* ncols)
{
	if(s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	std::optional<std::size_t> NRows, NCols;

	if(auto s= s_CurPlotWnd->GetActiveChart())
	{
		if(!Py_IsNone(nrows))
			NRows = PyLong_AsLong(nrows);

		if(!Py_IsNone(ncols))
			NCols = PyLong_AsLong(ncols);

		auto xy = s->GetPlotArea()->GetTopRight();
		auto Legend = s->CreateLegend(xy, NRows, NCols);
		s->RefreshRect(Legend->GetBoundRect().Inflate(5, 5));
	}

	CATCHRUNTIMEEXCEPTION(NOTHING);
}



PyObject* c_plot_axislim(PyObject* min, PyObject* max, char SelAxis)
{
	if(s_CurPlotWnd == nullptr)
	{
		//If no chart available then min=max=0.0
		PyObject *Tuple = PyTuple_New(2);
		PyTuple_SetItem(Tuple, 0, Py_BuildValue("d", 0.0));
		PyTuple_SetItem(Tuple, 1, Py_BuildValue("d", 0.0));
		return Tuple;
	}

	TRYBLOCK();

	if(auto chart= s_CurPlotWnd->GetActiveChart())
	{
		auto Axis = SelAxis == 'y' ? chart->GetVertAxis() : chart->GetHorizAxis();
		auto Bounds = Axis->GetBounds();

		if(Py_IsNone(min) && Py_IsNone(max))
		{
			PyObject *Tuple = PyTuple_New(2);
			PyTuple_SetItem(Tuple, 0, Py_BuildValue("d", Bounds.first));
			PyTuple_SetItem(Tuple, 1, Py_BuildValue("d", Bounds.second));
			return Tuple;
		}

		if(!Py_IsNone(min))
			Axis->SetBounds(std::make_pair(PyFloat_AsDouble(min), Bounds.second), true);

		if(!Py_IsNone(max))
			Axis->SetBounds(std::make_pair(Bounds.first, PyFloat_AsDouble(max)), true);
	}

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_plot_set_xticks(
	PyObject *pos, 
	PyObject *labels,
	const char* Alignment,
	const char* Position)
{
	if(s_CurPlotWnd == nullptr)
		Py_RETURN_NONE;

	TRYBLOCK();

	if(auto chart= s_CurPlotWnd->GetActiveChart())
	{
		auto Axis = chart->GetHorizAxis();
		
		auto TickPos = Iterable_As1DVector(pos);
		Axis->SetTickPos(TickPos);

		if(std::strcmp(Alignment, "center") == 0)
			Axis->SetLabelAlignment(charts::CAxis::LABELALIGN::CENTER);
		else if(std::strcmp(Alignment, "left") == 0)
			Axis->SetLabelAlignment(charts::CAxis::LABELALIGN::LEFT);

		if(std::strcmp(Position, "bottom") == 0)
			Axis->SetLabelPos(charts::CAxis::LABELPOS::BOTTOM);
		else if (std::strcmp(Position, "top") == 0)
			Axis->SetLabelPos(charts::CAxis::LABELPOS::TOP);

		if (!Py_IsNone(labels))
		{
			auto _Labels = Iterable_As1DVector<std::string>(labels);
			Axis->SetLabels(_Labels);
		}
	}

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_plot_set_yticks(
		PyObject *pos, 
		PyObject *labels,
		const char* Alignment,
		const char* Position)
{
	if(s_CurPlotWnd == nullptr)
		Py_RETURN_NONE;

	TRYBLOCK();

	if(auto chart= s_CurPlotWnd->GetActiveChart())
	{
		auto Axis = chart->GetVertAxis();

		auto TickPos = Iterable_As1DVector(pos);
		Axis->SetTickPos(TickPos);

		if(std::strcmp(Alignment, "center") == 0)
			Axis->SetLabelAlignment(charts::CAxis::LABELALIGN::CENTER);
		else if(std::strcmp(Alignment, "top") == 0)
			Axis->SetLabelAlignment(charts::CAxis::LABELALIGN::TOP);
		else if(std::strcmp(Alignment, "bottom") == 0)
			Axis->SetLabelAlignment(charts::CAxis::LABELALIGN::BOTTOM);
		
		if(std::strcmp(Position, "left") == 0)
			Axis->SetLabelPos(charts::CAxis::LABELPOS::LEFT);
		else if(std::strcmp(Position, "right") == 0)
			Axis->SetLabelPos(charts::CAxis::LABELPOS::RIGHT);

		if(!Py_IsNone(labels))
		{
			auto _Labels = Iterable_As1DVector<std::string>(labels);
			Axis->SetLabels(_Labels);
		}
	}

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject *c_plot_set_axispos(double pos, char SelAxis)
{
	if(s_CurPlotWnd == nullptr)
		Py_RETURN_NONE;

	TRYBLOCK();

	if(auto chart= s_CurPlotWnd->GetActiveChart())
	{
		auto Axis = SelAxis == 'y'? chart->GetVertAxis() : chart->GetHorizAxis();
		auto OrthAxis = Axis->GetOrthoAxis();

		auto Bnds = OrthAxis->GetBounds();

		//pos is clamped within bounds of orthogonal axis
		Axis->CrossThrough(pos, charts::CAxis::CROSS::USER);
	}

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject *c_plot_axisscale(const char* scale, char SelAxis)
{
	if(s_CurPlotWnd == nullptr)
		Py_RETURN_NONE;

	TRYBLOCK();

	if(auto chart= s_CurPlotWnd->GetActiveChart())
	{
		auto Axis = SelAxis == 'y'? chart->GetVertAxis() : chart->GetHorizAxis();
		
		if(std::strcmp(scale, "log") == 0)
			Axis->SetScale(charts::CAxis::SCALE::LOG);
	}

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




//------------------------------------------------------------------------

	

void c_plot_app()
{
	if (s_APP)
		return;
		
	s_APP = new wxApp();
	s_APP->SetUseBestVisual(true);

	//initialize static variables
	s_CurPlotWnd = nullptr;
	s_NCOLS = s_NROWS = 1;

	wxInitialize();
}


bool c_plot_mainloop(bool sharedLoop)
{	
	if (!s_APP)
		return true;

	CFrmPlot::SetApp(s_APP);

	if (!sharedLoop)
		CFrmPlot::SetCloseMode(CFrmPlot::CLOSE::NORMAL);
	else
		CFrmPlot::SetCloseMode(CFrmPlot::CLOSE::HIDE_DESTROY);


	if (!s_APP->IsMainLoopRunning())
	{
		Py_BEGIN_ALLOW_THREADS
			s_APP->MainLoop();
		Py_END_ALLOW_THREADS
	}

	return true;
}


bool c_plot_ismainlooprunning()
{
	if (!s_APP)
		return true;

	return s_APP->IsMainLoopRunning();
}


bool c_plot_exitmainloop()
{
	if (!s_APP)
		return false;

	s_APP->ExitMainLoop();

	return true;
}




