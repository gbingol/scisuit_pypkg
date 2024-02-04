#include "plot.h"

#include <list>

#include <wx/wx.h>

#include <core/dtypes/basetypes.h>
#include <core/dtypes/array.h>
#include <core/dtypes/datatable.h>

#include <plotter/charts/scatterchart.h>
#include <plotter/charts/barchart.h>
#include <plotter/charts/boxwhiskerchart.h>
#include <plotter/charts/histogramchart.h>
#include <plotter/charts/linechart.h>
#include <plotter/charts/piechart.h>


#include <plotter/windows/frmsingleplot.h>
#include <plotter/elems/chartelement.h>
#include <plotter/elems/trendline.h>


#include "wrapperfuncs.h"
#include "plot_helper.h"


using namespace charts;

static wxApp* s_APP = nullptr;
static CFrmPythonPlot* s_CurPlotWnd = nullptr;
static std::list< CFrmPythonPlot*> s_PlotWndList;

#define MAKE_BAR_LINE_CHART(TYPE)                                                 \
	if (!s_CurPlotWnd)                                                            \
	{                                                                             \
		IF_PYERRRUNTIME_RET(LabelsObj == Py_None, "'labels' must be specified!"); \
		frmPlot = new CFrmPythonPlot(nullptr);                                    \
		auto Rect = frmPlot->GetClientRect(); \
		auto ChartBase = std::make_unique<TYPE>(frmPlot, Rect); \
		frmPlot->SetChart(std::move(ChartBase)); \
		s_CurPlotWnd = frmPlot;\
	}\
	else{\
		frmPlot = s_CurPlotWnd;\
	}







PyObject* c_plot_bar(PyObject* args, PyObject* kwargs)
{
	CBarVertChart* ColChrt = nullptr;

	core::CArray LabelData;
		
	//Default type is clustered
	std::wstring Type = L"c";

	PyObject* LabelsObj = Py_None, * HeightObj = Py_None, *StyleObj = Py_None;
	PyObject* FillObj = Py_None, * LineObj = Py_None;

	const char* kwlist[] = { "height", "labels", "style", "fill", "line", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOOO", const_cast<char**>(kwlist),
		&HeightObj, &LabelsObj, &StyleObj, &FillObj, &LineObj))
	{
		return nullptr;
	}

	auto Data = Iterable_As1DVector(HeightObj);

	try
	{
		if (LabelsObj != Py_None)
		{
			LabelData = Iterable_AsArray(LabelsObj);
			IF_PYERRVALUE_RET(LabelData.size() < 2, "At least 2 labels expected.")
		}

		if (StyleObj != Py_None)
			Type = CheckString(StyleObj, "style must be type string");

		CFrmPythonPlot* frmPlot = nullptr;

		if (Type == "c") {
			MAKE_BAR_LINE_CHART(CBarVertClusterChart);
			ColChrt = ((CBarVertClusterChart*)frmPlot->GetChart());
		}

		else if (Type == "s") {
			MAKE_BAR_LINE_CHART(CBarVertStkChart);
			ColChrt = ((CBarVertStkChart*)frmPlot->GetChart());
		}

		else if (Type == "%") {
			MAKE_BAR_LINE_CHART(CBarVertPerStkChart);
			ColChrt = ((CBarVertPerStkChart*)frmPlot->GetChart());
		}
		else
		{
			PyErr_SetString(PyExc_ValueError, "'s', 'c' or '%' for stacked, clustered and %-stacked");
			return nullptr;
		}

		auto DataCol = std::make_shared<core::CRealColData>(Data);
		auto LblCol = std::make_shared<core::CStrColData>(LabelData.getstrings());
		auto DataTbl = std::make_unique<core::CGenericDataTable>();
		DataTbl->append_col(LblCol);
		DataTbl->append_col(DataCol);

		CBarVertSeries* Series = nullptr;
		if (Type == "c")
			Series = new CBarVertClusterSeries((CBarVertClusterChart*)ColChrt, std::move(DataTbl));

		else if (Type == "s")
			Series = new CBarVertStkSeries((CBarVertStkChart*)ColChrt, std::move(DataTbl));

		else if (Type == "%")
			Series = new CBarVertPerStkSeries((CBarVertPerStkChart*)ColChrt, std::move(DataTbl));

		wxPen Pen = Series->GetPen();
		if (LineObj != Py_None)
			PreparePen(LineObj, Pen);
		Series->SetPen(Pen);


		wxBrush Brush = Series->GetBrush();
		if (FillObj != Py_None)
			PrepareBrush(FillObj, Brush);
		Series->SetBrush(Brush);

		auto UniqueSeries = std::unique_ptr<CBarVertSeries>(Series);
		ColChrt->AddSeries(std::move(UniqueSeries));
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}



/**************************************************************************************/

