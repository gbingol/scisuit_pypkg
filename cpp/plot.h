#pragma once

#include <string>

#include <Python.h>
#include "dllimpexp.h"

#define EXTERN \
	extern "C" DLLPYBIND



EXTERN PyObject* c_plot_bubble(
	PyObject* args, 
	PyObject* kwargs);
	

EXTERN PyObject * c_plot_bar(
	PyObject * args, 
	PyObject * kwargs);


EXTERN PyObject * c_plot_barh(
	PyObject * args, 
	PyObject * kwargs);


EXTERN PyObject* c_plot_boxplot(
	PyObject* args, 
	PyObject* kwargs);


EXTERN PyObject* c_plot_histogram(
	PyObject* args, 
	PyObject* kwargs);


EXTERN PyObject* c_plot_line(
	PyObject* args, 
	PyObject* kwargs);


EXTERN PyObject * c_plot_pie(
	PyObject * args, 
	PyObject * kwargs);


EXTERN PyObject * c_plot_psychrometry(
	PyObject * args, 
	PyObject * kwargs);


EXTERN PyObject * c_plot_qqnorm(
	PyObject * args,
	PyObject * kwargs);


EXTERN PyObject * c_plot_qqplot(
	PyObject * args, 
	PyObject * kwargs);


EXTERN PyObject * c_plot_quiver(
	PyObject * args, 
	PyObject * kwargs);


EXTERN PyObject * c_plot_scatter(
	PyObject * args, 
	PyObject* kwargs);



/************************************************************************************/


EXTERN void c_plot_gdi_line(
	double x1,
	double y1,
	double x2,
	double y2,
	PyObject* PenObj);


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
	std::string text, 
	double angle, //positive angles are counterclockwise; the full angle is 360 degrees
	PyObject* FontObj,
	PyObject* ColorObj); 

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



/**********************************************************************************/
	
EXTERN void c_plot_app();
EXTERN bool c_plot_mainloop(bool sharedLoop = false);
EXTERN bool c_plot_ismainlooprunning();
EXTERN bool c_plot_exitmainloop();