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


#include <plotter/windows/frmplot.h>
#include <plotter/elems/chartelement.h>
#include <plotter/elems/trendline.h>


#include "wrapperfuncs.h"
#include "plot_helper.h"




using namespace charts;

static wxApp* s_APP = nullptr;
static CFrmPlot* s_CurPlotWnd = nullptr;
static std::list< CFrmPlot*> s_PlotWndList;

//Layout
static char s_NROWS = -1, s_NCOLS = -1;


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
static SubPlotInfo s_SubPlotInfo;




PyObject* c_plot_bar(PyObject* args, PyObject* kwargs)
{
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

	if (StyleObj != Py_None)
		Type = PyUnicode_AsWideCharString(StyleObj, nullptr);

	auto Data = Iterable_As1DVector(HeightObj);
	IF_PYERRVALUE_RET(Data.size() == 0, "height does not contain any numeric element.");

	CFrmPlot* frmPlot{ nullptr };
	CBarVertChart* Chart{nullptr};

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
		if (Type  == L"c")
		{
			auto BarChrt = std::make_unique<CBarVertClusterChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}

		else if (Type == L"s") 
		{
			auto BarChrt = std::make_unique<CBarVertStkChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}

		else if (Type == L"%") 
		{
			auto BarChrt = std::make_unique<CBarVertPerStkChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}
	}
	else
		frmPlot = s_CurPlotWnd;

	
	if (Type == L"c")
		Chart = (CBarVertClusterChart*)frmPlot->GetActiveChart();
	else if (Type == L"s") 
		Chart = (CBarVertStkChart*)frmPlot->GetActiveChart();
	else if (Type == L"%") 
		Chart = (CBarVertPerStkChart*)frmPlot->GetActiveChart();


	try
	{
		if (LabelsObj != Py_None)
			LabelData = Iterable_AsArray(LabelsObj);

		auto DataCol = std::make_shared<core::CRealColData>(Data);
		auto LblCol = std::make_shared<core::CStrColData>(LabelData.getstrings());
		auto DataTbl = std::make_unique<core::CGenericDataTable>();
		DataTbl->append_col(LblCol);
		DataTbl->append_col(DataCol);

		CBarVertSeries* Series = nullptr;
		if (Type == L"c")
			Series = new CBarVertClusterSeries((CBarVertClusterChart*)Chart, std::move(DataTbl));

		else if (Type == L"s")
			Series = new CBarVertStkSeries((CBarVertStkChart*)Chart, std::move(DataTbl));

		else if (Type == L"%")
			Series = new CBarVertPerStkSeries((CBarVertPerStkChart*)Chart, std::move(DataTbl));

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
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}



/**************************************************************************************/

