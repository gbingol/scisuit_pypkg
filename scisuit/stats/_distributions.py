from ctypes import c_double, c_int, py_object
from numbers import Real
from typing import Iterable

import numpy as _np

from .._ctypeslib import pydll as _pydll



# ----- Standard Beta Distribution  -------

def dbeta(x:Iterable|Real, shape1:Real, shape2:Real)->list|Real:
	"""
	shape1, shape2: similar to alpha and beta
	"""
	assert shape1>0, "shape1>0 expected"
	assert shape2>0, "shape2>0 expected"
	return _pydll.c_stat_dbeta(py_object(x), c_double(shape1), c_double(shape2))


def pbeta(q:Iterable|Real, shape1:Real, shape2:Real)->list|Real:
	"""
	shape1, shape2: similar to alpha and beta
	"""
	assert shape1>0, "shape1>0 expected"
	assert shape2>0, "shape2>0 expected"

	return _pydll.c_stat_pbeta(py_object(q), c_double(shape1), c_double(shape2))


def qbeta(p:Iterable|Real, shape1:Real, shape2:Real)->list|Real:
	"""
	shape1, shape2: similar to alpha and beta
	"""
	assert shape1>0, "shape1>0 expected"
	assert shape2>0, "shape2>0 expected"

	return _pydll.c_stat_qbeta(py_object(p), c_double(shape1), c_double(shape2))
	

def rbeta(n:int, shape1:Real, shape2:Real)->list:
	"""
	shape1, shape2: similar to alpha and beta
	"""
	assert n>0 ,"n>0 expected"
	assert shape1>0, "shape1>0 expected"
	assert shape2>0, "shape2>0 expected"

	return _np.random.beta(size=n, a=shape1, b=shape2).tolist()



# ----- Binomial Distribution  -------

def dbinom(x:Iterable|Real, size:int, prob:Real)->list|Real:
	"""
	size: number of trials
	prob: probability of success in each trial
	"""
	return _pydll.c_stat_dbinom(py_object(x), c_int(size), c_double(prob))


def pbinom(q:Iterable|Real, size:int, prob:Real)->list|Real:
	"""
	size: number of trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _pydll.c_stat_pbinom(py_object(q), c_int(size), c_double(prob))


def qbinom(p:Iterable|Real, size:int, prob:Real)->list|Real:
	"""
	size: number of trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _pydll.c_stat_qbinom(py_object(p), c_int(size), c_double(prob))
	

def rbinom(n:int, size:int, prob:Real)->list:
	"""
	size: number of trials
	prob: probability of success in each trial
	"""
	assert n>0 ,"n>0 expected"
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _np.random.binomial(size=n, n=size, p=prob).tolist()




# ----- Negative-Binomial Distribution  -------

def dnbinom(x:Iterable|Real, size:int, prob:Real)->list|Real:
	"""
	x: quantiles representing number of failures
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _pydll.c_stat_dnbinom(py_object(x), c_int(size), c_double(prob))


def pnbinom(q:Iterable|Real, size:int, prob:Real)->list|Real:
	"""
	q: quantiles representing number of failures
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _pydll.c_stat_pnbinom(py_object(q), c_int(size), c_double(prob))


def qnbinom(p:Iterable|Real, size:int, prob:Real)->list|Real:
	"""
	p: probabilities
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _pydll.c_stat_qnbinom(py_object(p), c_int(size), c_double(prob))


def rnbinom(n:int, size:int, prob:Real)->list:
	"""
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	assert n>0 ,"n>0 expected"
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _np.random.negative_binomial(size=n, n=size, p=prob).tolist()



# ----- Multinomial Distribution  -------

def dmultinom(x:Iterable, size:int, prob:Iterable)->Real:
	"""
	x: quantiles 
	size: number of trials
	prob: probabilities of success in each trial

	## Note:
	Internally sum of probabilities is normalized to 1.0
	"""

	assert sum(x) == size, "sum(x) == size expected."
	assert size>0, "size>0 expected"

	return _pydll.c_stat_dmultinom(py_object(x), c_int(size), prob)