PyObject* c_plot_barh(PyObject* args, PyObject* kwargs)
{
	CBarHorizChart* BarHorChart = nullptr;

	core::CArray LabelData;
		
	//Default type is clustered
	std::wstring Type = L"c";

	PyObject* LabelsObj = Py_None, * WidthObj = Py_None, *TypeObj = Py_None;
	PyObject* FillObj = Py_None, *LineObj = Py_None;
	
	const char* kwlist[] = { "width", "labels", "style", "fill", "line", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOOO", const_cast<char**>(kwlist),
		&WidthObj, &LabelsObj, &TypeObj, &FillObj, &LineObj))
	{
		return nullptr;
	}

	auto Data = Iterable_As1DVector(WidthObj);

	try
	{
		if (LabelsObj != Py_None)
		{
			LabelData = Iterable_AsArray(LabelsObj);
			IF_PYERRVALUE_RET(LabelData.size() < 2, "At least 2 labels expected.")
		}

		if (TypeObj != Py_None)
		{
			Type = CheckString(TypeObj, "type must be type string");

			std::transform(Type.begin(), Type.end(), Type.begin(), ::tolower);

			bool AcceptableType = Type == "s" || Type == "c" || Type == "%";
			IF_PYERRVALUE_RET(!AcceptableType, "'s', 'c' or '%' for stacked, clustered and percent-stacked");
		}


		CFrmPythonPlot* frmPlot = nullptr;

		if (Type == "c") {
			MAKE_BAR_LINE_CHART(CBarHorizClusterChart);
			BarHorChart = ((CBarHorizClusterChart*)frmPlot->GetChart());
		}

		else if (Type == "s") {
			MAKE_BAR_LINE_CHART(CBarHorizStkChart);
			BarHorChart = ((CBarHorizStkChart*)frmPlot->GetChart());
		}

		else if (Type == "%") {
			MAKE_BAR_LINE_CHART(CBarHorizPerStkChart);
			BarHorChart = ((CBarHorizPerStkChart*)frmPlot->GetChart());
		}

		auto DataCol = std::make_shared<core::CRealColData>(Data);
		auto LblCol = std::make_shared<core::CStrColData>(LabelData.getstrings());
		auto DataTbl = std::make_unique<core::CGenericDataTable>();
		DataTbl->append_col(LblCol);
		DataTbl->append_col(DataCol);

		CBarHorizSeries* Series = nullptr;
		if (Type == "c")
			Series = new CBarHorizClusterSeries((CBarHorizClusterChart*)BarHorChart, std::move(DataTbl));

		else if (Type == "s")
			Series = new CBarHorizStkSeries((CBarHorizStkChart*)BarHorChart, std::move(DataTbl));

		else if (Type == "%")
			Series = new CBarHorizPerStkSeries((CBarHorizPerStkChart*)BarHorChart, std::move(DataTbl));

		wxPen Pen = Series->GetPen();
		if (LineObj != Py_None)
			PreparePen(LineObj, Pen);
		Series->SetPen(Pen);


		wxBrush Brush = Series->GetBrush();
		if (FillObj != Py_None)
			PrepareBrush(FillObj, Brush);
		Series->SetBrush(Brush);


		auto UniqueSeries = std::unique_ptr<CBarHorizSeries>(Series);
		BarHorChart->AddSeries(std::move(UniqueSeries));
	}
	CATCHRUNTIMEEXCEPTION_RET();

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
	IF_PYERRVALUE_RET(Data.size() == 0, "Data does not contain any valid element.");

	try
	{
		CFrmPythonPlot* frmPlot = nullptr;

		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPythonPlot(nullptr);
			auto Rect = frmPlot->GetClientRect();
			auto ChartBase = std::make_unique<CBoxWhiskerChart>(frmPlot, Rect);
			frmPlot->SetChart(std::move(ChartBase));

			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		BW_Chrt = ((CBoxWhiskerChart*)frmPlot->GetChart());

		auto DataTbl = std::make_unique<core::CRealDataTable>();
		auto NumData = std::make_shared<core::CRealColData>(Data);
		DataTbl->append_col(NumData);

		auto series = std::make_unique<CBoxWhiskerSeries>(BW_Chrt, std::move(DataTbl));

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
			series->SetName(CheckString(NameObj, "name must be type string"));

		BW_Chrt->AddSeries(std::move(series));
	}
	CATCHRUNTIMEEXCEPTION_RET();

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

	bool IsCumulative = false;
	CHistogramSeries::Mode BinMode = CHistogramSeries::Mode::Frequency;
	std::variant<std::monostate, std::vector<double>, int> Breaks;

	auto Data = Iterable_As1DVector(DataObj);
	IF_PYERRVALUE_RET(Data.size() == 0, "data does not have any valid element");
	try
	{
		if (ModeObj != Py_None)
		{
			auto distmode = CheckString(ModeObj, "mode must be type string");

			if (distmode == "d") BinMode = CHistogramSeries::Mode::Density;
			else if (distmode == "f") BinMode = CHistogramSeries::Mode::Frequency;
			else if (distmode == "r") BinMode = CHistogramSeries::Mode::RelativeFreq;
		}

		if (CumulObj != Py_None)
		{
			IsCumulative = CheckBool(CumulObj, "cumulative must be type bool");
		}

		if (BreaksObj != Py_None)
		{
			if (PyLong_CheckExact(BreaksObj))
			{
				int Brk = PyLong_AsLong(BreaksObj);
				CHECKPOSITIVE_RET(Brk, "breaks, if int then must be >0");

				Breaks = Brk;
			}
			else
			{
				auto Brk = Iterable_As1DVector(BreaksObj);
				IF_PYERRVALUE_RET(Brk.size() == 0, "breaks do not contain any valid number");

				Breaks = std::move(Brk);
			}
		}

			
		CFrmPythonPlot* frmPlot{ nullptr };
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPythonPlot(nullptr);
			auto Rect = frmPlot->GetClientRect();
			auto ChartBase = std::make_unique<CHistogramChart>(frmPlot, Rect);
			frmPlot->SetChart(std::move(ChartBase));

			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Histogram = ((CHistogramChart*)frmPlot->GetChart());

		auto NumData = std::make_shared<core::CRealColData>(Data);
		auto DataTbl = std::make_unique<core::CRealDataTable>();
		DataTbl->append_col(NumData);

		auto series = std::make_unique<CHistogramSeries>(Histogram, std::move(DataTbl));

		wxPen Pen = series->GetPen();
		if (LineObj != Py_None)
			PreparePen(LineObj, Pen);
		series->SetPen(Pen);


		wxBrush Brush = series->GetBrush();
		if (FillObj != Py_None)
			PrepareBrush(FillObj, Brush);
		series->SetBrush(Brush);


		series->SetMode(BinMode);

		if (IsCumulative && BinMode != CHistogramSeries::Mode::Density)
			series->MakeCumulative(true);


		if (std::holds_alternative<std::vector<double>>(Breaks))
		{
			const auto& v = std::get<std::vector<double>>(Breaks);
			IF_PYERRRUNTIME_RET(series->SetBreakPoints(v) == false, "Invalid break points");
		}

		else if (std::holds_alternative<int>(Breaks))
		{
			int NBins = std::get<int>(Breaks) + 1;
			IF_PYERRRUNTIME_RET(NBins <= 0, "Number of breaks >0 expected");

			IF_PYERRRUNTIME_RET(series->SetNumberOfBins(NBins) == false, "Invalid number of breaks");
		}

		series->PrepareForDrawing();
		Histogram->AddSeries(std::move(series), false);
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}




