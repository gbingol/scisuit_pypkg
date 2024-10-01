from ._core import kurt, mode, moveavg, rolling, skew

from ._aov import aov, aov_results, aov2, aov2_results
from ._linregress import linregress, linregressResult

from ._test_basic import test_f, test_f_Result, test_sign, test_sign_Result

from ._test_t import test_t, test_t1_result, test_t2_result, test_tpaired_result
from ._test_z import test_z, test_z_Result


from ._test_normality import \
	anderson, ADTestRes, \
	ks_1samp, Ks1SampletestResult, \
	shapiro, ShapiroTestResult


from ._distributions import \
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




