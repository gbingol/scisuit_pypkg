#pragma once


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


//start a new plot window
EXTERN void c_plot_figure();

EXTERN void c_plot_show(bool maximize = false);

EXTERN void c_plot_title(PyObject* title);
EXTERN void c_plot_xlabel(PyObject* xlabel);
EXTERN void c_plot_ylabel(PyObject* ylabel);
EXTERN void c_plot_legend();

	
EXTERN void c_plot_app();
EXTERN bool c_plot_mainloop(bool sharedLoop = false);
EXTERN bool c_plot_ismainlooprunning();
EXTERN bool c_plot_exitmainloop();