def rmultinom(n:int, size:int, prob:Iterable)->list:
	"""
	size: number of trials
	prob: probabilities of success in each trial

	returns 2D list, where list[i] corresponds to prob[i]

	## Note:
	Sum of probabilities is normalized to 1.0
	"""
	assert size>0, "size>0 expected"
	assert len(prob)>1, "For single prob value use rbinom function"

	Sum = sum(prob) 
	assert Sum>0, "sum of probabilities must be >0"

	return [rbinom(n, size, p/Sum) for p in prob]




# ----- Chi-Square Distribution  -------

def dchisq(x:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"
	return _pydll.c_stat_dchisq(py_object(x), c_int(df))


def pchisq(q:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"	
	return _pydll.c_stat_pchisq(py_object(q), c_int(df))


def qchisq(p:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"
	return _pydll.c_stat_qchisq(py_object(p), c_int(df))


def rchisq(n:int, df)->list:
	"""
	df: degrees of freedom
	"""
	assert n>0 ,"n>0 expected"
	assert df>0, "df>0 expected"

	return _np.random.chisquare(size=n, df = df).tolist()



# ----- Exponential Distribution  -------

def dexp(x:Iterable|Real, rate = 1.0)->list|Real:
	"""
	x: quantiles
	rate: 1/mean, where mean is the waiting time for the next event recurrence
	"""
	return _pydll.c_stat_dexp(py_object(x), c_double(rate))


def pexp(q:Iterable|Real, rate = 1.0)->list|Real:
	"""
	q: quantiles
	rate: 1/mean, where mean is the waiting time for the next event recurrence
	"""
	return _pydll.c_stat_pexp(py_object(q),  c_double(rate))


def qexp(p:Iterable|Real, rate = 1.0)->list|Real:
	"""
	p: probabilities
	rate: 1/mean, where mean is the waiting time for the next event recurrence
	"""
	return _pydll.c_stat_qexp(py_object(p), c_double(rate))


def rexp(n:int, rate=1.0)->list:
	"""
	rate: 1/mean, where mean is the waiting time for the next event recurrence
	"""
	assert n>0 ,"n>0 expected"
	assert rate>0, "rate>0 expected"

	return _np.random.exponential(size=n, scale=1/rate).tolist()



# ----- F Distribution  -------

def df(x:Iterable|Real, df1:int, df2:int)->list|Real:
	"""
	df1: degrees of freedom, numerator
	df2: degrees of freedom, denominator
	"""
	assert df1>0, "df1>0 expected"
	assert df2>0, "df2>0 expected"

	return _pydll.c_stat_df(py_object(x), c_int(df1), c_int(df2))


def pf(q:Iterable|Real, df1:int, df2:int)->list|Real:
	"""
	df1: degrees of freedom, numerator
	df2: degrees of freedom, denominator
	"""
	assert df1>0, "df1>0 expected"
	assert df2>0, "df2>0 expected"

	return _pydll.c_stat_pf(py_object(q), c_int(df1), c_int(df2))

def qf(p:Iterable|Real, df1:int, df2:int)->list|Real:
	"""
	df1: degrees of freedom, numerator
	df2: degrees of freedom, denominator
	"""
	assert df1>0, "df1>0 expected"
	assert df2>0, "df2>0 expected"

	return _pydll.c_stat_qf(py_object(p), c_int(df1), c_int(df2))


def rf(n:int, df1, df2)->list:
	"""
	df1: degrees of freedom, numerator
	df2: degrees of freedom, denominator
	"""
	assert n>0 ,"n>0 expected"
	assert df1>0, "df1>0 expected"
	assert df2>0, "df2>0 expected"

	return _np.random.f(size=n, dfnum=df1, dfden=df2).tolist()




# ----- Gamma Distribution  -------

def dgamma(x:Iterable|Real, shape:Real, scale = 1.0)->list|Real:
	"""
	x: quantile	
	shape: waiting time for the rth event to occur
	scale: average waiting time for the next event recurrence
	"""
	return _pydll.c_stat_dgamma(py_object(x), c_double(shape), c_double(scale))


def pgamma(q:Iterable|Real, shape:Real, scale = 1.0)->list|Real:
	"""
	q: quantile
	shape: waiting time for the rth event to occur
	scale: average waiting time for the next event recurrence
	"""
	return _pydll.c_stat_pgamma(py_object(q), c_double(shape), c_double(scale))


def qgamma(p:Iterable|Real, shape:Real, scale = 1.0)->list|Real:
	"""
	p: probabilities
	shape: waiting time for the rth event to occur
	scale: average waiting time for the next event recurrence
	"""
	return _pydll.c_stat_qgamma(py_object(p), c_double(shape), c_double(scale))


def rgamma(n:int, shape:Real, scale=1.0)->list:
	"""
	Draw samples from gamma distribution
	"""
	assert n>0 ,"n>0 expected"
	assert shape>0, "shape>0 expected"
	assert scale>0, "scale>0 expected"

	return _np.random.gamma(size=n, scale=scale, shape=shape).tolist()




# ----- Geometric Distribution  -------

def dgeom(x:Iterable|Real, prob:Real)->list|Real:
	"""
	x: Number of failures before success occurs.
	prob: probability of success in each trial.
	"""
	return _pydll.c_stat_dgeom(py_object(x), c_double(prob))


def pgeom(q:Iterable|Real, prob:Real)->list|Real:
	"""
	q: Number of failures before success occurs.
	prob: probability of success in each trial.
	"""
	return _pydll.c_stat_pgeom(py_object(q), c_double(prob))


def qgeom(p:Iterable|Real, prob:Real)->list|Real:
	"""
	p: probabilities
	prob: probability of success in each trial.
	"""
	return _pydll.c_stat_qgeom(py_object(p), c_double(prob))


def rgeom(n:int, prob:Real)->list:
	"""
	Draw samples from geometric distribution
	"""
	assert n>0 ,"n>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _np.random.geometric(size=n, p=prob).tolist()




# ----- Hypergeometric Distribution  -------

def dhyper(x:Iterable|Real, m:int, n:int, k:int)->list|Real:
	"""
	m: number of good samples in the urn
	n: number of bad samples in the urn
	k: samples drawn from the urn
	"""
	return _pydll.c_stat_dhyper(py_object(x), c_int(m), c_int(n), c_int(k))


def phyper(q:Iterable|Real, m:int, n:int, k:int)->list|Real:
	"""
	m: number of good samples in the urn
	n: number of bad samples in the urn
	k: samples drawn from the urn
	"""
	return _pydll.c_stat_phyper(py_object(q), c_int(m), c_int(n), c_int(k))


def qhyper(p:Iterable|Real, m:int, n:int, k:int)->list|Real:
	"""
	m: number of good samples in the urn
	n: number of bad samples in the urn
	k: samples drawn from the urn
	"""
	return _pydll.c_stat_qhyper(py_object(p), c_int(m), c_int(n), c_int(k))


def rhyper(nn:int, m:int, n:int, k:int)->list:
	"""
	m: number of good samples in the urn
	n: number of bad samples in the urn
	k: samples drawn from the urn
	"""
	assert nn>0 ,"nn>0 expected"
	assert m>0, "m>0 expected"
	assert n>0, "n>0 expected"
	assert k>0, "k>0 expected"

	return _np.random.hypergeometric(size=nn, ngood=m, nbad=n, nsample=k)




# ----- Normal Distribution  -------

def dnorm(x:Iterable|Real, mean=0.0, sd=1.0)->list|Real:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	return _pydll.c_stat_dnorm(py_object(x), c_double(mean), c_double(sd))


def pnorm(q:Iterable|Real, mean=0.0, sd=1.0)->list|Real:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	return _pydll.c_stat_pnorm(py_object(q), c_double(mean), c_double(sd))


def qnorm(p:Iterable|Real, mean=0.0, sd=1.0)->list|Real:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	return _pydll.c_stat_qnorm(py_object(p), c_double(mean), c_double(sd))


def rnorm(n:int, mean=0.0, sd=1.0)->list:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	assert n>0 ,"n>0 expected"
	assert sd>0, "sd>0 expected"

	return _np.random.normal(size=n, loc=mean, scale=sd).tolist()




# ----- Log Normal Distribution  -------

def dlnorm(x:Iterable|Real, meanlog=0.0, sdlog=1.0)->list|Real:
	"""
	meanlog: mean value of the distribution
	sdlog: standard deviation of the distribution
	"""
	return _pydll.c_stat_dlnorm(py_object(x), c_double(meanlog), c_double(sdlog))


def plnorm(q:Iterable|Real, meanlog=0.0, sdlog=1.0)->list|Real:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	return _pydll.c_stat_plnorm(py_object(q), c_double(meanlog), c_double(sdlog))


def qlnorm(p:Iterable|Real, meanlog=0.0, sdlog=1.0)->list|Real:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	return _pydll.c_stat_qlnorm(py_object(p), c_double(meanlog), c_double(sdlog))


def rlnorm(n:int, meanlog=0.0, sdlog=1.0)->list:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	assert n>0 ,"n>0 expected"
	assert sdlog>0, "sd>0 expected"

	return _np.random.lognormal(size=n, mean=meanlog, sigma=sdlog).tolist()




# ----- Pareto Distribution  -------

def dpareto(x:Iterable|Real, location:Real, shape=1.0)->list|Real:
	"""
	location: location parameter
	shape: shape parameter
	"""
	assert location>0 and shape>0, "'location' and 'shape' must be positive"
	return _pydll.c_stat_dpareto(py_object(x), c_double(location), c_double(shape))


def ppareto(q:Iterable|Real, location:Real, shape=1.0)->list|Real:
	"""
	location: location parameter
	shape: shape parameter
	"""
	assert location>0 and shape>0, "'location' and 'shape' must be positive"
	return _pydll.c_stat_ppareto(py_object(q), c_double(location), c_double(shape))


def qpareto(p:Iterable|Real, location:Real, shape=1.0)->list|Real:
	"""
	location: location parameter
	shape: shape parameter
	"""
	assert location>0 and shape>0, "'location' and 'shape' must be positive"
	return _pydll.c_stat_qpareto(py_object(p), c_double(location), c_double(shape))


def rpareto(n:int, location:Real, shape=1.0)->list:
	"""
	location: location parameter
	shape: shape parameter
	"""
	assert location>0 and shape>0, "'location' and 'shape' must be positive"
	assert n>0 ,"n>0 expected"
	
	return (_np.random.pareto(size=n, a=shape)*location).tolist()




# ----- Poisson Distribution  -------

def dpois(x:Iterable|Real, mu:Real)->list|Real:
	return _pydll.c_stat_dpois(py_object(x), c_double(mu))


def ppois(q:Iterable|Real, mu:Real)->list|Real:
	return _pydll.c_stat_ppois(py_object(q), c_double(mu))


def qpois(p:Iterable|Real, mu:Real)->list|Real:
	return _pydll.c_stat_qpois(py_object(p), c_double(mu))


def rpois(n:int, mu = 1)->list:
	"""
	Draw samples from Poisson distribution
	"""
	assert n>0 ,"n>0 expected"
	assert mu>0, "mu>0 expected"

	return _np.random.poisson(size=n, lam=mu).tolist()



#---- Kolmogorov-Smirnov Dist --------

def psmirnov(q:Iterable|Real, n:int)->list|Real:
	"""
	n: size of the sample
	"""
	assert isinstance(n, int), "n must be int"
	assert n>0, "n>0 expected"

	return _pydll.c_stat_psmirnov(py_object(q), c_int(n))


# ----- t Distribution  -------

def dt(x:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"

	return _pydll.c_stat_dt(py_object(x), c_int(df))


def pt(q:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"

	return _pydll.c_stat_pt(py_object(q), c_int(df))


def qt(p:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"

	return _pydll.c_stat_qt(py_object(p), c_int(df))


def rt(n:int, df)->list:
	"""
	df: degrees of freedom
	"""
	assert n>0 ,"n>0 expected"
	assert df>0, "df1>0 expected"

	return _np.random.standard_t(size=n, df=df).tolist()




# ----- Uniform Distribution  -------

def dunif(x:Iterable|Real, min=0.0, max=1.0)->list|Real:
	"""
	min: minimum bound
	max: maximum bound
	"""
	assert max>min, "max>min expected"

	return _pydll.c_stat_dunif(py_object(x), c_double(min), c_double(max))


def punif(q:Iterable|Real, min=0.0, max=1.0)->list|Real:
	"""
	min: minimum bound
	max: maximum bound
	"""
	assert max>min, "max>min expected"

	return _pydll.c_stat_punif(py_object(q), c_double(min), c_double(max))


def qunif(p:Iterable|Real, min=0.0, max=1.0)->list|Real:
	"""
	min: minimum bound
	max: maximum bound
	"""
	assert max>min, "max>min expected"

	return _pydll.c_stat_qunif(py_object(p), c_double(min), c_double(max))


def runif(n:int, min=0.0, max=1.0)->list:
	"""
	min: minimum bound
	max: maximum bound
	"""
	assert max>min, "max>min expected"
	assert n>0 ,"n>0 expected"

	return _np.random.uniform(size=n, low=min, high=max).tolist()



# ----- Weibull Distribution  -------

def dweibull(x:Iterable|Real, shape:Real, scale = 1.0)->list|Real:
	"""
	x: quantile	
	shape: known as Weibull-slope
	scale: characteristic life
	"""
	assert shape>0, "shape>0 expected"
	assert scale>0, "scale>0 expected"

	return _pydll.c_stat_dweibull(py_object(x), c_double(shape), c_double(scale))


def pweibull(q:Iterable|Real, shape:Real, scale = 1.0)->list|Real:
	"""
	q: quantile
	shape: known as Weibull-slope
	scale: characteristic life
	"""
	assert shape>0, "shape>0 expected"
	assert scale>0, "scale>0 expected"

	return _pydll.c_stat_pweibull(py_object(q), c_double(shape), c_double(scale))


def qweibull(p:Iterable|Real, shape:Real, scale = 1.0)->list|Real:
	"""
	p: probabilities
	shape: known as Weibull-slope
	scale: characteristic life
	"""
	assert shape>0, "shape>0 expected"
	assert scale>0, "scale>0 expected"
	
	return _pydll.c_stat_qweibull(py_object(p), c_double(shape), c_double(scale))


def rweibull(n:int, shape:Real, scale=1.0)->list:
	"""
	Draw samples from weibull distribution
	"""
	assert n>0 ,"n>0 expected"
	assert shape>0, "shape>0 expected"
	assert scale>0, "scale>0 expected"

	return (scale*_np.random.weibull(size=n, a=shape, )).tolist()


# ----- Wilcoxon Sign Rank Distribution  -------

def dsignrank(x:Iterable|Real, n:int)->list|Real:
	return _pydll.c_stat_dsignrank(py_object(x), c_int(n))


def psignrank(q:Iterable|Real, n:int)->list|Real:
	return _pydll.c_stat_psignrank(py_object(q), c_int(n))


def qsignrank(p:Iterable|Real, n:int)->list|Real:
	return _pydll.c_stat_qsignrank(py_object(p), c_int(n))