/**************************************************************************************/

PyObject* c_plot_line(PyObject* args, PyObject* kwargs)
{
	CLineChartBase* LineChart = nullptr;

	core::CArray LabelData;

	//Default type is clustered (unstacked)
	std::wstring Style = L"c";
	std::wstring Name{}, Title{};

	PyObject* LabelsObj = Py_None, * YObj = Py_None, *NameObj = Py_None;
	PyObject* StyleObj = Py_None, *MarkerObj = Py_None, *LineObj = Py_None;

	const char* kwlist[] = { "y", "labels", "name", "style", "marker", "line", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOOOO", const_cast<char**>(kwlist),
		&YObj, &LabelsObj, &NameObj, &StyleObj, &MarkerObj, &LineObj))
	{
		return nullptr;
	}

	auto Data = Iterable_As1DVector(YObj);

		
	try
	{
		if (NameObj != Py_None)
			Name = CheckString(NameObj, "name must be type string");

		if (LabelsObj != Py_None)
		{
			LabelData = Iterable_AsArray(LabelsObj);
			IF_PYERRVALUE_RET(LabelData.size() < 2, "At least 2 labels expected.")
		}

		if (StyleObj != Py_None)
			Style = CheckString(StyleObj, "type must be type string");


		CFrmPythonPlot* frmPlot = nullptr;
			
		if (Style == "c") {
			MAKE_BAR_LINE_CHART(CLineClusterChart);
			LineChart = ((CLineClusterChart*)frmPlot->GetChart());
		}

		else if (Style == "s") {
			MAKE_BAR_LINE_CHART(CStackedLineChart);
			LineChart = ((CStackedLineChart*)frmPlot->GetChart());
		}

		else if (Style == "%") {
			MAKE_BAR_LINE_CHART(CPercentStackedLineChart);
			LineChart = ((CPercentStackedLineChart*)frmPlot->GetChart());
		}


		auto DataCol = std::make_shared<core::CRealColData>(Data);
		std::shared_ptr<core::CStrColData> LabelCol;
		if (LabelData.size() == 0)
			LabelCol = std::make_shared<core::CStrColData>(1, Data.size());

		else if (LabelData.size() == Data.size())
			LabelCol = std::make_shared<core::CStrColData>(LabelData.getstrings());

		else if (LabelData.size() < Data.size())
		{
			LabelCol = std::make_shared<core::CStrColData>(1, Data.size());
			for (size_t i = 0; const auto & Lbl:LabelData)
				LabelCol->set(i++, Lbl->to_string());
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

		size_t szMarker = 0;
		CLineSeriesBase* Series = nullptr;
		szMarker = CSeriesBase::GetDefMarkerSize();

		if (Style == "c")
			Series = new CLineClusterSeries((CLineClusterChart*)LineChart, std::move(DataTbl), szMarker);

		else if (Style == "s")
			Series = new CStackedLineSeries((CStackedLineChart*)LineChart, std::move(DataTbl), szMarker);

		else if (Style == "%")
			Series = new CPercentStackedLineSeries((CPercentStackedLineChart*)LineChart, std::move(DataTbl), szMarker);

		if (!Name.empty())
			Series->SetName(Name);

		wxPen LinePen = Series->GetLinePen();
		PreparePen(LineObj, LinePen);
		Series->SetLinePen(LinePen);

		PrepareMarker(MarkerObj, Series);

		auto UniqueSeries = std::unique_ptr<CLineSeriesBase>(Series);
		LineChart->AddSeries(std::move(UniqueSeries));
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}




/**************************************************************************************/

PyObject* c_plot_pie(PyObject* args, PyObject* kwargs)
{
	PyObject* DataObj = Py_None; // list/Vector
	PyObject* LabelsObj = Py_None; // list
	PyObject* ColorsObj = Py_None; //  list
	PyObject* ExplodeObj = Py_None; // list/int
	PyObject* StartAngleObj = Py_None; //int

	const char* kwlist[] = { "data", "labels", "colors", "explode", "startangle", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOOO", const_cast<char**>(kwlist),
		&DataObj,
		&LabelsObj,
		&ColorsObj,
		&ExplodeObj,
		&StartAngleObj))
	{
		return nullptr;
	}

	CPieChart* PieChart = nullptr;

	core::CArray Labels;
	std::vector<wxColor> Colors;
	int StartAngle = 0; // in degrees
	int ExplodeSeries = 0; //for whole series
	std::vector<int> Explode; //for individual data points if defined
	std::wstring Title{};
		
	auto Data = Iterable_As1DVector(DataObj);
	IF_PYERRVALUE_RET(Data.size() == 0, "data does not have any valid element");
	IF_PYERRVALUE_RET(Data.size() < 2, "data must contain at least 2 numeric values");

	try
	{
		if (LabelsObj != Py_None)
			Labels = Iterable_AsArray(LabelsObj);

		if (ColorsObj != Py_None)
		{
			Colors = CheckColors(ColorsObj);
			IF_PYERRVALUE_RET(Colors.size() == 0, "colors list does not contain any valid color");
		}

		if (StartAngleObj != Py_None)
		{
			StartAngle = CheckInt(StartAngleObj, "startangle must be type int");
			IF_PYERRVALUE_RET(StartAngle < 0 || StartAngle>359, "[0, 359] expected");
		}

		if (ExplodeObj != Py_None)
		{
			if (PyLong_CheckExact(ExplodeObj))
			{
				ExplodeSeries = CheckInt(ExplodeObj, "explode must be int/list");
				IF_PYERRVALUE_RET(ExplodeSeries < 0 || ExplodeSeries>10, "explode pie: [0, 10] expected");
			}
			else
				Explode = ExplodeDataPoints(ExplodeObj);
		}


		CFrmPythonPlot* frmPlot{ nullptr };
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPythonPlot(nullptr);
			auto Rect = frmPlot->GetClientRect();
			auto ChartBase = std::make_unique<CPieChart>(frmPlot, Rect);
			frmPlot->SetChart(std::move(ChartBase));

			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		PieChart = ((CPieChart*)frmPlot->GetChart());
			
		auto DataCol = std::make_shared<core::CRealColData>(Data);

		std::shared_ptr<core::CStrColData> LabelCol;
		if (Labels.size() == 0)
			LabelCol = std::make_shared<core::CStrColData>(1, Data.size());

		else if (Labels.size() == Data.size())
			LabelCol = std::make_shared<core::CStrColData>(Labels.getstrings());

		else if (Labels.size() < Data.size())
		{
			LabelCol = std::make_shared<core::CStrColData>(1, Data.size());
			for (size_t i = 0; const auto & Lbl:Labels)
				LabelCol->set(i++, Lbl->to_string());
		}
		else //too many labels
		{
			LabelCol = std::make_shared<core::CStrColData>(Labels.getstrings());
			size_t diff = Labels.size() - Data.size();
			LabelCol->pop_back(diff);
		}


		auto DataTbl = std::make_unique<core::CGenericDataTable>();
		DataTbl->append_col(LabelCol);
		DataTbl->append_col(DataCol);

		auto PieSeries = std::make_unique<CPieSeries>(PieChart, std::move(DataTbl));

		if (Colors.size() > 0)
			PieSeries->SetSliceColors(Colors);

		if (ExplodeSeries > 0)
			PieSeries->ExplodeSeries(ExplodeSeries);
		else if (Explode.size() > 0)
		{
			for (size_t i = 0; i < Explode.size(); ++i)
			{
				IF_PYERRRUNTIME_RET(PieSeries->ExplodeNthDataPoint(i, Explode[i]) == false, "Cannot explode data point");
			}
		}

		if (StartAngle > 0)
		{
			const float PI = 3.141592654f;
			float InRadians = (float)StartAngle / 360.0f * (2.0f * PI);

			PieSeries->SetAngleFirstSlice(InRadians);
		}

		PieChart->AddSeries(std::move(PieSeries));
	}
	CATCHRUNTIMEEXCEPTION_RET();

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

	try
	{
		if (TdbObj && TdbObj != Py_None)
		{
			auto Tdb_ = Iterable_As1DVector(TdbObj);
			IF_PYERRVALUE_RET(Tdb_.size() != 2, "Tdb must contain exactly 2 real numbers.");
				
			auto MinMax = std::ranges::minmax(Tdb_);
			Tdb = { MinMax.min, MinMax.max };
		}

		if (RHObj && RHObj != Py_None)
		{
			RH = Iterable_As1DVector(RHObj);
			IF_PYERRVALUE_RET(RH.size() < 2, "RH must contain at least 2 numeric values");
		}

		auto frmPlot = new CFrmPythonPlot(nullptr);
		auto PsyChart = std::make_unique<charts::CPsychrometricChart>(frmPlot, Tdb, RH, P);
		frmPlot->SetChart(std::move(PsyChart));

		s_CurPlotWnd = frmPlot;
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}

	

/**************************************************************************************/

PyObject* c_plot_qqnorm(PyObject* args, PyObject* kwargs)
{
	PyObject* DataObj = Py_None;
	PyObject* ShowObj = Py_None, *LineObj = Py_None, *MarkerObj = Py_None;
	PyObject* NameObj = Py_None;
		
	const char* kwlist[] = { "data","name", "show", "line", "marker",  NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOOO", const_cast<char**>(kwlist),
		&DataObj, &NameObj, &ShowObj, &LineObj, &MarkerObj))
	{
		return nullptr;
	}

	CScatterChart* QQChart = nullptr;
	bool LineShown = true;

	auto Data = Iterable_As1DVector(DataObj);

	IF_PYERRVALUE_RET(Data.size() == 0, "data does not have any valid element");
	IF_PYERRVALUE_RET(Data.size() < 2, "data must contain at least 2 numeric values");

	try
	{
		if (ShowObj != Py_None)
			LineShown = CheckBool(ShowObj, "show must be type bool");

			
		CFrmPythonPlot* frmPlot{ nullptr };
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPythonPlot(nullptr);
			auto Rect = frmPlot->GetClientRect();
			auto ChartBase = std::make_unique<CScatterChart>(frmPlot, Rect);
			frmPlot->SetChart(std::move(ChartBase));

			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		QQChart = ((CScatterChart*)frmPlot->GetChart());

		auto ColX = std::make_shared<core::CRealColData>(Data);
		auto DataTable = std::make_unique<core::CRealDataTable>();
		DataTable->append_col(ColX);

		auto series = std::make_unique<CQQSeries>(QQChart, std::move(DataTable));

		if (MarkerObj != Py_None)
			PrepareMarker(MarkerObj, series.get());

		series->ShowTheoreticalLine(LineShown);

		if (LineShown)
		{
			wxPen LinePen = series->GetLinePen();
			PreparePen(LineObj, LinePen);
			series->SetLinePen(LinePen);
		}

		if (NameObj && PyUnicode_Check(NameObj))
		{
			auto SeriesName = PyUnicode_AsWideCharString(NameObj, nullptr);
			series->SetName(SeriesName);
		}

		series->PrepareForDrawing();
		QQChart->AddSeries(std::move(series));
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}



/**************************************************************************************/

PyObject* c_plot_qqplot(PyObject* args, PyObject* kwargs)
{
	PyObject* XObj = Py_None, * YObj = Py_None;
	PyObject* MarkerObj = Py_None;

	const char* kwlist[] = { "x", "y", "marker",  NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|O", const_cast<char**>(kwlist),
		&XObj, &YObj, &MarkerObj))
	{
		return nullptr;
	}

	CScatterChart* QQChart = nullptr;

	auto DataX = Iterable_As1DVector(XObj);
	IF_PYERRVALUE_RET(DataX.size() == 0, "x does not have any valid element");
	IF_PYERRVALUE_RET(DataX.size() < 2, "x must contain at least 2 numeric values");

	auto DataY = Iterable_As1DVector(YObj);
	IF_PYERRVALUE_RET(DataY.size() == 0, "y does not have any valid element");
	IF_PYERRVALUE_RET(DataY.size() < 2, "y must contain at least 2 numeric values");

	try
	{
		CFrmPythonPlot* frmPlot{ nullptr };
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPythonPlot(nullptr);
			auto Rect = frmPlot->GetClientRect();
			auto ChartBase = std::make_unique<CScatterChart>(frmPlot, Rect);
			frmPlot->SetChart(std::move(ChartBase));

			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		QQChart = ((CScatterChart*)frmPlot->GetChart());

		IF_PYERRVALUE_RET(DataX.size() == 0, "X data is not valid");
		IF_PYERRVALUE_RET(DataY.size() == 0, "Y data is not valid");

		auto DataTable = std::make_unique<core::CRealDataTable>();
		auto ColX = std::make_shared<core::CRealColData>(DataX);
		auto ColY = std::make_shared<core::CRealColData>(DataY);
		DataTable->append_col(ColX);
		DataTable->append_col(ColY);
		auto series = std::make_unique<CQQSeries>(QQChart, std::move(DataTable));

		if (MarkerObj != Py_None)
			PrepareMarker(MarkerObj, series.get());

		series->PrepareForDrawing();
		QQChart->AddSeries(std::move(series));
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}



/**************************************************************************************/

PyObject* c_plot_quiver(PyObject* args, PyObject* kwargs)
{
	PyObject* XObj = Py_None, * YObj = Py_None, * UObj = Py_None, * VObj = Py_None; // Numpy array
	PyObject* ScaleObj = Py_None, * NameObj = Py_None;

	const char* kwlist[] = { "x", "y","u", "v", "scale", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOOO|O", const_cast<char**>(kwlist),
		&XObj, &YObj, &UObj, &VObj, &ScaleObj))
	{
		return nullptr;
	}

	CQuiverChart* Chart = nullptr;
	std::vector<double> DataX, DataY, DataU, DataV;
	bool IsScaled = false;

	IF_PYERRVALUE_RET(XObj == Py_None, "x must be specified.");
	IF_PYERRVALUE_RET(YObj == Py_None, "y must be specified.");
	IF_PYERRVALUE_RET(UObj == Py_None, "u must be specified.");
	IF_PYERRVALUE_RET(VObj == Py_None, "v must be specified.");

	DataX = Iterable_As1DVector(XObj);
	DataY = Iterable_As1DVector(YObj);
	DataU = Iterable_As1DVector(UObj);
	DataV = Iterable_As1DVector(VObj);

	IF_PYERRVALUE_RET(DataX.size() == 0, "x does not have any valid element");
	IF_PYERRVALUE_RET(DataX.size() < 2, "x must contain at least 2 numeric values");

	IF_PYERRVALUE_RET(DataY.size() == 0, "y does not have any valid element");
	IF_PYERRVALUE_RET(DataY.size() < 2, "y must contain at least 2 numeric values");

	IF_PYERRVALUE_RET(DataU.size() == 0, "u does not have any valid element");
	IF_PYERRVALUE_RET(DataU.size() < 2, "u must contain at least 2 numeric values");

	IF_PYERRVALUE_RET(DataV.size() == 0, "v does not have any valid element");
	IF_PYERRVALUE_RET(DataV.size() < 2, "v must contain at least 2 numeric values");

	IF_PYERRVALUE_RET(DataV.size() != DataU.size(), "u and v must have same number of elements");
	IF_PYERRVALUE_RET(DataX.size() != DataY.size(), "x and y must have same number of elements");
	IF_PYERRVALUE_RET(DataX.size() != DataU.size(), "x and u must have same number of elements");

	try
	{
		CFrmPythonPlot* frmPlot{ nullptr };
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPythonPlot(nullptr);
			auto Rect = frmPlot->GetClientRect();
			auto ChartBase = std::make_unique<CQuiverChart>(frmPlot, Rect);
			frmPlot->SetChart(std::move(ChartBase));

			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		Chart = ((CQuiverChart*)frmPlot->GetChart());

		if (ScaleObj != Py_None)
			IsScaled = CheckBool(ScaleObj, "scale must be boolean");

		Chart->SetScaled(IsScaled);

		auto DataTable = std::make_unique<core::CRealDataTable>();
		auto ColX = std::make_shared<core::CRealColData>(DataX);
		auto ColY = std::make_shared<core::CRealColData>(DataY);
		auto ColU = std::make_shared<core::CRealColData>(DataU);
		auto ColV = std::make_shared<core::CRealColData>(DataV);
		DataTable->append_col(ColX);
		DataTable->append_col(ColY);
		DataTable->append_col(ColU);
		DataTable->append_col(ColV);
		auto series = std::make_unique<CQuiverSeries>(Chart, std::move(DataTable));

		series->PrepareForDrawing();
		Chart->AddSeries(std::move(series));
		Chart->BoundsChanged();
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}





/**************************************************************************************/

PyObject* c_plot_scatter(PyObject* args, PyObject* kwargs)
{
	PyObject* XObj = nullptr, * YObj = nullptr;
	PyObject* NameObj = nullptr;
	PyObject* SmoothObj = nullptr, *MarkerObj = nullptr;
	PyObject* LineObj = nullptr, *TrendObj = nullptr;

	const char* kwlist[] = { "x","y", "name", "smooth", "marker", "line", "trendline", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|OOOOO", const_cast<char**>(kwlist),
		&XObj, &YObj, &NameObj, &SmoothObj,&MarkerObj, &LineObj, &TrendObj))
	{
		return nullptr;
	}

	auto xdata = Iterable_As1DVector(XObj);
	auto ydata = Iterable_As1DVector(YObj);

	IF_PYERRRUNTIME_RET(xdata.size() == 0, "'x' has no valid numeric data.");
	IF_PYERRRUNTIME_RET(ydata.size() == 0, "'y' has no valid numeric data.");

	IF_PYERRRUNTIME_RET(xdata.size() != ydata.size(), "'x' and 'y' must have same number of numeric data.");

	try
	{
		CFrmPythonPlot* frmPlot = nullptr;

		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPythonPlot(nullptr);
			auto Rect = frmPlot->GetClientRect();
			auto ChartBase = std::make_unique<CScatterChart>(frmPlot, Rect);
			frmPlot->SetChart(std::move(ChartBase));

			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;
					
		auto YData = std::make_shared<core::CRealColData>(ydata);
		auto XData = std::make_shared<core::CRealColData>(xdata);

		auto DTbl = std::make_unique<core::CRealDataTable>();
		DTbl->append_col(XData);
		DTbl->append_col(YData);

		auto Chart = ((CScatterChart*)frmPlot->GetChart());
		auto series = std::make_unique<CScatterSeries>(Chart, std::move(DTbl));

		bool IsSmooth = false;
		if (SmoothObj && SmoothObj != Py_None)
			IsSmooth = CheckBool(SmoothObj, "smooth must be bool type");

			
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
			series->SetMarkerSize(series->GetDefMarkerSize());

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
			

		if (TrendObj && TrendObj != Py_None)
			PrepareTrendline(TrendObj, Chart->GetNextColor(), series.get());
			 
		if (NameObj && PyUnicode_Check(NameObj))
		{
			auto SeriesName = PyUnicode_AsWideCharString(NameObj, nullptr);
			series->SetName(SeriesName);
		}

		Chart->AddSeries(std::move(series));
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}





/**************************************************************************************/

PyObject* c_plot_bubble(PyObject* args, PyObject* kwargs)
{
	PyObject* XObj = nullptr, * YObj = nullptr, * SizeObj = nullptr;
	PyObject* ColorObj = nullptr, * ModeObj = nullptr, * ScaleObj = nullptr;
	PyObject* LabelObj = nullptr;

	const char* kwlist[] = { "x","y", "size", "color", "mode", "scale", "label", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO|OOOO", const_cast<char**>(kwlist),
		&XObj, &YObj, &SizeObj,
		&ColorObj, &ModeObj, &ScaleObj,
		&LabelObj))
	{
		return nullptr;
	}


	auto xdata = Iterable_As1DVector(XObj);
	auto ydata = Iterable_As1DVector(YObj);
	auto sizedata = Iterable_As1DVector(SizeObj);

	IF_PYERRRUNTIME_RET(xdata.size() == 0, "x has no valid numeric data.");
	IF_PYERRRUNTIME_RET(ydata.size() == 0, "y has no valid numeric data.");
	IF_PYERRRUNTIME_RET(sizedata.size() == 0, "y has no valid numeric data.");

	IF_PYERRRUNTIME_RET(xdata.size() != ydata.size(), "'x' and 'y' must have same number of numeric data.");
	IF_PYERRRUNTIME_RET(ydata.size() != sizedata.size(), "'y' and 'size' must have same number of numeric data.");

	try
	{
		CFrmPythonPlot* frmPlot = nullptr;

		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPythonPlot(nullptr);
			auto Rect = frmPlot->GetClientRect();
			auto ChartBase = std::make_unique<CBubbleChart>(frmPlot, Rect);
			frmPlot->SetChart(std::move(ChartBase));

			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Chart = ((CBubbleChart*)frmPlot->GetChart());

		auto XData = std::make_shared<core::CRealColData>(xdata);
		auto YData = std::make_shared<core::CRealColData>(ydata);
		auto SizeData = std::make_shared<core::CRealColData>(sizedata);

		auto DTable = std::make_unique<core::CRealDataTable>();
		DTable->append_col(XData);
		DTable->append_col(YData);
		DTable->append_col(SizeData);

		auto series = std::make_unique<CBubbleSeries>(Chart, std::move(DTable));

		if (ColorObj && ColorObj != Py_None)
		{
			auto Color = CheckColor(ColorObj);
			auto Brush = series->GetBrush();

			//modify existing brush
			Brush.SetColour(Color);
			series->SetBrush(Brush);
		}

		if (ModeObj && ModeObj != Py_None)
		{
			auto mode = charts::CBubbleSeries::SIZEMODE::AREA;

			auto s = CheckString(ModeObj, "mode must be type string");
			if (s == "w" || s == "W")
				mode = charts::CBubbleSeries::SIZEMODE::WIDTH;
				
			series->SetSizeMode(mode);
		}

		if (ScaleObj && ScaleObj != Py_None)
		{
			int scl = CheckInt(ScaleObj, "scale must be type int");
			if (scl < 0 || scl>200)
				throw std::exception("scale must be an integer in the interval (0,200].");

			series->SetScalingFactor(scl);
		}

		if (LabelObj && PyUnicode_Check(LabelObj))
		{
			auto lbl = PyUnicode_AsWideCharString(LabelObj, nullptr);
			series->SetName(lbl);
		}

		Chart->AddSeries(std::move(series));
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}







/*
************************************************************************************
************************************************************************************
*/

void c_plot_figure()
{
	s_PlotWndList.push_back(s_CurPlotWnd);

	//Reset plot window so that a new plot window will be created by the calling chart
	s_CurPlotWnd = nullptr;
}

	
void c_plot_show(bool maximize)
{
	if (s_CurPlotWnd == nullptr)
		return;

	s_PlotWndList.push_back(s_CurPlotWnd);

	//c_plot_app();

	for (const auto& Wnd : s_PlotWndList)
	{
		if (maximize)
			Wnd->Maximize();

		Wnd->Show();
	}

	s_PlotWndList.clear();
	s_CurPlotWnd = nullptr;

	//c_plot_mainloop(sharedLoop);
}


void c_plot_title(PyObject* TitleObj )
{
	if (TitleObj == nullptr || s_CurPlotWnd == nullptr)
		return;

	auto Title = CheckString(TitleObj, "title must be type string");

	auto Chart = s_CurPlotWnd->GetChart();

	auto TextBox = Chart->GetChartTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::TITLE);
		TextBox = Chart->GetChartTitle();
	}

	TextBox->SetText(Title);
}


