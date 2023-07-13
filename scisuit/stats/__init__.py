import ctypes as _ct
from .._ctypeslib import core as _core
from dataclasses import dataclass as _dataclass    


def dbinom(x, size:int, prob:float):
	return _core.c_stat_dbinom(x, _ct.c_int(size), _ct.c_double(prob))


def pbinom(q, size:int, prob:float):
	return _core.c_stat_pbinom(q, _ct.c_int(size), _ct.c_double(prob))

def qbinom(p, size:int, prob:float):
	return _core.c_stat_qbinom(p, _ct.c_int(size), _ct.c_double(prob))


def df(x, df1:int, df2:int):
	return _core.c_stat_df(x, _ct.c_int(df1), _ct.c_int(df2))

def pf(q, df1:int, df2:int):
	return _core.c_stat_pf(q, _ct.c_int(df1), _ct.c_int(df2))

def qf(p, df1:int, df2:int):
	return _core.c_stat_qf(p, _ct.c_int(df1), _ct.c_int(df2))

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

from .dist_random import rbinom, rchisq, rf, rnorm, rpois, rt, runif




