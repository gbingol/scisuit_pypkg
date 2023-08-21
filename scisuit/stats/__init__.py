import numpy as _np
import ctypes as _ct

from .._ctypeslib import core as _core
from dataclasses import dataclass as _dataclass    




def dbinom(x:list|_np.ndarray, size:int, prob:float):
	return _core.c_stat_dbinom(x, _ct.c_int(size), _ct.c_double(prob))


def pbinom(q:list|_np.ndarray, size:int, prob:float):
	return _core.c_stat_pbinom(q, _ct.c_int(size), _ct.c_double(prob))

def qbinom(p:list|_np.ndarray, size:int, prob:float):
	return _core.c_stat_qbinom(p, _ct.c_int(size), _ct.c_double(prob))


#------------------------------

def dnbinom(x:list|_np.ndarray, size:int, prob:float):
	"""
	x: quantiles representing number of failures
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	return _core.c_stat_dnbinom(x, _ct.c_int(size), _ct.c_double(prob))


def pnbinom(q:list|_np.ndarray, size:int, prob:float):
	"""
	q: quantiles representing number of failures
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	return _core.c_stat_pnbinom(q, _ct.c_int(size), _ct.c_double(prob))

def qnbinom(p:list|_np.ndarray, size:int, prob:float):
	"""
	p: probabilities
	size: target for number of successful trials
	prob: probability of success in each trial
	"""
	return _core.c_stat_qnbinom(p, _ct.c_int(size), _ct.c_double(prob))




#------------------------------

def dexp(x:list|_np.ndarray, rate = 1.0):
	"""
	x: quantiles
	rate: 1/mean, where mean is the waiting time for the next event recurrence
	"""
	return _core.c_stat_dexp(x, _ct.c_double(rate))


def pexp(q:list|_np.ndarray, rate = 1.0):
	"""
	q: quantiles
	rate: 1/mean, where mean is the waiting time for the next event recurrence
	"""
	return _core.c_stat_pnbinom(q,  _ct.c_double(rate))

def qnbinom(p:list|_np.ndarray, rate = 1.0):
	"""
	p: probabilities
	rate: 1/mean, where mean is the waiting time for the next event recurrence
	"""
	return _core.c_stat_qnbinom(p,  _ct.c_double(rate))



#-----------------------------
def df(x, df1:int, df2:int):
	return _core.c_stat_df(x, _ct.c_int(df1), _ct.c_int(df2))

def pf(q, df1:int, df2:int):
	return _core.c_stat_pf(q, _ct.c_int(df1), _ct.c_int(df2))

def qf(p, df1:int, df2:int):
	return _core.c_stat_qf(p, _ct.c_int(df1), _ct.c_int(df2))


#-------------------------

def dgeom(x:list|_np.ndarray, prob:float):
	"""
	x: Number of failures before success occurs.
	prob: probability of success in each trial.
	"""
	return _core.c_stat_dgeom(x, _ct.c_double(prob))


def pgeom(q:list|_np.ndarray, prob:float):
	"""
	q: Number of failures before success occurs.
	prob: probability of success in each trial.
	"""
	return _core.c_stat_pgeom(q, _ct.c_double(prob))

def qgeom(p:list|_np.ndarray, prob:float):
	"""
	p: probabilities
	prob: probability of success in each trial.
	"""
	return _core.c_stat_qgeom(p, _ct.c_double(prob))


#----------------------

def dhyper(x, m:int, n:int, k:int):
	return _core.c_stat_dhyper(x, _ct.c_int(m), _ct.c_int(n), _ct.c_int(k))

def phyper(q, m:int, n:int, k:int):
	return _core.c_stat_phyper(q, _ct.c_int(m), _ct.c_int(n), _ct.c_int(k))

def qhyper(p, m:int, n:int, k:int):
	return _core.c_stat_qhyper(p, _ct.c_int(m), _ct.c_int(n), _ct.c_int(k))


#----------------
def dnorm(x, mean=0.0, sd=1.0):
	return _core.c_stat_dnorm(x, _ct.c_double(mean), _ct.c_double(sd))

def pnorm(q, mean=0.0, sd=1.0):
	return _core.c_stat_pnorm(q, _ct.c_double(mean), _ct.c_double(sd))

def qnorm(p, mean=0.0, sd=1.0):
	return _core.c_stat_qnorm(p, _ct.c_double(mean), _ct.c_double(sd))


#------------------
def dpois(x, mu:float):
	return _core.c_stat_dpois(x, _ct.c_double(mu))

def ppois(q, mu:float):
	return _core.c_stat_ppois(q, _ct.c_double(mu))

def qpois(p, mu:float):
	return _core.c_stat_qpois(p, _ct.c_double(mu))


#-----------------
def dt(x, df:int):
	return _core.c_stat_dt(x, _ct.c_int(df))

def pt(q, df:int):
	return _core.c_stat_pt(q, _ct.c_int(df))

def qt(p, df:int):
	return _core.c_stat_qt(p, _ct.c_int(df))


#----------------------------
def dchisq(x, df:int):
	return _core.c_stat_dchisq(x, _ct.c_int(df))

def pchisq(q, df:int):
	return _core.c_stat_pchisq(q, _ct.c_int(df))

def qchisq(p, df:int):
	return _core.c_stat_qchisq(p, _ct.c_int(df))


#-------------------
def dunif(x, min=0.0, max=1.0):
	return _core.c_stat_dunif(x, _ct.c_double(min), _ct.c_double(max))

def punif(q, min=0.0, max=1.0):
	return _core.c_stat_punif(q, _ct.c_double(min), _ct.c_double(max))

def qunif(p, min=0.0, max=1.0):
	return _core.c_stat_qunif(p, _ct.c_double(min), _ct.c_double(max))


#----------------
def dsignrank(x, n:int):
	return _core.c_stat_dsignrank(x, _ct.c_int(n))

def psignrank(q, n:int):
	return _core.c_stat_psignrank(q, _ct.c_int(n))

def qsignrank(p, n:int):
	return _core.c_stat_qsignrank(p, _ct.c_int(n))


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
from .kurt import kurt
from .linregress import linregress
from .rolling import rolling
from .mode import mode
from .sample import sample
from .skew import skew
from .test_z import test_z, test_z_Result
from .test_f import test_f, test_f_Result
from .test_sign import test_sign, test_sign_Result
from .test_t import test_t, test_t1_result, test_t2_result, test_tpaired_result

from .dist_random import rbinom, rchisq, rf, rgeom, rhyper, rnorm, rpois, rt, runif




