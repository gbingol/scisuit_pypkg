import numpy as _np


def rbinom(n:int, size, prob):
	"""
	Draw samples from binomial distribution
	"""
	assert n>0 ,"n>0 expected"
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _np.random.binomial(size=n, n=size, p=prob).tolist()


def rnbinom(n:int, size, prob):
	"""
	Draw samples from negative binomial distribution
	"""
	assert n>0 ,"n>0 expected"
	assert size>0, "size>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _np.random.negative_binomial(size=n, n=size, p=prob).tolist()


def rchisq(n:int, df):
	"""
	Draw samples from Chi-Square distribution
	"""
	assert n>0 ,"n>0 expected"
	assert df>0, "df>0 expected"

	return _np.random.chisquare(size=n, df = df).tolist()


def rexp(n:int, rate=1.0):
	"""
	Draw samples from exponential distribution
	"""
	assert n>0 ,"n>0 expected"
	assert rate>0, "rate>0 expected"

	return _np.random.exponential(size=n, scale=1/rate).tolist()


def rf(n:int, df1, df2):
	"""
	Draw samples from F distribution
	"""
	assert n>0 ,"n>0 expected"
	assert df1>0, "df1>0 expected"
	assert df2>0, "df2>0 expected"

	return _np.random.f(size=n, dfnum=df1, dfden=df2).tolist()


def rexp(n:int, shape:float, scale=1.0):
	"""
	Draw samples from gamma distribution
	"""
	assert n>0 ,"n>0 expected"
	assert shape>0, "shape>0 expected"
	assert scale>0, "scale>0 expected"

	return _np.random.gamma(size=n, scale=scale, shape=shape).tolist()


def rgeom(n:int, prob):
	"""
	Draw samples from geometric distribution
	"""
	assert n>0 ,"n>0 expected"
	assert prob>=0 and prob<=1, "prob in [0, 1] expected"

	return _np.random.geometric(size=n, p=prob).tolist()


def rhyper(nn:int, m:int, n:int, k:int):
	"""
	Draw samples from hypergeometric distribution
	"""
	assert nn>0 ,"nn>0 expected"
	assert m>0, "m>0 expected"
	assert n>0, "n>0 expected"
	assert k>0, "k>0 expected"

	return _np.random.hypergeometric(size=nn, ngood=m, nbad=n, nsample=k)


def rnorm(n:int, mean=0.0, sd=1.0):
	"""
	Draw samples from normal distribution
	"""
	assert n>0 ,"n>0 expected"
	assert sd>0, "sd>0 expected"

	return _np.random.normal(size=n, loc=mean, scale=sd).tolist()


def rpois(n:int, mu = 1):
	"""
	Draw samples from Poisson distribution
	"""
	assert n>0 ,"n>0 expected"
	assert mu>0, "mu>0 expected"

	return _np.random.poisson(size=n, lam=mu).tolist()


def rt(n:int, df):
	"""
	Draw samples from standard Student's t distribution
	"""
	assert n>0 ,"n>0 expected"
	assert df>0, "df1>0 expected"

	return _np.random.standard_t(size=n, df=df).tolist()


def runif(n:int, min=0.0, max=1.0):
	"""
	Draw samples from uniform distribution
	"""
	assert n>0 ,"n>0 expected"

	return _np.random.uniform(size=n, low=min, high=max).tolist()