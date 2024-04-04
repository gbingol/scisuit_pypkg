import ctypes as _ct

from dataclasses import dataclass as _dataclass





from .core import kurt, mode, moveavg, rolling, sample, skew

from .aov import aov, aov2, aov2_results
from .linregress import linregress

from .test_basic import \
	anderson, ADTestRes, \
	ks_1samp, Ks1SampletestResult, \
	test_f, test_f_Result, \
	test_sign, test_sign_Result,\
	test_t, test_t1_result, test_t2_result, test_tpaired_result, \
	test_z, test_z_Result


from .distributions import \
	dbeta, pbeta, qbeta, rbeta, \
	dbinom, pbinom, qbinom, rbinom, \
	dchisq, pchisq, qchisq, rchisq, \
	dexp, pexp, qexp, rexp, \
	df, pf, qf, rf, \
	dgamma, pgamma, qgamma,rgamma, \
	dgeom, pgeom, qgeom, rgeom, \
	dhyper, phyper, qhyper, rhyper, \
	dmultinom, rmultinom, \
	dnbinom, pnbinom, qnbinom,rnbinom, \
	dnorm, pnorm, qnorm, rnorm, \
	dlnorm, plnorm, qlnorm, rlnorm, \
	dpareto, ppareto, qpareto, rpareto, \
	dpois, ppois, qpois, rpois, \
	dsignrank, qsignrank, psignrank, \
	psmirnov, \
	dt, pt, qt, rt, \
	dunif, punif, qunif, runif, \
	dweibull, pweibull, qweibull, rweibull