void c_plot_xlabel(PyObject* xlblObj)
{
	if (xlblObj == nullptr || s_CurPlotWnd == nullptr)
		return;

	auto XLabel = CheckString(xlblObj, "xlab must be type string");

	auto Chart = s_CurPlotWnd->GetChart();

	auto TextBox = Chart->GetHorizAxisTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::HAXISTITLE);
		TextBox = Chart->GetHorizAxisTitle();
	}

	TextBox->SetText(XLabel);
}


void c_plot_ylabel(PyObject* YlabObj)
{
	if (YlabObj == nullptr || s_CurPlotWnd == nullptr)
		return;

	auto YLabel = CheckString(YlabObj, "ylab must be type string");

	auto Chart = s_CurPlotWnd->GetChart();
	auto TextBox = Chart->GetVertAxisTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::VAXISTITLE);
		TextBox = Chart->GetVertAxisTitle();
	}

	TextBox->SetText(YLabel);
}


void c_plot_legend()
{
	if(s_CurPlotWnd == nullptr)
		return;

	s_CurPlotWnd->GetChart()->CreateElement(CChartBase::Elems::LEGEND);
}





//------------------------------------------------------------------------

	

void c_plot_app()
{
	if (s_APP)
		return;
		
	s_APP = new wxApp();
	s_APP->SetUseBestVisual(true);

	wxInitialize();
}


bool c_plot_mainloop(bool sharedLoop)
{	
	if (!s_APP)
		return true;

	CFrmPythonPlot::SetApp(s_APP);

	if (!sharedLoop)
		CFrmPythonPlot::SetCloseMode(CFrmPythonPlot::CLOSEMODE::NORMAL);
	else
		CFrmPythonPlot::SetCloseMode(CFrmPythonPlot::CLOSEMODE::HIDE_DESTROY);


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




