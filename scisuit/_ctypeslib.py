from ctypes import PyDLL, c_bool, c_char, c_char_p, c_double, c_int, py_object, c_uint8, c_uint32, c_longlong, c_ulonglong
import sys
from pathlib import Path as _Path

"""
Tested with: 3.10.6, 3.11.6, 3.12.0
"""
_DLLname = "scisuit_pybind" + str(sys.version_info.major) + str(sys.version_info.minor)


#__file__ is guaranteed to be an absolute path in Python 3.9+
__pt = _Path(__file__)
pydll = PyDLL(str(__pt.parents[0] / _DLLname))



__all__ = ['pydll']




"""
-------------------------------------------------------------------------------
------------------------  ENGINEERING --------------------------------------- 
"""

pydll.c_eng_psychrometry.argtypes = [py_object]
pydll.c_eng_psychrometry.restype = py_object




"""
-------------------------------------------------------------------------------
------------------------    ROOTS  --------------------------------------- 
"""

pydll.c_root_bisect.argtypes = [py_object, c_double, c_double, c_double, c_int, c_char_p, c_bool]
pydll.c_root_bisect.restype = py_object


pydll.c_root_itp.argtypes = [
					py_object, #f
					c_double, #a
					c_double, #b
					c_double, #k1
					c_double, #k2
					c_double, #TOL
					c_int] #maxiter
pydll.c_root_itp.restype = py_object


pydll.c_root_brentq.argtypes = [
					py_object, 
					c_double, 
					c_double, 
					c_double, 
					c_int]
pydll.c_root_brentq.restype = py_object


pydll.c_root_muller.argtypes = [
					py_object, 
					py_object, 
					py_object, 
					py_object, 
					py_object, 
					c_double, 
					c_int]
pydll.c_root_muller.restype = py_object


pydll.c_root_newton.argtypes = [
					py_object, #f
					c_double, #X0
					py_object, #X1
					py_object, #fprime
					py_object, #fprime2
					c_double, #tol
					c_int #maxiter
				]
pydll.c_root_newton.restype = py_object


pydll.c_root_ridder.argtypes = [
					py_object, 
					c_double, 
					c_double, 
					c_double, 
					c_int]
pydll.c_root_ridder.restype = py_object


pydll.c_root_toms748.argtypes = [
					py_object, 
					c_double, 
					c_double, 
					c_double, 
					c_int]
pydll.c_root_toms748.restype = py_object




"""
-------------------------------------------------------------------------------
------------------------  FITTING PACKAGE --------------------------------------- 
"""

pydll.c_fit_expfit.argtypes = [py_object, py_object, py_object]
pydll.c_fit_expfit.restype = py_object


pydll.c_fit_lagrange.argtypes = [py_object, py_object,c_double]
pydll.c_fit_lagrange.restype = py_object


pydll.c_fit_logfit.argtypes = [py_object, py_object]
pydll.c_fit_logfit.restype = py_object


pydll.c_fit_logistfit.argtypes = [py_object, py_object, py_object]
pydll.c_fit_logistfit.restype = py_object


pydll.c_fit_powfit.argtypes = [py_object, py_object]
pydll.c_fit_powfit.restype = py_object


pydll.c_fit_spline.argtypes = [py_object, py_object]
pydll.c_fit_spline.restype = py_object






"""
-------------------------------------------------------------------------------
------------------------  INTEGRATION --------------------------------------- 
"""
pydll.c_integ_simpson.argtypes = [py_object, py_object]
pydll.c_integ_simpson.restype = py_object

pydll.c_integ_romberg.argtypes = [py_object, c_double, c_double, c_double, c_int]
pydll.c_integ_romberg.restype = py_object

pydll.c_integ_fixed_quad.argtypes = [py_object, c_double, c_double, c_int]
pydll.c_integ_fixed_quad.restype = py_object



"""
-------------------------------------------------------------------------------
------------------------  OPTIMIZATION --------------------------------------- 
"""

pydll.c_optimize_bracket.argtypes = [
					py_object, #function
					c_double, #a
					c_double, #b
					c_double, #growlimit
					c_uint32] #maxiter
pydll.c_optimize_bracket.restype = py_object 


pydll.c_optimize_golden.argtypes = [
					py_object, #function
					c_double, #xlow
					c_double, #xhigh
					c_double, #tol
					c_uint32] #maxiter
pydll.c_optimize_golden.restype = py_object 


pydll.c_optimize_parabolic.argtypes = [
					py_object, #function
					c_double, #xa
					c_double, #xb
					py_object, #xc
					c_double, #tol
					c_uint32] #maxiter
