import sys
import ctypes as _ct
from .util import parent_path as _parent_path

"""
Tested with: 3.10.6, 3.11.6, 3.12.0
"""
_DLLname = "scisuit_pybind" + str(sys.version_info.major) + str(sys.version_info.minor)

#TODO: Change to debug version
_path = _parent_path(__file__) / _DLLname
pydll = _ct.PyDLL(str(_path))




"""       ENGINEERING               """

pydll.c_eng_psychrometry.argtypes = [_ct.py_object]
pydll.c_eng_psychrometry.restype = _ct.py_object




"""        ROOTS PACKAGE           """

pydll.c_root_bisect.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double, _ct.c_double, _ct.c_int, _ct.c_char_p, _ct.c_bool]
pydll.c_root_bisect.restype = _ct.py_object

pydll.c_root_brentq.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double, _ct.c_double, _ct.c_int]
pydll.c_root_brentq.restype = _ct.py_object

pydll.c_root_muller.argtypes = [_ct.py_object, _ct.py_object, _ct.py_object, _ct.py_object, _ct.py_object, _ct.c_double, _ct.c_int]
pydll.c_root_muller.restype = _ct.py_object

pydll.c_root_newton.argtypes = [_ct.py_object, _ct.c_double, _ct.py_object, _ct.py_object, _ct.c_double, _ct.c_int]
pydll.c_root_newton.restype = _ct.py_object

pydll.c_root_ridder.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double, _ct.c_double, _ct.c_int]
pydll.c_root_ridder.restype = _ct.py_object




"""                 FITTING PACKAGE"""

pydll.c_fit_expfit.argtypes = [_ct.py_object, _ct.py_object, _ct.py_object]
pydll.c_fit_expfit.restype = _ct.py_object
pydll.c_fit_lagrange.argtypes = [_ct.py_object, _ct.py_object,_ct.c_double]
pydll.c_fit_lagrange.restype = _ct.py_object
pydll.c_fit_logfit.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_fit_logfit.restype = _ct.py_object
pydll.c_fit_logistfit.argtypes = [_ct.py_object, _ct.py_object, _ct.py_object]
pydll.c_fit_logistfit.restype = _ct.py_object
pydll.c_fit_powfit.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_fit_powfit.restype = _ct.py_object
pydll.c_fit_spline.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_fit_spline.restype = _ct.py_object


"""      INTEG PACKAGE        """
pydll.c_integ_simpson.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_integ_simpson.restype = _ct.py_object

pydll.c_integ_romberg.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double, _ct.c_double, _ct.c_int]
pydll.c_integ_romberg.restype = _ct.py_object

pydll.c_integ_fixed_quad.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double, _ct.c_int]
pydll.c_integ_fixed_quad.restype = _ct.py_object


"""        STATS PACKAGE           """

pydll.c_stat_dbeta.argtypes = [_ct.py_object,  _ct.c_double, _ct.c_double]
pydll.c_stat_dbeta.restype=_ct.py_object
pydll.c_stat_pbeta.argtypes = [_ct.py_object,  _ct.c_double, _ct.c_double]
pydll.c_stat_pbeta.restype=_ct.py_object
pydll.c_stat_qbeta.argtypes = [_ct.py_object,  _ct.c_double, _ct.c_double]
pydll.c_stat_qbeta.restype=_ct.py_object


pydll.c_stat_dbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
pydll.c_stat_dbinom.restype=_ct.py_object
pydll.c_stat_pbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
pydll.c_stat_pbinom.restype=_ct.py_object
pydll.c_stat_qbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
pydll.c_stat_qbinom.restype=_ct.py_object


pydll.c_stat_dnbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
pydll.c_stat_dnbinom.restype=_ct.py_object
pydll.c_stat_pnbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
pydll.c_stat_pnbinom.restype=_ct.py_object
pydll.c_stat_qnbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
pydll.c_stat_qnbinom.restype=_ct.py_object


pydll.c_stat_dmultinom.argtypes = [_ct.py_object, _ct.c_int, _ct.py_object]
pydll.c_stat_dmultinom.restype=_ct.py_object


pydll.c_stat_dchisq.argtypes = [_ct.py_object, _ct.c_int]
pydll.c_stat_dchisq.restype=_ct.py_object
pydll.c_stat_pchisq.argtypes = [_ct.py_object, _ct.c_int]
pydll.c_stat_pchisq.restype=_ct.py_object
pydll.c_stat_qchisq.argtypes = [_ct.py_object, _ct.c_int]
pydll.c_stat_qchisq.restype=_ct.py_object


pydll.c_stat_dexp.argtypes = [_ct.py_object, _ct.c_double]
pydll.c_stat_dexp.restype=_ct.py_object
pydll.c_stat_pexp.argtypes = [_ct.py_object, _ct.c_double]
pydll.c_stat_pexp.restype=_ct.py_object
pydll.c_stat_qexp.argtypes = [_ct.py_object, _ct.c_double]
pydll.c_stat_qexp.restype=_ct.py_object


pydll.c_stat_df.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int]
pydll.c_stat_df.restype=_ct.py_object
pydll.c_stat_pf.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int]
pydll.c_stat_pf.restype=_ct.py_object
pydll.c_stat_qf.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int]
pydll.c_stat_qf.restype=_ct.py_object


pydll.c_stat_dgamma.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_dgamma.restype=_ct.py_object
pydll.c_stat_pgamma.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_pgamma.restype=_ct.py_object
pydll.c_stat_qgamma.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_qgamma.restype=_ct.py_object


