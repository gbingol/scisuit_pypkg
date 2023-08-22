import ctypes as _ct

from .._ctypeslib import coreDLL as _core
from dataclasses import dataclass as _dataclass    






#----------------------
def moveavg(x, y, period=2):
	return _core.c_stat_moveavg(x, y, _ct.c_int(period))

def rolling(x, y, period=2):
	return _core.c_stat_rolling(x, y, _ct.c_int(period))

#----------------------

@_dataclass
class TestNormRes:
	pval:float
	A2:float

def test_norm_ad(x):
	pval, A2 = _core.c_stat_test_norm_ad(x)
	return TestNormRes(pval, A2)





from .aov import aov
from .aov2 import aov2, aov2_results
from .core import kurt, mode, rolling, sample, skew
from .linregress import linregress

from .test_z import test_z, test_z_Result
from .test_f import test_f, test_f_Result
from .test_sign import test_sign, test_sign_Result
from .test_t import test_t, test_t1_result, test_t2_result, test_tpaired_result

from .distributions import \
	dbinom, pbinom, qbinom, rbinom, \
	dchisq, pchisq, qchisq, rchisq, \
	dexp, pexp, qexp, rexp, \
	df, pf, qf, rf, \
	dgamma, pgamma, qgamma,rgamma, \
	dgeom, pgeom, qgeom, rgeom, \
	dhyper, phyper, qhyper, rhyper, \
	dnbinom, pnbinom, qnbinom,rnbinom, \
	dnorm, pnorm, qnorm, rnorm, \
	dpois, ppois, qpois, rpois, \
	dsignrank, qsignrank, psignrank, \
	dt, pt, qt, rt, \
	dunif, punif, qunif, runif




