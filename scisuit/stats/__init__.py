from ._core import kurt, mode, moveavg, rolling, skew

from .anova import aov, aov_results, tukey, TukeyResults, TukeyComparison 
from .anova import aov2, aov2_results

from .regression import linregress

from .basictests import test_f, test_f_Result
from .basictests import test_t, test_t1_result, test_t2_result, test_tpaired_result
from .basictests import test_z, test_z1_Result, test_z2_Result
from .basictests import anderson, ADTestRes, ks_1samp, Ks1SampletestResult, shapiro, ShapiroTestResult
from .basictests import cor_test

from .nonparametric import test_sign, test_sign_Result
from .nonparametric import test_wilcox, test_wilcox_Result

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