pydll.c_stat_dgeom.argtypes = [_ct.py_object, _ct.c_double]
pydll.c_stat_dgeom.restype=_ct.py_object
pydll.c_stat_pgeom.argtypes =  [_ct.py_object, _ct.c_double]
pydll.c_stat_pgeom.restype=_ct.py_object
pydll.c_stat_qgeom.argtypes =  [_ct.py_object, _ct.c_double]
pydll.c_stat_qgeom.restype=_ct.py_object


pydll.c_stat_dhyper.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int, _ct.c_int]
pydll.c_stat_dhyper.restype=_ct.py_object
pydll.c_stat_phyper.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int, _ct.c_int]
pydll.c_stat_phyper.restype=_ct.py_object
pydll.c_stat_qhyper.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int, _ct.c_int]
pydll.c_stat_qhyper.restype=_ct.py_object


pydll.c_stat_dnorm.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_dnorm.restype=_ct.py_object
pydll.c_stat_pnorm.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_pnorm.restype=_ct.py_object
pydll.c_stat_qnorm.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_qnorm.restype=_ct.py_object


pydll.c_stat_dlnorm.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_dlnorm.restype=_ct.py_object
pydll.c_stat_plnorm.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_plnorm.restype=_ct.py_object
pydll.c_stat_qlnorm.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_qlnorm.restype=_ct.py_object


pydll.c_stat_dpareto.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_dpareto.restype=_ct.py_object
pydll.c_stat_ppareto.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_ppareto.restype=_ct.py_object
pydll.c_stat_qpareto.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_qpareto.restype=_ct.py_object


pydll.c_stat_dpois.argtypes = [_ct.py_object, _ct.c_double]
pydll.c_stat_dpois.restype=_ct.py_object
pydll.c_stat_ppois.argtypes = [_ct.py_object, _ct.c_double]
pydll.c_stat_ppois.restype=_ct.py_object
pydll.c_stat_qpois.argtypes = [_ct.py_object, _ct.c_double]
pydll.c_stat_qpois.restype=_ct.py_object


pydll.c_stat_dt.argtypes = [_ct.py_object, _ct.c_int]
pydll.c_stat_dt.restype=_ct.py_object
pydll.c_stat_pt.argtypes = [_ct.py_object, _ct.c_int]
pydll.c_stat_pt.restype=_ct.py_object
pydll.c_stat_qt.argtypes = [_ct.py_object, _ct.c_int]
pydll.c_stat_qt.restype=_ct.py_object


pydll.c_stat_dunif.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_dunif.restype=_ct.py_object
pydll.c_stat_punif.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_punif.restype=_ct.py_object
pydll.c_stat_qunif.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_qunif.restype=_ct.py_object


pydll.c_stat_dweibull.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_dweibull.restype=_ct.py_object
pydll.c_stat_pweibull.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_pweibull.restype=_ct.py_object
pydll.c_stat_qweibull.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
pydll.c_stat_qweibull.restype=_ct.py_object


pydll.c_stat_dsignrank.argtypes = [_ct.py_object, _ct.c_int]
pydll.c_stat_dsignrank.restype=_ct.py_object
pydll.c_stat_psignrank.argtypes = [_ct.py_object, _ct.c_int]
pydll.c_stat_psignrank.restype=_ct.py_object
pydll.c_stat_qsignrank.argtypes = [_ct.py_object, _ct.c_int]
pydll.c_stat_qsignrank.restype=_ct.py_object


pydll.c_stat_moveavg.argtypes = [_ct.py_object, _ct.py_object, _ct.c_int]
pydll.c_stat_moveavg.restype=_ct.py_object

pydll.c_stat_rolling.argtypes = [_ct.py_object, _ct.py_object, _ct.c_int]
pydll.c_stat_rolling.restype=_ct.py_object

pydll.c_stat_test_norm_ad.argtypes = [_ct.py_object]
pydll.c_stat_test_norm_ad.restype=_ct.py_object


""" -----------  PLOT LIBRARY ----------------------"""

pydll.c_plot_bar.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_bar.restype=_ct.py_object

pydll.c_plot_barh.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_barh.restype=_ct.py_object

pydll.c_plot_boxplot.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_boxplot.restype=_ct.py_object

pydll.c_plot_histogram.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_histogram.restype=_ct.py_object

pydll.c_plot_line.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_line.restype=_ct.py_object

pydll.c_plot_pie.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_pie.restype=_ct.py_object

pydll.c_plot_psychrometry.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_psychrometry.restype=_ct.py_object

pydll.c_plot_qqnorm.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_qqnorm.restype=_ct.py_object

pydll.c_plot_qqplot.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_qqplot.restype=_ct.py_object

pydll.c_plot_quiver.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_quiver.restype=_ct.py_object

pydll.c_plot_scatter.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_scatter.restype=_ct.py_object

pydll.c_plot_bubble.argtypes = [_ct.py_object, _ct.py_object]
pydll.c_plot_bubble.restype=_ct.py_object

pydll.c_plot_figure.argtypes = []
pydll.c_plot_figure.restype=None

pydll.c_plot_title.argtypes = [_ct.py_object]
pydll.c_plot_title.restype=None

pydll.c_plot_xlabel.argtypes = [_ct.py_object]
pydll.c_plot_xlabel.restype=None

pydll.c_plot_ylabel.argtypes = [_ct.py_object]
pydll.c_plot_ylabel.restype=None

pydll.c_plot_legend.argtypes = []
pydll.c_plot_legend.restype=None

pydll.c_plot_show.argtypes = [_ct.c_bool, _ct.c_bool]
pydll.c_plot_show.restype=None


__all__ = ['pydll']