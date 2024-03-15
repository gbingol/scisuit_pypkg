#include "plot.h"

#include <list>

#include <wx/wx.h>

#include <core/dtypes/basetypes.h>
#include <core/dtypes/datatable.h>

#include <plotter/charts/scatterchart.h>
#include <plotter/charts/barchart.h>
#include <plotter/charts/boxwhiskerchart.h>
#include <plotter/charts/histogramchart.h>
#include <plotter/charts/linechart.h>

#include <plotter/windows/frmplot.h>
#include <plotter/elems/chartelement.h>
#include <plotter/elems/trendline.h>


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




PyObject* c_plot_bar(PyObject* args, PyObject* kwargs)
{	
	//Default type is clustered
	const char* Style = "c";

	PyObject* LabelsObj = Py_None, * HeightObj = Py_None, *StyleObj = Py_None;
	PyObject* FillObj = Py_None, * LineObj = Py_None;

	const char* kwlist[] = { "height", "labels", "style", "fill", "line", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|OOO", const_cast<char**>(kwlist),
		&HeightObj, &LabelsObj, &StyleObj, &FillObj, &LineObj))
	{
		return nullptr;
	}

	if (StyleObj != Py_None)
		Style = PyUnicode_AsUTF8(StyleObj);

	auto Data = Iterable_As1DVector(HeightObj);
	IF_PYERRVALUE_RET(Data.size() == 0, "height does not contain any numeric element.");

	core::CArray LabelData = Iterable_AsArray(LabelsObj);
	IF_PYERRVALUE_RET(LabelData.size() == 0, "labels does not contain any element.");

	IF_PYERRVALUE_RET(LabelData.size() != Data.size(), "len(height) = len(labels) expected.");


	CFrmPlot* frmPlot{ nullptr };

	if (!s_CurPlotWnd || (s_SubPlotInfo.row>=0 && s_SubPlotInfo.col >= 0))
	{
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPlot(nullptr, s_NROWS, s_NCOLS);
			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;


		auto Rect = frmPlot->GetRect(s_SubPlotInfo);
		if (strcmp(Style, "c") == 0)
		{
			auto BarChrt = std::make_unique<CBarVertClusterChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}

		else if (strcmp(Style, "s") == 0) 
		{
			auto BarChrt = std::make_unique<CBarVertStkChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}
	}
	else
		frmPlot = s_CurPlotWnd;

	CBarVertChart* Chart{nullptr};
	if (strcmp(Style, "c") == 0)
		Chart = (CBarVertClusterChart*)frmPlot->GetActiveChart();
	else if (strcmp(Style, "s") == 0) 
		Chart = (CBarVertStkChart*)frmPlot->GetActiveChart();


	TRYBLOCK();

	auto DataCol = std::make_shared<core::CRealColData>(Data);
	auto LblCol = std::make_shared<core::CStrColData>(LabelData.getstrings());
	auto DataTbl = std::make_unique<core::CGenericDataTable>();
	DataTbl->append_col(LblCol);
	DataTbl->append_col(DataCol);

	CBarVertSeries *Series = nullptr;
	if (strcmp(Style, "c") == 0)
		Series = new CBarVertClusterSeries((CBarVertClusterChart *)Chart, std::move(DataTbl));

	else if (strcmp(Style, "s") == 0)
		Series = new CBarVertStkSeries((CBarVertStkChart *)Chart, std::move(DataTbl));

	wxPen Pen = Series->GetPen();
	if (LineObj != Py_None)
		PreparePen(LineObj, Pen);
	Series->SetPen(Pen);

	wxBrush Brush = Series->GetBrush();
	if (FillObj != Py_None)
		PrepareBrush(FillObj, Brush);
	Series->SetBrush(Brush);

	auto UniqueSeries = std::unique_ptr<CBarVertSeries>(Series);
	Chart->AddSeries(std::move(UniqueSeries));

	s_SubPlotInfo = SubPlotInfo();
	
	return PyCapsule_New((void*)Chart, nullptr, nullptr);

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/**************************************************************************************/

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

	auto DataTbl = std::make_unique<core::CRealDataTable>();
	auto NumData = std::make_shared<core::CRealColData>(Data);
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
	

	auto NumData = std::make_shared<core::CRealColData>(Data);
	auto DataTbl = std::make_unique<core::CRealDataTable>();
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

