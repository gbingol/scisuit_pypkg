import numpy as _np
import ctypes as _ct
from typing import Iterable
from numbers import Real
from .._ctypeslib import coreDLL as _core


# ----- Binomial Distribution  -------

def dbinom(x:Iterable|Real, size:int, prob:float)->list|Real:
	"""
	size: number of trials
	prob: probability of success in each trial
	"""
	return _core.c_stat_dbinom(x, _ct.c_int(size), _ct.c_double(prob))


def pbinom(q:Iterable|Real, size:int, prob:float)->list|Real:
	"""
	size: number of trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _core.c_stat_pbinom(q, _ct.c_int(size), _ct.c_double(prob))

def qbinom(p:Iterable|Real, size:int, prob:float)->list|Real:
	"""
	size: number of trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _core.c_stat_qbinom(p, _ct.c_int(size), _ct.c_double(prob))
	

def rbinom(n:int, size:int, prob:float)->list:
	"""
	size: number of trials
	prob: probability of success in each trial
	"""
	assert n>0 ,"n>0 expected"
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _np.random.binomial(size=n, n=size, p=prob).tolist()




# ----- Negative-Binomial Distribution  -------

def dnbinom(x:Iterable|Real, size:int, prob:float)->list|Real:
	"""
	x: quantiles representing number of failures
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _core.c_stat_dnbinom(x, _ct.c_int(size), _ct.c_double(prob))


def pnbinom(q:Iterable|Real, size:int, prob:float)->list|Real:
	"""
	q: quantiles representing number of failures
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _core.c_stat_pnbinom(q, _ct.c_int(size), _ct.c_double(prob))

def qnbinom(p:Iterable|Real, size:int, prob:float)->list|Real:
	"""
	p: probabilities
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _core.c_stat_qnbinom(p, _ct.c_int(size), _ct.c_double(prob))


def rnbinom(n:int, size, prob)->list:
	"""
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	assert n>0 ,"n>0 expected"
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _np.random.negative_binomial(size=n, n=size, p=prob).tolist()



# ----- Multinomial Distribution  -------

def dmultinom(x:Iterable, size:int, prob:Iterable)->float:
	"""
	x: quantiles 
	size: number of trials
	prob: probabilities of success in each trial

	## Note:
	Internally sum of probabilities is normalized to 1.0
	"""

	assert sum(x) == size, "sum(x) == size expected."
	assert size>0, "size>0 expected"

	return _core.c_stat_dmultinom(x, _ct.c_int(size), prob)





# ----- Chi-Square Distribution  -------

