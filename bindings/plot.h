#pragma once

#include <cstdint>

#include <Python.h>
#include "dllimpexp.h"

#define EXTERN \
	extern "C" DLLPYBIND



EXTERN 
PyObject* c_plot_boxplot(
	PyObject* args, 
	PyObject* kwargs);


EXTERN 
PyObject* c_plot_histogram(
	PyObject* args, 
	PyObject* kwargs);


EXTERN 
PyObject * c_plot_psychrometry(
	PyObject * args, 
	PyObject * kwargs);


EXTERN 
PyObject * c_plot_scatter(
	PyObject * args, 
	PyObject* kwargs);


//X and Y bounds
EXTERN 
PyObject * c_plot_canvas(
	PyObject * X, 
	PyObject* Y,
	bool ShowHAxis = true, 
	bool ShowVAxis = true,
	bool ShowHGrid = true,
	bool ShowVGrid = true,
	bool Rescale = false); 




/************************************************************************************/

EXTERN 
size_t c_plot_gdi_arrow(
	double x1,
	double y1,
	double x2,
	double y2,
	double angle,
	double length,
	const char* label,
	PyObject* PenObj);


EXTERN 
size_t c_plot_gdi_line(
	double x1,
	double y1,
	double x2,
	double y2,
	const char* label,
	PyObject* PenObj);


//xy: bottom-left
EXTERN 
size_t c_plot_gdi_rect(
	double x,
	double y,
	double width,
	double height,
	const char* label,
	PyObject* PenObj,
	PyObject* BrushObj);


EXTERN 
size_t c_plot_gdi_ellipse(
	double x,
	double y,
	double width,
	double height,
	const char* label,
	PyObject* PenObj,
	PyObject* BrushObj);


//(x,y) top-left
EXTERN 
size_t c_plot_gdi_text(
	double x,
	double y,
	const char* text, 
	double angle, //positive angles are counterclockwise; the full angle is 360 degrees
	char hanchor,
	char vanchor, 
	const char* color,
	PyObject* FontObj); 


// (x1,y1): start, (x2, y2):end, (xc, yc): center
EXTERN 
size_t c_plot_gdi_arc(
	double x1,
	double y1,
	double x2,
	double y2,
	double xc,
	double yc,
	const char* label,
	PyObject* PenObj,
	PyObject* BrushObj);


EXTERN 
size_t c_plot_gdi_curve(
	PyObject* XObj,
	PyObject* YObj,
	const char* label,
	PyObject* PenObj);


EXTERN 
size_t c_plot_gdi_polygon(
	PyObject* XObj,
	PyObject* YObj,
	const char* label,
	PyObject* PenObj,
	PyObject* BrushObj);


//(x,y) centroid
EXTERN 
size_t c_plot_gdi_marker(
	double x,
	double y,
	const char* Type, 
	std::uint8_t Size,
	const char* label,
	PyObject* PenObj,
	PyObject* BrushObj); 


EXTERN
void c_plot_gdi_makegroup(
	size_t ownerid,
	PyObject *members);






/************************************************************************************/

EXTERN
void c_plot_layout(int nrows, int ncols);


EXTERN 
void c_plot_subplot(
	int row,
	int col,
	int nrows = 1,
	int ncols = 1);




//start a new plot window
EXTERN 
void c_plot_figure();


EXTERN
void c_plot_savefig(const char *fullpath);


EXTERN
void c_plot_set_figsize(size_t width, size_t height);


EXTERN 
void c_plot_show(bool antialiasing);


EXTERN 
void c_plot_title(const char* title);


EXTERN 
void c_plot_xlabel(const char* xlabel);


EXTERN 
void c_plot_ylabel(const char* ylabel);


EXTERN 
void c_plot_legend(
	PyObject* nrows, 
	PyObject* ncols);


//Either returns the limits or sets the limits
EXTERN 
PyObject *c_plot_axislim(
			PyObject *min, 
			PyObject *max, 
			char SelAxis='y');


EXTERN 
PyObject* c_plot_set_xticks(
			PyObject* pos, 
			PyObject* labels,
			const char* Alignment = "center",
			const char* Position = "bottom");


EXTERN 
PyObject* c_plot_set_yticks(
			PyObject* pos, 
			PyObject* labels,
			const char* Alignment = "center",
			const char* Position = "left");


EXTERN 
PyObject* c_plot_set_axispos(
				double pos, 
				char SelAxis);


EXTERN 
PyObject* c_plot_axisscale(
				const char* scale, 
				char SelAxis);





/**********************************************************************************/
	
EXTERN 
void c_plot_app();

EXTERN 
bool c_plot_mainloop();

EXTERN 
bool c_plot_ismainlooprunning();

EXTERN 
bool c_plot_exitmainloop();