PyObject* c_plot_line(PyObject* args, PyObject* kwargs)
{
	//Default type is clustered (unstacked)
	const char* Style = "c";

	PyObject *LabelsObj = Py_None, *YObj = Py_None;
	PyObject* LabelObj = Py_None; //series label
	PyObject* StyleObj = Py_None, *MarkerObj = Py_None, *LineObj = Py_None;

	const char* kwlist[] = { "y", "labels", "label", "style", "marker", "line", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|OOOO", const_cast<char**>(kwlist),
		&YObj, &LabelsObj, &LabelObj, &StyleObj, &MarkerObj, &LineObj))
	{
		return nullptr;
	}


	auto Data = Iterable_As1DVector(YObj);
	auto LabelData = Iterable_AsArray(LabelsObj);

	if (StyleObj != Py_None)
		Style = PyUnicode_AsUTF8(StyleObj);


	CFrmPlot* frmPlot{ nullptr };

	if (!s_CurPlotWnd || (s_SubPlotInfo.row>=0 && s_SubPlotInfo.col >= 0))
	{
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPlot(nullptr, s_NROWS, s_NCOLS);
			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Rect = frmPlot->GetRect(s_SubPlotInfo);

		if (strcmp(Style, "c") == 0)
		{
			auto BarChrt = std::make_unique<CLineClusterChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}

		else if (strcmp(Style, "s") == 0) 
		{
			auto BarChrt = std::make_unique<CStackedLineChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}

	}
	else
		frmPlot = s_CurPlotWnd;

	CLineChartBase* Chart{nullptr};
	if (strcmp(Style, "c") == 0)
		Chart = (CLineClusterChart*)frmPlot->GetActiveChart();
	else if (strcmp(Style, "s") == 0) 
		Chart = (CStackedLineChart*)frmPlot->GetActiveChart();


	TRYBLOCK();

	auto DataCol = std::make_shared<core::CRealColData>(Data);

	std::shared_ptr<core::CStrColData> LabelCol;
	if (LabelData.size() == 0)
		LabelCol = std::make_shared<core::CStrColData>(1, Data.size());

	else if (LabelData.size() == Data.size())
		LabelCol = std::make_shared<core::CStrColData>(LabelData.getstrings());

	else if (LabelData.size() < Data.size())
	{
		LabelCol = std::make_shared<core::CStrColData>(1, Data.size());
		for (size_t i = 0; const auto &Lbl : LabelData)
		{
			if (auto s = dynamic_cast<core::CString *>(Lbl.get()))
				LabelCol->set(i++, s->data());
		}
	}
	else //too many labels
	{
		LabelCol = std::make_shared<core::CStrColData>(LabelData.getstrings());
		size_t diff = LabelData.size() - Data.size();
		LabelCol->pop_back(diff);
	}


	auto DataTbl = std::make_unique<core::CGenericDataTable>();
	DataTbl->append_col(LabelCol);
	DataTbl->append_col(DataCol);
	
	CLineSeriesBase* Series = nullptr;
	if (strcmp(Style, "c") == 0)
		Series = new CLineClusterSeries((CLineClusterChart*)Chart, std::move(DataTbl), MARKERSIZE);

	else if (strcmp(Style, "s") == 0)
		Series = new CStackedLineSeries((CStackedLineChart*)Chart, std::move(DataTbl), MARKERSIZE);


	if (LabelObj != Py_None)
	{
		auto Label = PyUnicode_AsUTF8(LabelObj);
		Series->SetName(Label);
	}

	wxPen LinePen = Series->GetLinePen();
	PreparePen(LineObj, LinePen);
	Series->SetLinePen(LinePen);

	PrepareMarker(MarkerObj, Series);

	auto UniqueSeries = std::unique_ptr<CLineSeriesBase>(Series);
	Chart->AddSeries(std::move(UniqueSeries));

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
				
	auto YData = std::make_shared<core::CRealColData>(ydata);
	auto XData = std::make_shared<core::CRealColData>(xdata);

	auto DTbl = std::make_unique<core::CRealDataTable>();
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

PyObject* c_plot_canvas(PyObject* args, PyObject* kwargs)
{
	PyObject* XObj = nullptr, * YObj = nullptr;

	const char* kwlist[] = { "x","y", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", const_cast<char**>(kwlist),
		&XObj, &YObj))
	{
		return nullptr;
	}

	//lower and upper bounds of x and y
	auto xdata = Iterable_As1DVector(XObj);
	auto ydata = Iterable_As1DVector(YObj);

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
				
	auto YData = std::make_shared<core::CRealColData>(ydata);
	auto XData = std::make_shared<core::CRealColData>(xdata);

	auto DTbl = std::make_unique<core::CRealDataTable>();
	DTbl->append_col(XData);
	DTbl->append_col(YData);

	auto series = std::make_unique<CCanvasSeries>(Chart, std::move(DTbl));

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


//(x, y) top-left
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

	NumChart->DrawText(x, y, text, angle, font, textColor);

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


void c_plot_title(PyObject* LabelObj )
{
	if (LabelObj == nullptr || s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	auto Chart = s_CurPlotWnd->GetActiveChart();

	auto TextBox = Chart->GetChartTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::TITLE);
		TextBox = Chart->GetChartTitle();
	}

	if(auto Label = PyUnicode_AsUTF8(LabelObj))
		TextBox->SetText(Label);

	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_xlabel(PyObject* LabelObj)
{
	if (LabelObj == nullptr || s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();


	auto Chart = s_CurPlotWnd->GetActiveChart();

	auto TextBox = Chart->GetHorizAxisTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::HAXISTITLE);
		TextBox = Chart->GetHorizAxisTitle();
	}

	if(auto Label = PyUnicode_AsUTF8(LabelObj))
		TextBox->SetText(Label);


	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_ylabel(PyObject* LabelObj)
{
	if (LabelObj == nullptr || s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	auto Chart = s_CurPlotWnd->GetActiveChart();
	auto TextBox = Chart->GetVertAxisTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::VAXISTITLE);
		TextBox = Chart->GetVertAxisTitle();
	}

	if(auto Label = PyUnicode_AsUTF8(LabelObj))
		TextBox->SetText(Label);


	CATCHRUNTIMEEXCEPTION(NOTHING);
}


void c_plot_legend()
{
	if(s_CurPlotWnd == nullptr)
		return;

	TRYBLOCK();

	if(auto s= s_CurPlotWnd->GetActiveChart())
		s->CreateElement(CChartBase::Elems::LEGEND);
	

	CATCHRUNTIMEEXCEPTION(NOTHING);
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




