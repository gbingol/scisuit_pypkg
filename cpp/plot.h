#pragma once

#include <string>

#include <Python.h>
#include "dllimpexp.h"

#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_plot_boxplot(
	PyObject* args, 
	PyObject* kwargs);


EXTERN PyObject* c_plot_histogram(
	PyObject* args, 
	PyObject* kwargs);


EXTERN PyObject * c_plot_psychrometry(
	PyObject * args, 
	PyObject * kwargs);


EXTERN PyObject * c_plot_scatter(
	PyObject * args, 
	PyObject* kwargs);


/*
	are given X and Y labels or bounds
	if XHasLabel = false, then X is bounds otherwise labels
	if YHasLabel = false, then Y is bounds otherwise labels
*/
EXTERN PyObject * c_plot_canvas(
	PyObject * X, 
	PyObject* Y,
	bool XHasLabel = false, 
	bool YHasLabel = false,
	double xs=0.0,
	double ys=0.0); 


/************************************************************************************/


EXTERN void c_plot_gdi_arrow(
	double x1,
	double y1,
	double x2,
	double y2,
	double angle,
	double length,
	PyObject* PenObj);


EXTERN void c_plot_gdi_line(
	double x1,
	double y1,
	double x2,
	double y2,
	PyObject* PenObj);


//xy: bottom-left
EXTERN void c_plot_gdi_rect(
	double x,
	double y,
	double width,
	double height,
	PyObject* PenObj,
	PyObject* BrushObj);


EXTERN void c_plot_gdi_ellipse(
	double x,
	double y,
	double width,
	double height,
	PyObject* PenObj,
	PyObject* BrushObj);


//(x,y) top-left
EXTERN void c_plot_gdi_text(
	double x,
	double y,
	const char* text, 
	double angle, //positive angles are counterclockwise; the full angle is 360 degrees
	const char* color,
	PyObject* FontObj); 


// (x1,y1): start, (x2, y2):end, (xc, yc): center
EXTERN void c_plot_gdi_arc(
	double x1,
	double y1,
	double x2,
	double y2,
	double xc,
	double yc,
	PyObject* PenObj,
	PyObject* BrushObj);


EXTERN void c_plot_gdi_curve(
	PyObject* XObj,
	PyObject* YObj,
	PyObject* PenObj);


EXTERN void c_plot_gdi_polygon(
	PyObject* XObj,
	PyObject* YObj,
	PyObject* PenObj,
	PyObject* BrushObj);


//(x,y) centroid
EXTERN void c_plot_gdi_marker(
	double x,
	double y,
	const char* Type, 
	std::uint8_t Size,
	PyObject* PenObj,
	PyObject* BrushObj); 



/************************************************************************************/

EXTERN void c_plot_layout(int nrows, int ncols);

EXTERN void c_plot_subplot(
	int row,
	int col,
	int nrows = 1,
	int ncols = 1);




//start a new plot window
EXTERN void c_plot_figure();

EXTERN void c_plot_show();

EXTERN void c_plot_title(PyObject* title);
EXTERN void c_plot_xlabel(PyObject* xlabel);
EXTERN void c_plot_ylabel(PyObject* ylabel);
EXTERN void c_plot_legend();

//Either returns the limits or sets the limits
EXTERN PyObject *c_plot_axislim(PyObject *min, PyObject *max, char SelAxis='y');


/**********************************************************************************/
	
EXTERN void c_plot_app();
EXTERN bool c_plot_mainloop(bool sharedLoop = false);
EXTERN bool c_plot_ismainlooprunning();
EXTERN bool c_plot_exitmainloop();