PyObject* c_plot_barh(PyObject* args, PyObject* kwargs)
{
	
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

	if (TypeObj != Py_None)
		Type = PyUnicode_AsWideCharString(TypeObj, nullptr);

	auto Data = Iterable_As1DVector(WidthObj);
	IF_PYERRVALUE_RET(Data.size() == 0, "width does not contain any numeric element.");

	CFrmPlot* frmPlot{ nullptr };
	CBarHorizChart* Chart{nullptr};
	
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
		if (Type  == L"c")
		{
			auto BarChrt = std::make_unique<CBarHorizClusterChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}

		else if (Type == L"s") 
		{
			auto BarChrt = std::make_unique<CBarHorizStkChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}

		else if (Type == L"%") 
		{
			auto BarChrt = std::make_unique<CBarHorizPerStkChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BarChrt));
		}
	}
	else
		frmPlot = s_CurPlotWnd;

	
	
	if (Type == L"c")
		Chart = (CBarHorizClusterChart*)frmPlot->GetActiveChart();
	else if (Type == L"s") 
		Chart = (CBarHorizStkChart*)frmPlot->GetActiveChart();
	else if (Type == L"%") 
		Chart = (CBarHorizPerStkChart*)frmPlot->GetActiveChart();
	
	try
	{
		if (LabelsObj != Py_None)
			LabelData = Iterable_AsArray(LabelsObj);

		auto DataCol = std::make_shared<core::CRealColData>(Data);
		auto LblCol = std::make_shared<core::CStrColData>(LabelData.getstrings());
		auto DataTbl = std::make_unique<core::CGenericDataTable>();
		DataTbl->append_col(LblCol);
		DataTbl->append_col(DataCol);

		CBarHorizSeries* Series = nullptr;
		if (Type == "c")
			Series = new CBarHorizClusterSeries((CBarHorizClusterChart*)Chart, std::move(DataTbl));

		else if (Type == "s")
			Series = new CBarHorizStkSeries((CBarHorizStkChart*)Chart, std::move(DataTbl));

		else if (Type == "%")
			Series = new CBarHorizPerStkSeries((CBarHorizPerStkChart*)Chart, std::move(DataTbl));

		wxPen Pen = Series->GetPen();
		if (LineObj != Py_None)
			PreparePen(LineObj, Pen);
		Series->SetPen(Pen);


		wxBrush Brush = Series->GetBrush();
		if (FillObj != Py_None)
			PrepareBrush(FillObj, Brush);
		Series->SetBrush(Brush);


		auto UniqueSeries = std::unique_ptr<CBarHorizSeries>(Series);
		Chart->AddSeries(std::move(UniqueSeries));

		s_SubPlotInfo = SubPlotInfo();
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
	IF_PYERRVALUE_RET(Data.size() == 0, "Data does not contain any numeric element.");

	try
	{
		CFrmPlot* frmPlot = nullptr;

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
			series->SetName(CheckString(NameObj, "name must be string."));

		Chart->AddSeries(std::move(series));

		s_SubPlotInfo = SubPlotInfo();
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
	IF_PYERRVALUE_RET(Data.size() == 0, "data does not have any numeric element.");

	try
	{
		if (ModeObj != Py_None)
		{
			auto distmode = CheckString(ModeObj, "mode must be string.");

			if (distmode == "d") BinMode = CHistogramSeries::Mode::Density;
			else if (distmode == "f") BinMode = CHistogramSeries::Mode::Frequency;
			else if (distmode == "r") BinMode = CHistogramSeries::Mode::RelativeFreq;
		}

		if (CumulObj != Py_None)
		{
			IsCumulative = CheckBool(CumulObj, "cumulative must be bool.");
		}

		if (BreaksObj != Py_None)
		{
			if (PyLong_CheckExact(BreaksObj))
			{
				int Brk = PyLong_AsLong(BreaksObj);
				CHECKPOSITIVE_RET(Brk, "breaks, if int then must be >0 .");

				Breaks = Brk;
			}
			else
			{
				auto Brk = Iterable_As1DVector(BreaksObj);
				IF_PYERRVALUE_RET(Brk.size() == 0, "breaks do not contain any valid number.");

				Breaks = std::move(Brk);
			}
		}

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


		series->SetMode(BinMode);

		if (IsCumulative && BinMode != CHistogramSeries::Mode::Density)
			series->MakeCumulative(true);


		if (std::holds_alternative<std::vector<double>>(Breaks))
		{
			const auto& v = std::get<std::vector<double>>(Breaks);
			IF_PYERRRUNTIME_RET(series->SetBreakPoints(v) == false, "Invalid break points.");
		}

		else if (std::holds_alternative<int>(Breaks))
		{
			int NBins = std::get<int>(Breaks) + 1;
			IF_PYERRRUNTIME_RET(NBins <= 0, "Number of breaks >0 expected");

			IF_PYERRRUNTIME_RET(series->SetNumberOfBins(NBins) == false, "Invalid number of breaks.");
		}

		series->PrepareForDrawing();
		Chart->AddSeries(std::move(series), false);

		s_SubPlotInfo = SubPlotInfo();
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}




/**************************************************************************************/

PyObject* c_plot_line(PyObject* args, PyObject* kwargs)
{
	/*
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

	CFrmPlot* frmPlot = nullptr;
	if (!s_CurPlotWnd) {  
		IF_PYERRRUNTIME_RET(LabelsObj == Py_None, "'labels' must be specified!"); 
		frmPlot = new CFrmPlot(nullptr);  
		s_CurPlotWnd = frmPlot;
	}
	else{
		frmPlot = s_CurPlotWnd;
	}

	auto Rect = frmPlot->GetClientRect(); 
	auto ChartBase = std::make_unique<CLineChartBase>(frmPlot, Rect);
		
	try
	{
		if (NameObj != Py_None)
			Name = CheckString(NameObj, "name must be string.");

		if (LabelsObj != Py_None)
		{
			LabelData = Iterable_AsArray(LabelsObj);
			IF_PYERRVALUE_RET(LabelData.size() < 2, "At least 2 labels expected.")
		}

		if (StyleObj != Py_None)
			Style = CheckString(StyleObj, "type must be string.");


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
			Series = new CLineClusterSeries((CLineClusterChart*)ChartBase.get(), std::move(DataTbl), szMarker);

		else if (Style == "s")
			Series = new CStackedLineSeries((CStackedLineChart*)ChartBase.get(), std::move(DataTbl), szMarker);

		else if (Style == "%")
			Series = new CPercentStackedLineSeries((CPercentStackedLineChart*)ChartBase.get(), std::move(DataTbl), szMarker);

		if (!Name.empty())
			Series->SetName(Name);

		wxPen LinePen = Series->GetLinePen();
		PreparePen(LineObj, LinePen);
		Series->SetLinePen(LinePen);

		PrepareMarker(MarkerObj, Series);

		auto UniqueSeries = std::unique_ptr<CLineSeriesBase>(Series);
		ChartBase->AddSeries(std::move(UniqueSeries));

		frmPlot->AddChart(std::move(ChartBase));
	}
	CATCHRUNTIMEEXCEPTION_RET();
	
	*/
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


		CFrmPlot* frmPlot{ nullptr };
		if (!s_CurPlotWnd)
		{
			frmPlot = new CFrmPlot(nullptr);
			s_CurPlotWnd = frmPlot;
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Rect = frmPlot->GetClientRect();
		auto PieChart = std::make_unique<CPieChart>(frmPlot, Rect);
			
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

		auto PieSeries = std::make_unique<CPieSeries>(PieChart.get(), std::move(DataTbl));

		if (Colors.size() > 0)
			PieSeries->SetSliceColors(Colors);

		if (ExplodeSeries > 0)
			PieSeries->ExplodeSeries(ExplodeSeries);
		else if (Explode.size() > 0)
		{
			for (size_t i = 0; i < Explode.size(); ++i)
			{
				IF_PYERRRUNTIME_RET(PieSeries->ExplodeNthDataPoint(i, Explode[i]) == false, "Cannot explode data point.");
			}
		}

		if (StartAngle > 0)
		{
			const float PI = 3.141592654f;
			float InRadians = (float)StartAngle / 360.0f * (2.0f * PI);

			PieSeries->SetAngleFirstSlice(InRadians);
		}

		PieChart->AddSeries(std::move(PieSeries));

		frmPlot->AddChart(std::move(PieChart));
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
			IF_PYERRVALUE_RET(RH.size() < 2, "RH must contain at least 2 numeric values.");
		}

		auto frmPlot = new CFrmPlot(nullptr);
		auto PsyChart = std::make_unique<charts::CPsychrometricChart>(frmPlot, Tdb, RH, P);
		frmPlot->AddChart(std::move(PsyChart));

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
	PyObject* LabelObj = Py_None;
		
	const char* kwlist[] = { "data","label", "show", "line", "marker",  NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOOO", const_cast<char**>(kwlist),
		&DataObj, &LabelObj, &ShowObj, &LineObj, &MarkerObj))
	{
		return nullptr;
	}

	bool LineShown = true;

	auto Data = Iterable_As1DVector(DataObj);

	IF_PYERRVALUE_RET(Data.size() == 0, "data does not have any valid element.");
	IF_PYERRVALUE_RET(Data.size() < 2, "data must contain at least 2 numeric values.");

	try
	{
		if (ShowObj != Py_None)
			LineShown = CheckBool(ShowObj, "show must be bool.");

			
		CFrmPlot* frmPlot = nullptr;
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
			auto QQChart = std::make_unique<CScatterChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(QQChart));
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Chart = (CScatterChart*)frmPlot->GetActiveChart();
		
		auto ColX = std::make_shared<core::CRealColData>(Data);
		auto DataTable = std::make_unique<core::CRealDataTable>();
		DataTable->append_col(ColX);

		auto series = std::make_unique<CQQSeries>(Chart, std::move(DataTable));

		if (MarkerObj != Py_None)
			PrepareMarker(MarkerObj, series.get());

		series->ShowTheoreticalLine(LineShown);

		if (LineShown)
		{
			wxPen LinePen = series->GetLinePen();
			PreparePen(LineObj, LinePen);
			series->SetLinePen(LinePen);
		}

		if (LabelObj && PyUnicode_Check(LabelObj))
		{
			auto Lbl = PyUnicode_AsWideCharString(LabelObj, nullptr);
			series->SetName(Lbl);
		}

		series->PrepareForDrawing();
		Chart->AddSeries(std::move(series));

		s_SubPlotInfo = SubPlotInfo();
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

	auto DataX = Iterable_As1DVector(XObj);
	IF_PYERRVALUE_RET(DataX.size() == 0, "x does not have any valid element.");
	IF_PYERRVALUE_RET(DataX.size() < 2, "x must contain at least 2 numeric values.");

	auto DataY = Iterable_As1DVector(YObj);
	IF_PYERRVALUE_RET(DataY.size() == 0, "y does not have any valid element.");
	IF_PYERRVALUE_RET(DataY.size() < 2, "y must contain at least 2 numeric values.");

	try
	{
		CFrmPlot* frmPlot = nullptr;
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
			auto QQChart = std::make_unique<CScatterChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(QQChart));
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Chart = (CScatterChart*)frmPlot->GetActiveChart();

		IF_PYERRVALUE_RET(DataX.size() == 0, "X data is not valid.");
		IF_PYERRVALUE_RET(DataY.size() == 0, "Y data is not valid.");

		auto DataTable = std::make_unique<core::CRealDataTable>();
		auto ColX = std::make_shared<core::CRealColData>(DataX);
		auto ColY = std::make_shared<core::CRealColData>(DataY);
		DataTable->append_col(ColX);
		DataTable->append_col(ColY);
		auto series = std::make_unique<CQQSeries>(Chart, std::move(DataTable));

		if (MarkerObj != Py_None)
			PrepareMarker(MarkerObj, series.get());

		series->PrepareForDrawing();
		Chart->AddSeries(std::move(series));

		s_SubPlotInfo = SubPlotInfo();
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
		CFrmPlot* frmPlot = nullptr;

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
			auto Quiver = std::make_unique<CQuiverChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(Quiver));
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Chart = (CQuiverChart*)frmPlot->GetActiveChart();

		if (ScaleObj != Py_None)
			IsScaled = CheckBool(ScaleObj, "scale must be boolean.");

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

		s_SubPlotInfo = SubPlotInfo();
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
		CFrmPlot* frmPlot = nullptr;

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
			IsSmooth = CheckBool(SmoothObj, "smooth must be bool.");

			
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
			

		if (TrendObj && TrendObj != Py_None)
			PrepareTrendline(TrendObj, Chart->GetNextColor(), series.get());
			 
		if (NameObj && PyUnicode_Check(NameObj))
		{
			auto SeriesName = PyUnicode_AsWideCharString(NameObj, nullptr);
			series->SetName(SeriesName);
		}

		Chart->AddSeries(std::move(series));

		s_SubPlotInfo = SubPlotInfo();
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
		CFrmPlot* frmPlot = nullptr;

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
			auto BubbleChrt = std::make_unique<CBubbleChart>(frmPlot, Rect);
			frmPlot->AddChart(std::move(BubbleChrt));
		}
		else
			frmPlot = s_CurPlotWnd;

		auto Chart = (CBubbleChart*)frmPlot->GetActiveChart();
		
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
			#define enm charts::CBubbleSeries::SIZEMODE
			std::wstring s = PyUnicode_AsWideCharString(ModeObj, nullptr);
			auto mode = s == "w"? enm::WIDTH: enm::AREA;
				
			series->SetSizeMode(mode);
		}

		if (ScaleObj && ScaleObj != Py_None)
			series->SetScalingFactor(PyLong_AsLong(ScaleObj));

		if (LabelObj && PyUnicode_Check(LabelObj))
			series->SetName(PyUnicode_AsWideCharString(LabelObj, nullptr));

		Chart->AddSeries(std::move(series));

		s_SubPlotInfo = SubPlotInfo();
	}
	CATCHRUNTIMEEXCEPTION_RET();

	Py_RETURN_NONE;
}