pydll.c_optimize_parabolic.restype = py_object 


pydll.c_optimize_brent.argtypes = [
					py_object, #function
					c_double, #xlow
					c_double, #xhigh
					c_longlong] #maxiter
pydll.c_optimize_brent.restype = py_object 


"""
-------------------------------------------------------------------------------
------------------------  STATS --------------------------------------- 
"""

pydll.c_stat_dbeta.argtypes = [py_object,  c_double, c_double]
pydll.c_stat_dbeta.restype=py_object

pydll.c_stat_pbeta.argtypes = [py_object,  c_double, c_double]
pydll.c_stat_pbeta.restype=py_object

pydll.c_stat_qbeta.argtypes = [py_object,  c_double, c_double]
pydll.c_stat_qbeta.restype=py_object

#----

pydll.c_stat_dbinom.argtypes = [py_object, c_int, c_double]
pydll.c_stat_dbinom.restype=py_object

pydll.c_stat_pbinom.argtypes = [py_object, c_int, c_double]
pydll.c_stat_pbinom.restype=py_object

pydll.c_stat_qbinom.argtypes = [py_object, c_int, c_double]
pydll.c_stat_qbinom.restype=py_object

#----

pydll.c_stat_dnbinom.argtypes = [py_object, c_int, c_double]
pydll.c_stat_dnbinom.restype=py_object

pydll.c_stat_pnbinom.argtypes = [py_object, c_int, c_double]
pydll.c_stat_pnbinom.restype=py_object

pydll.c_stat_qnbinom.argtypes = [py_object, c_int, c_double]
pydll.c_stat_qnbinom.restype=py_object

#----

pydll.c_stat_dmultinom.argtypes = [py_object, c_int, py_object]
pydll.c_stat_dmultinom.restype=py_object

#----

pydll.c_stat_dchisq.argtypes = [py_object, c_int]
pydll.c_stat_dchisq.restype=py_object

pydll.c_stat_pchisq.argtypes = [py_object, c_int]
pydll.c_stat_pchisq.restype=py_object

pydll.c_stat_qchisq.argtypes = [py_object, c_int]
pydll.c_stat_qchisq.restype=py_object

#----

pydll.c_stat_dexp.argtypes = [py_object, c_double]
pydll.c_stat_dexp.restype=py_object

pydll.c_stat_pexp.argtypes = [py_object, c_double]
pydll.c_stat_pexp.restype=py_object

pydll.c_stat_qexp.argtypes = [py_object, c_double]
pydll.c_stat_qexp.restype=py_object

#----

pydll.c_stat_df.argtypes = [py_object, c_int, c_int]
pydll.c_stat_df.restype=py_object

pydll.c_stat_pf.argtypes = [py_object, c_int, c_int]
pydll.c_stat_pf.restype=py_object

pydll.c_stat_qf.argtypes = [py_object, c_int, c_int]
pydll.c_stat_qf.restype=py_object

#----

pydll.c_stat_dgamma.argtypes = [py_object, c_double, c_double]
pydll.c_stat_dgamma.restype=py_object

pydll.c_stat_pgamma.argtypes = [py_object, c_double, c_double]
pydll.c_stat_pgamma.restype=py_object

pydll.c_stat_qgamma.argtypes = [py_object, c_double, c_double]
pydll.c_stat_qgamma.restype=py_object

#----

pydll.c_stat_dgeom.argtypes = [py_object, c_double]
pydll.c_stat_dgeom.restype=py_object

pydll.c_stat_pgeom.argtypes =  [py_object, c_double]
pydll.c_stat_pgeom.restype=py_object

pydll.c_stat_qgeom.argtypes =  [py_object, c_double]
pydll.c_stat_qgeom.restype=py_object

#----

pydll.c_stat_dhyper.argtypes = [py_object, c_int, c_int, c_int]
pydll.c_stat_dhyper.restype=py_object

pydll.c_stat_phyper.argtypes = [py_object, c_int, c_int, c_int]
pydll.c_stat_phyper.restype=py_object

pydll.c_stat_qhyper.argtypes = [py_object, c_int, c_int, c_int]
pydll.c_stat_qhyper.restype=py_object

#----

pydll.c_stat_dnorm.argtypes = [py_object, c_double, c_double]
pydll.c_stat_dnorm.restype=py_object

pydll.c_stat_pnorm.argtypes = [py_object, c_double, c_double]
pydll.c_stat_pnorm.restype=py_object

pydll.c_stat_qnorm.argtypes = [py_object, c_double, c_double]
pydll.c_stat_qnorm.restype=py_object

#----