def dchisq(x:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"

	return _core.c_stat_dchisq(x, _ct.c_int(df))

def pchisq(q:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"
	
	return _core.c_stat_pchisq(q, _ct.c_int(df))

def qchisq(p:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"
	
	return _core.c_stat_qchisq(p, _ct.c_int(df))


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
	return _core.c_stat_dexp(x, _ct.c_double(rate))


def pexp(q:Iterable|Real, rate = 1.0)->list|Real:
	"""
	q: quantiles
	rate: 1/mean, where mean is the waiting time for the next event recurrence
	"""
	return _core.c_stat_pexp(q,  _ct.c_double(rate))


def qexp(p:Iterable|Real, rate = 1.0)->list|Real:
	"""
	p: probabilities
	rate: 1/mean, where mean is the waiting time for the next event recurrence
	"""
	return _core.c_stat_qexp(p,  _ct.c_double(rate))


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

	return _core.c_stat_df(x, _ct.c_int(df1), _ct.c_int(df2))


def pf(q:Iterable|Real, df1:int, df2:int)->list|Real:
	"""
	df1: degrees of freedom, numerator
	df2: degrees of freedom, denominator
	"""
	assert df1>0, "df1>0 expected"
	assert df2>0, "df2>0 expected"

	return _core.c_stat_pf(q, _ct.c_int(df1), _ct.c_int(df2))

def qf(p:Iterable|Real, df1:int, df2:int)->list|Real:
	"""
	df1: degrees of freedom, numerator
	df2: degrees of freedom, denominator
	"""
	assert df1>0, "df1>0 expected"
	assert df2>0, "df2>0 expected"

	return _core.c_stat_qf(p, _ct.c_int(df1), _ct.c_int(df2))


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

def dgamma(x:Iterable|Real, shape:float, scale = 1.0)->list|Real:
	"""
	x: quantile	
	shape: waiting time for the rth event to occur
	scale: average waiting time for the next event recurrence
	"""
	return _core.c_stat_dgamma(x, _ct.c_double(shape), _ct.c_double(scale))


def pgamma(q:Iterable|Real, shape:float, scale = 1.0)->list|Real:
	"""
	q: quantile
	shape: waiting time for the rth event to occur
	scale: average waiting time for the next event recurrence
	"""
	return _core.c_stat_pgamma(q, _ct.c_double(shape), _ct.c_double(scale))


def qgamma(p:Iterable|Real, shape:float, scale = 1.0)->list|Real:
	"""
	p: probabilities
	shape: waiting time for the rth event to occur
	scale: average waiting time for the next event recurrence
	"""
	return _core.c_stat_qgamma(p, _ct.c_double(shape), _ct.c_double(scale))


def rgamma(n:int, shape:float, scale=1.0)->list:
	"""
	Draw samples from gamma distribution
	"""
	assert n>0 ,"n>0 expected"
	assert shape>0, "shape>0 expected"
	assert scale>0, "scale>0 expected"

	return _np.random.gamma(size=n, scale=scale, shape=shape).tolist()




# ----- Geometric Distribution  -------

def dgeom(x:Iterable|Real, prob:float)->list|Real:
	"""
	x: Number of failures before success occurs.
	prob: probability of success in each trial.
	"""
	return _core.c_stat_dgeom(x, _ct.c_double(prob))


def pgeom(q:Iterable|Real, prob:float)->list|Real:
	"""
	q: Number of failures before success occurs.
	prob: probability of success in each trial.
	"""
	return _core.c_stat_pgeom(q, _ct.c_double(prob))

def qgeom(p:Iterable|Real, prob:float)->list|Real:
	"""
	p: probabilities
	prob: probability of success in each trial.
	"""
	return _core.c_stat_qgeom(p, _ct.c_double(prob))


def rgeom(n:int, prob)->list:
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
	return _core.c_stat_dhyper(x, _ct.c_int(m), _ct.c_int(n), _ct.c_int(k))


def phyper(q:Iterable|Real, m:int, n:int, k:int)->list|Real:
	"""
	m: number of good samples in the urn
	n: number of bad samples in the urn
	k: samples drawn from the urn
	"""
	return _core.c_stat_phyper(q, _ct.c_int(m), _ct.c_int(n), _ct.c_int(k))


def qhyper(p:Iterable|Real, m:int, n:int, k:int)->list|Real:
	"""
	m: number of good samples in the urn
	n: number of bad samples in the urn
	k: samples drawn from the urn
	"""
	return _core.c_stat_qhyper(p, _ct.c_int(m), _ct.c_int(n), _ct.c_int(k))


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
	return _core.c_stat_dnorm(x, _ct.c_double(mean), _ct.c_double(sd))


def pnorm(q:Iterable|Real, mean=0.0, sd=1.0)->list|Real:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	return _core.c_stat_pnorm(q, _ct.c_double(mean), _ct.c_double(sd))


def qnorm(p:Iterable|Real, mean=0.0, sd=1.0)->list|Real:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	return _core.c_stat_qnorm(p, _ct.c_double(mean), _ct.c_double(sd))


def rnorm(n:int, mean=0.0, sd=1.0)->list:
	"""
	mean: mean value of the distribution
	sd: standard deviation of the distribution
	"""
	assert n>0 ,"n>0 expected"
	assert sd>0, "sd>0 expected"

	return _np.random.normal(size=n, loc=mean, scale=sd).tolist()




# ----- Poisson Distribution  -------

def dpois(x:Iterable|Real, mu:float)->list|Real:
	return _core.c_stat_dpois(x, _ct.c_double(mu))


def ppois(q:Iterable|Real, mu:float)->list|Real:
	return _core.c_stat_ppois(q, _ct.c_double(mu))


def qpois(p:Iterable|Real, mu:float)->list|Real:
	return _core.c_stat_qpois(p, _ct.c_double(mu))


def rpois(n:int, mu = 1)->list:
	"""
	Draw samples from Poisson distribution
	"""
	assert n>0 ,"n>0 expected"
	assert mu>0, "mu>0 expected"

	return _np.random.poisson(size=n, lam=mu).tolist()




# ----- t Distribution  -------

def dt(x:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"

	return _core.c_stat_dt(x, _ct.c_int(df))


def pt(q:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"

	return _core.c_stat_pt(q, _ct.c_int(df))


def qt(p:Iterable|Real, df:int)->list|Real:
	"""
	df: degrees of freedom
	"""
	assert df>0, "df>0 expected"

	return _core.c_stat_qt(p, _ct.c_int(df))


def rt(n:int, df)->list:
	"""
	df: degrees of freedom
	"""
	assert n>0 ,"n>0 expected"
	assert df>0, "df1>0 expected"

	return _np.random.standard_t(size=n, df=df).tolist()




# ----- Wilcoxon Sign Rank Distribution  -------

def dsignrank(x:Iterable|Real, n:int)->list|Real:
	return _core.c_stat_dsignrank(x, _ct.c_int(n))


def psignrank(q:Iterable|Real, n:int)->list|Real:
	return _core.c_stat_psignrank(q, _ct.c_int(n))


def qsignrank(p:Iterable|Real, n:int)->list|Real:
	return _core.c_stat_qsignrank(p, _ct.c_int(n))



# ----- Uniform Distribution  -------

def dunif(x:Iterable|Real, min=0.0, max=1.0)->list|Real:
	"""
	min: minimum bound
	max: maximum bound
	"""
	assert max>min, "max>min expected"

	return _core.c_stat_dunif(x, _ct.c_double(min), _ct.c_double(max))


def punif(q:Iterable|Real, min=0.0, max=1.0)->list|Real:
	"""
	min: minimum bound
	max: maximum bound
	"""
	assert max>min, "max>min expected"

	return _core.c_stat_punif(q, _ct.c_double(min), _ct.c_double(max))


def qunif(p:Iterable|Real, min=0.0, max=1.0)->list|Real:
	"""
	min: minimum bound
	max: maximum bound
	"""
	assert max>min, "max>min expected"

	return _core.c_stat_qunif(p, _ct.c_double(min), _ct.c_double(max))


def runif(n:int, min=0.0, max=1.0)->list:
	"""
	min: minimum bound
	max: maximum bound
	"""
	assert max>min, "max>min expected"
	assert n>0 ,"n>0 expected"

	return _np.random.uniform(size=n, low=min, high=max).tolist()