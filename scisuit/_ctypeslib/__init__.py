import ctypes as _ct
from ..util import parent_path as _parent_path

#TODO: Change to release version
_path = _parent_path(__file__, level=1) / "scisuit_core_d"
core = _ct.PyDLL(str(_path))





"""       ENGINEERING               """

core.c_eng_psychrometry.argtypes = [_ct.py_object]
core.c_eng_psychrometry.restype = _ct.py_object




"""        ROOTS PACKAGE           """

core.c_root_bisect.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double, _ct.c_double, _ct.c_int, _ct.c_char_p, _ct.c_bool]
core.c_root_bisect.restype = _ct.py_object

core.c_root_brentq.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double, _ct.c_double, _ct.c_int]
core.c_root_brentq.restype = _ct.py_object

core.c_root_muller.argtypes = [_ct.py_object, _ct.py_object, _ct.py_object, _ct.py_object, _ct.py_object, _ct.c_double, _ct.c_int]
core.c_root_muller.restype = _ct.py_object

core.c_root_newton.argtypes = [_ct.py_object, _ct.c_double, _ct.py_object, _ct.py_object, _ct.c_double, _ct.c_int]
core.c_root_newton.restype = _ct.py_object

core.c_root_ridder.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double, _ct.c_double, _ct.c_int]
core.c_root_ridder.restype = _ct.py_object




"""                 FITTING PACKAGE"""

core.c_fit_expfit.argtypes = [_ct.py_object, _ct.py_object, _ct.py_object]
core.c_fit_expfit.restype = _ct.py_object
core.c_fit_lagrange.argtypes = [_ct.py_object, _ct.py_object,_ct.c_double]
core.c_fit_lagrange.restype = _ct.py_object
core.c_fit_logfit.argtypes = [_ct.py_object, _ct.py_object]
core.c_fit_logfit.restype = _ct.py_object
core.c_fit_logistfit.argtypes = [_ct.py_object, _ct.py_object, _ct.py_object]
core.c_fit_logistfit.restype = _ct.py_object
core.c_fit_powfit.argtypes = [_ct.py_object, _ct.py_object]
core.c_fit_powfit.restype = _ct.py_object
core.c_fit_spline.argtypes = [_ct.py_object, _ct.py_object]
core.c_fit_spline.restype = _ct.py_object



"""        STATS PACKAGE           """

core.c_stat_dbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
core.c_stat_dbinom.restype=_ct.py_object
core.c_stat_pbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
core.c_stat_pbinom.restype=_ct.py_object
core.c_stat_qbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
core.c_stat_qbinom.restype=_ct.py_object


core.c_stat_dnbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
core.c_stat_dnbinom.restype=_ct.py_object
core.c_stat_pnbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
core.c_stat_pnbinom.restype=_ct.py_object
core.c_stat_qnbinom.argtypes = [_ct.py_object, _ct.c_int, _ct.c_double]
core.c_stat_qnbinom.restype=_ct.py_object


core.c_stat_dchisq.argtypes = [_ct.py_object, _ct.c_int]
core.c_stat_dchisq.restype=_ct.py_object
core.c_stat_pchisq.argtypes = [_ct.py_object, _ct.c_int]
core.c_stat_pchisq.restype=_ct.py_object
core.c_stat_qchisq.argtypes = [_ct.py_object, _ct.c_int]
core.c_stat_qchisq.restype=_ct.py_object


core.c_stat_dexp.argtypes = [_ct.py_object, _ct.c_double]
core.c_stat_dexp.restype=_ct.py_object
core.c_stat_pexp.argtypes = [_ct.py_object, _ct.c_double]
core.c_stat_pexp.restype=_ct.py_object
core.c_stat_qexp.argtypes = [_ct.py_object, _ct.c_double]
core.c_stat_qexp.restype=_ct.py_object


core.c_stat_df.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int]
core.c_stat_df.restype=_ct.py_object
core.c_stat_pf.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int]
core.c_stat_pf.restype=_ct.py_object
core.c_stat_qf.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int]
core.c_stat_qf.restype=_ct.py_object


core.c_stat_dgeom.argtypes = [_ct.py_object, _ct.c_double]
core.c_stat_dgeom.restype=_ct.py_object
core.c_stat_pgeom.argtypes =  [_ct.py_object, _ct.c_double]
core.c_stat_pgeom.restype=_ct.py_object
core.c_stat_qgeom.argtypes =  [_ct.py_object, _ct.c_double]
core.c_stat_qgeom.restype=_ct.py_object

core.c_stat_dhyper.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int, _ct.c_int]
core.c_stat_dhyper.restype=_ct.py_object
core.c_stat_phyper.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int, _ct.c_int]
core.c_stat_phyper.restype=_ct.py_object
core.c_stat_qhyper.argtypes = [_ct.py_object, _ct.c_int, _ct.c_int, _ct.c_int]
core.c_stat_qhyper.restype=_ct.py_object


core.c_stat_dnorm.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
core.c_stat_dnorm.restype=_ct.py_object
core.c_stat_pnorm.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
core.c_stat_pnorm.restype=_ct.py_object
core.c_stat_qnorm.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
core.c_stat_qnorm.restype=_ct.py_object


core.c_stat_dpois.argtypes = [_ct.py_object, _ct.c_double]
core.c_stat_dpois.restype=_ct.py_object
core.c_stat_ppois.argtypes = [_ct.py_object, _ct.c_double]
core.c_stat_ppois.restype=_ct.py_object
core.c_stat_qpois.argtypes = [_ct.py_object, _ct.c_double]
core.c_stat_qpois.restype=_ct.py_object


core.c_stat_dt.argtypes = [_ct.py_object, _ct.c_int]
core.c_stat_dt.restype=_ct.py_object
core.c_stat_pt.argtypes = [_ct.py_object, _ct.c_int]
core.c_stat_pt.restype=_ct.py_object
core.c_stat_qt.argtypes = [_ct.py_object, _ct.c_int]
core.c_stat_qt.restype=_ct.py_object


core.c_stat_dunif.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
core.c_stat_dunif.restype=_ct.py_object
core.c_stat_punif.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
core.c_stat_punif.restype=_ct.py_object
core.c_stat_qunif.argtypes = [_ct.py_object, _ct.c_double, _ct.c_double]
core.c_stat_qunif.restype=_ct.py_object


core.c_stat_dsignrank.argtypes = [_ct.py_object, _ct.c_int]
core.c_stat_dsignrank.restype=_ct.py_object
core.c_stat_psignrank.argtypes = [_ct.py_object, _ct.c_int]
core.c_stat_psignrank.restype=_ct.py_object
core.c_stat_qsignrank.argtypes = [_ct.py_object, _ct.c_int]
core.c_stat_qsignrank.restype=_ct.py_object


core.c_stat_moveavg.argtypes = [_ct.py_object, _ct.py_object, _ct.c_int]
core.c_stat_moveavg.restype=_ct.py_object

core.c_stat_rolling.argtypes = [_ct.py_object, _ct.py_object, _ct.c_int]
core.c_stat_rolling.restype=_ct.py_object

core.c_stat_test_norm_ad.argtypes = [_ct.py_object]
core.c_stat_test_norm_ad.restype=_ct.py_object



__all__ = ['core']