/*
************************************************************************************
************************************************************************************
*/

void c_plot_layout(char nrows, char ncols)
{
	s_NROWS = nrows;
	s_NCOLS = ncols;
}


void c_plot_subplot(
	char row,
	char col,
	unsigned char nrows,
	unsigned char ncols)
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
	s_NROWS = s_NCOLS = -1;
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

	//reset static variables
	s_NROWS = s_NCOLS = -1;

	//c_plot_mainloop(sharedLoop);
}


void c_plot_title(PyObject* LabelObj )
{
	if (LabelObj == nullptr || s_CurPlotWnd == nullptr)
		return;

	auto Chart = s_CurPlotWnd->GetActiveChart();

	auto TextBox = Chart->GetChartTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::TITLE);
		TextBox = Chart->GetChartTitle();
	}

	if(auto Label = PyUnicode_AsWideCharString(LabelObj, nullptr))
		TextBox->SetText(Label);
}


void c_plot_xlabel(PyObject* LabelObj)
{
	if (LabelObj == nullptr || s_CurPlotWnd == nullptr)
		return;

	auto Chart = s_CurPlotWnd->GetActiveChart();

	auto TextBox = Chart->GetHorizAxisTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::HAXISTITLE);
		TextBox = Chart->GetHorizAxisTitle();
	}

	if(auto Label = PyUnicode_AsWideCharString(LabelObj, nullptr))
		TextBox->SetText(Label);
}


void c_plot_ylabel(PyObject* LabelObj)
{
	if (LabelObj == nullptr || s_CurPlotWnd == nullptr)
		return;

	auto Chart = s_CurPlotWnd->GetActiveChart();
	auto TextBox = Chart->GetVertAxisTitle();
	if (TextBox == nullptr)
	{
		Chart->CreateElement(CChartBase::Elems::VAXISTITLE);
		TextBox = Chart->GetVertAxisTitle();
	}

	if(auto Label = PyUnicode_AsWideCharString(LabelObj, nullptr))
		TextBox->SetText(Label);
}


void c_plot_legend()
{
	if(s_CurPlotWnd == nullptr)
		return;

	s_CurPlotWnd->GetActiveChart()->CreateElement(CChartBase::Elems::LEGEND);
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