pydll.c_stat_dlnorm.argtypes = [py_object, c_double, c_double]
pydll.c_stat_dlnorm.restype=py_object

pydll.c_stat_plnorm.argtypes = [py_object, c_double, c_double]
pydll.c_stat_plnorm.restype=py_object

pydll.c_stat_qlnorm.argtypes = [py_object, c_double, c_double]
pydll.c_stat_qlnorm.restype=py_object

#----

pydll.c_stat_dpareto.argtypes = [py_object, c_double, c_double]
pydll.c_stat_dpareto.restype=py_object

pydll.c_stat_ppareto.argtypes = [py_object, c_double, c_double]
pydll.c_stat_ppareto.restype=py_object

pydll.c_stat_qpareto.argtypes = [py_object, c_double, c_double]
pydll.c_stat_qpareto.restype=py_object

#----

pydll.c_stat_dpois.argtypes = [py_object, c_double]
pydll.c_stat_dpois.restype=py_object

pydll.c_stat_ppois.argtypes = [py_object, c_double]
pydll.c_stat_ppois.restype=py_object

pydll.c_stat_qpois.argtypes = [py_object, c_double]
pydll.c_stat_qpois.restype=py_object


#---

pydll.c_stat_psmirnov.argtypes = [py_object, c_int]
pydll.c_stat_psmirnov.restype=py_object


#----

pydll.c_stat_dt.argtypes = [py_object, c_int]
pydll.c_stat_dt.restype=py_object

pydll.c_stat_pt.argtypes = [py_object, c_int]
pydll.c_stat_pt.restype=py_object

pydll.c_stat_qt.argtypes = [py_object, c_int]
pydll.c_stat_qt.restype=py_object

#----

pydll.c_stat_dunif.argtypes = [py_object, c_double, c_double]
pydll.c_stat_dunif.restype=py_object

pydll.c_stat_punif.argtypes = [py_object, c_double, c_double]
pydll.c_stat_punif.restype=py_object

pydll.c_stat_qunif.argtypes = [py_object, c_double, c_double]
pydll.c_stat_qunif.restype=py_object

#----

pydll.c_stat_dweibull.argtypes = [py_object, c_double, c_double]
pydll.c_stat_dweibull.restype=py_object

pydll.c_stat_pweibull.argtypes = [py_object, c_double, c_double]
pydll.c_stat_pweibull.restype=py_object

pydll.c_stat_qweibull.argtypes = [py_object, c_double, c_double]
pydll.c_stat_qweibull.restype=py_object

#----

pydll.c_stat_dsignrank.argtypes = [py_object, c_int]
pydll.c_stat_dsignrank.restype=py_object

pydll.c_stat_psignrank.argtypes = [py_object, c_int]
pydll.c_stat_psignrank.restype=py_object

pydll.c_stat_qsignrank.argtypes = [py_object, c_int]
pydll.c_stat_qsignrank.restype=py_object

#----


pydll.c_stat_rolling.argtypes = [py_object, py_object, c_int]
pydll.c_stat_rolling.restype=py_object

pydll.c_stat_test_norm_ad.argtypes = [py_object]
pydll.c_stat_test_norm_ad.restype=py_object


pydll.c_stat_test_shapirowilkinson.argtypes = [py_object]
pydll.c_stat_test_shapirowilkinson.restype=py_object




"""
--------------------------------------------------------------------------------
----------------------------  PLOT LIBRARY --------------------------------------
"""


pydll.c_plot_boxplot.argtypes = [py_object, py_object]
pydll.c_plot_boxplot.restype=py_object


pydll.c_plot_histogram.argtypes = [py_object, py_object]
pydll.c_plot_histogram.restype=py_object


pydll.c_plot_psychrometry.argtypes = [py_object, py_object]
pydll.c_plot_psychrometry.restype=py_object


pydll.c_plot_scatter.argtypes = [py_object, py_object]
pydll.c_plot_scatter.restype=py_object


pydll.c_plot_canvas.argtypes = [
						py_object, #x-bounds
						py_object, #y-bounds
						c_bool, # Show Horiz Axis
						c_bool, # Show Vert Axis
						c_bool, # Show Horiz Gridlines
						c_bool, # Show Vert Gridlines
						c_bool] # Allow Rescale
pydll.c_plot_canvas.restype=py_object



#-----------------------------------------
pydll.c_plot_gdi_arc.argtypes = [
					c_double, #x1
					c_double, #y1
					c_double, #x2
					c_double, #y2
					c_double, #xcenter
					c_double, #ycenter
					py_object, #dictionary for Pen
					py_object] #dictionary for Brush				
pydll.c_plot_gdi_arc.restype=c_ulonglong


pydll.c_plot_gdi_arrow.argtypes = [
					c_double, #x1
					c_double, #y1
					c_double, #x2
					c_double, #y2
					c_double, #angle
					c_double, #length
					c_char_p, # label
					py_object] #dictionary for Pen				
pydll.c_plot_gdi_arrow.restype=c_ulonglong


pydll.c_plot_gdi_line.argtypes = [
					c_double, #x1
					c_double, #y1
					c_double, #x2
					c_double, #y2
					c_char_p, # label
					py_object] #dictionary for Pen				
pydll.c_plot_gdi_line.restype=c_ulonglong


pydll.c_plot_gdi_rect.argtypes = [
					c_double, #x of top-left
					c_double, #y of top-left
					c_double, #width
					c_double, #height
					c_char_p, # label
					py_object, #dictionary for Pen
					py_object] #dictionary for Brush
pydll.c_plot_gdi_ellipse.restype=c_ulonglong


pydll.c_plot_gdi_ellipse.argtypes = [
					c_double, # x of center
					c_double, # y of center
					c_double, # half width
					c_double, # half height
					c_char_p, # label
					py_object, #dictionary for Pen
					py_object] #dictionary for Brush
pydll.c_plot_gdi_ellipse.restype=c_ulonglong


pydll.c_plot_gdi_text.argtypes = [
					c_double, # x of top-left
					c_double, # y of top-left
					c_char_p, # text
					c_double, # rotation
					c_char, #halign
					c_char, #valign
					c_char_p, # color
					py_object] #dictionary for Font
pydll.c_plot_gdi_text.restype=c_ulonglong


pydll.c_plot_gdi_curve.argtypes = [
					py_object, #x-values (iterable)
					py_object,#y-values (iterable)
					c_char_p, # label
					py_object] #dictionary for Pen
pydll.c_plot_gdi_curve.restype=c_ulonglong


pydll.c_plot_gdi_polygon.argtypes = [
					py_object, #x-values (iterable)
					py_object,#y-values (iterable)
					c_char_p, # label
					py_object, #dictionary for Pen
					py_object] #dictionary for brush
pydll.c_plot_gdi_polygon.restype=c_ulonglong


pydll.c_plot_gdi_marker.argtypes = [
					c_double, # x of centroid
					c_double, # y of centroid
					c_char_p, # type
					c_uint8, # size
					c_char_p, # label
					py_object, # dictionary for Pen
					py_object] #dictionary for Brush
pydll.c_plot_gdi_marker.restype=c_ulonglong


pydll.c_plot_gdi_makegroup.argtypes = [
					c_ulonglong, #owner id
					py_object] #member ids
pydll.c_plot_gdi_makegroup.restype=None


#---------------------------------------------

pydll.c_plot_layout.argtypes = [c_int, c_int]
pydll.c_plot_layout.restype=None


pydll.c_plot_subplot.argtypes = [
						c_int, 
						c_int, 
						c_int, 
						c_int]
pydll.c_plot_subplot.restype=None


pydll.c_plot_figure.argtypes = []
pydll.c_plot_figure.restype=None

pydll.c_plot_savefig.argtypes = [c_char_p]
pydll.c_plot_savefig.restype=None


pydll.c_plot_title.argtypes = [c_char_p]
pydll.c_plot_title.restype=None


pydll.c_plot_xlabel.argtypes = [c_char_p]
pydll.c_plot_xlabel.restype=None


pydll.c_plot_ylabel.argtypes = [c_char_p]
pydll.c_plot_ylabel.restype=None


pydll.c_plot_axislim.argtypes = [
						py_object, 
						py_object, 
						c_char]
pydll.c_plot_axislim.restype=py_object


pydll.c_plot_set_xticks.argtypes = [
						py_object, 
						py_object,
						c_char_p, #Alignment
						c_char_p] #Position
pydll.c_plot_set_xticks.restype=py_object


pydll.c_plot_set_yticks.argtypes = [
						py_object, 
						py_object,
						c_char_p, #Alignment
						c_char_p] #Position
pydll.c_plot_set_yticks.restype=py_object

#param2: x, y
pydll.c_plot_set_axispos.argtypes = [c_double, c_char]
pydll.c_plot_set_axispos.restype=py_object

#param1: linear, log | param2: x, y
pydll.c_plot_axisscale.argtypes = [c_char_p, c_char]
pydll.c_plot_axisscale.restype=py_object


pydll.c_plot_legend.argtypes = [py_object, py_object]
pydll.c_plot_legend.restype=None


pydll.c_plot_show.argtypes = [
							c_bool] #antialiasing
pydll.c_plot_show.restype=None


