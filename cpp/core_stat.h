#pragma once
#include <Python.h>

#include "dllimpexp.h"


#define EXTERN \
	extern "C" DLLPYBIND



//beta distribution
EXTERN PyObject* c_stat_dbeta(
	PyObject* X, 
	double shape1, 
	double shape2);

EXTERN PyObject* c_stat_pbeta(
	PyObject* qvalObj, 
	double shape1, 
	double shape2);

EXTERN PyObject* c_stat_qbeta(
	PyObject* pvalObj, 
	double shape1, 
	double shape2);



//binomial distribution
EXTERN PyObject * c_stat_dbinom(
	PyObject * X, 
	int size_, 
	double prob);

EXTERN PyObject * c_stat_pbinom(
	PyObject * qvalObj, 
	int size_, 
	double prob);

EXTERN PyObject * c_stat_qbinom(
	PyObject * pvalObj, 
	int size_, 
	double prob);



//negative-binomial distribution
EXTERN PyObject* c_stat_dnbinom(
	PyObject* X, 
	int size_, 
	double prob);

EXTERN PyObject* c_stat_pnbinom(
	PyObject* qvalObj, 
	int size_, 
	double prob);

EXTERN PyObject* c_stat_qnbinom(
	PyObject* pvalObj, 
	int size_, 
	double prob);



//multinomial distribution
EXTERN PyObject* c_stat_dmultinom(
	PyObject* X, 
	int size_, 
	PyObject* probs);



//chisq distribution
EXTERN PyObject * c_stat_dchisq(
	PyObject * xvalObj, 
	int df);

EXTERN PyObject * c_stat_pchisq(
	PyObject * qvalObj, 
	int df);

EXTERN PyObject * c_stat_qchisq(
	PyObject * pvalObj, 
	int df);



//exponential distribution
EXTERN PyObject* c_stat_dexp(
	PyObject* xvalObj, 
	double rate = 1.0);

EXTERN PyObject* c_stat_pexp(
	PyObject* qvalObj, 
	double rate = 1.0);

EXTERN PyObject* c_stat_qexp(
	PyObject* pvalObj, 
	double rate = 1.0);



//F distribution
EXTERN PyObject * c_stat_df(
	PyObject * xvalObj, 
	int df1, 
	int df2);

EXTERN PyObject * c_stat_pf(
	PyObject * qvalObj, 
	int df1, 
	int df2);

EXTERN PyObject * c_stat_qf(
	PyObject * pvalObj, 
	int df1, 
	int df2);



//Gamma distribution
EXTERN PyObject* c_stat_dgamma(
	PyObject* xvalObj, 
	double shape, 
	double scale = 1.0);

EXTERN PyObject* c_stat_pgamma(
	PyObject* qvalObj, 
	double shape, 
	double scale = 1.0);

EXTERN PyObject* c_stat_qgamma(
	PyObject* pvalObj, 
	double shape, 
	double scale = 1.0);



//geometric distribution
EXTERN PyObject* c_stat_dgeom(
	PyObject* X, 
	double prob);

EXTERN PyObject* c_stat_pgeom(
	PyObject* qvalObj, 
	double prob);

EXTERN PyObject* c_stat_qgeom(
	PyObject* pvalObj, 
	double prob);



//hypergeometric distribution
EXTERN PyObject* c_stat_dhyper(
	PyObject* X, 
	int m, 
	int n, 
	int k); 

EXTERN PyObject* c_stat_phyper(
	PyObject* qvalObj, 
	int m, 
	int n, 
	int k); 

EXTERN PyObject* c_stat_qhyper(
	PyObject* pvalObj,
	int m, 
	int n, 
	int k); 



//Normal distribution
EXTERN PyObject * c_stat_dnorm(
	PyObject * xvalObj, 
	double mean = 0.0, 
	double sd = 1.0);

EXTERN PyObject * c_stat_pnorm(
	PyObject * qvalObj, 
	double mean = 0.0, 
	double sd = 1.0);

EXTERN PyObject * c_stat_qnorm(
	PyObject * pvalObj, 
	double mean = 0.0, 
	double sd = 1.0);



//Lognormal distribution
EXTERN PyObject* c_stat_dlnorm(
	PyObject* xvalObj, 
	double meanlog = 0.0, 
	double sdlog = 1.0);

EXTERN PyObject* c_stat_plnorm(
	PyObject* qvalObj, 
	double meanlog = 0.0, 
	double sdlog = 1.0);

EXTERN PyObject* c_stat_qlnorm(
	PyObject* pvalObj, 
	double meanlog = 0.0, 
	double sdlog = 1.0);



//Pareto distribution
EXTERN PyObject* c_stat_dpareto(
	PyObject* xvalObj, 
	double location, 
	double shape = 1.0);

EXTERN PyObject* c_stat_ppareto(
	PyObject* qvalObj, 
	double location, 
	double shape = 1.0);

EXTERN PyObject* c_stat_qpareto(
	PyObject* pvalObj, 
	double location, 
	double shape = 1.0);



//Poisson distribution
EXTERN PyObject * c_stat_dpois(
	PyObject * xvalObj, 
	double mu);

EXTERN PyObject * c_stat_ppois(
	PyObject * qvalObj, 
	double mu);

EXTERN PyObject * c_stat_qpois(
	PyObject * pvalObj, 
	double mu);




//Kolmogorov-Smirnov Dist
EXTERN PyObject * c_stat_psmirnov(
	PyObject * qvalObj, 
	int n);




//t distribution
EXTERN PyObject* c_stat_dt(
	PyObject* xvalObj, 
	int df);

EXTERN PyObject* c_stat_pt(
	PyObject* qvalObj, 
	int df);

EXTERN PyObject* c_stat_qt(
	PyObject* pvalObj, 
	int df);



//uniform distribution
EXTERN PyObject* c_stat_dunif(
	PyObject* xvalObj, 
	double min = 0.0, 
	double max = 0.0);

EXTERN PyObject* c_stat_punif(
	PyObject* qvalObj, 
	double min = 0.0, 
	double max = 0.0);

EXTERN PyObject* c_stat_qunif(
	PyObject* pvalObj, 
	double min = 0.0, 
	double max = 0.0);



//weibull distribution
EXTERN PyObject* c_stat_dweibull(
	PyObject* xvalObj, 
	double shape, 
	double scale);

EXTERN PyObject* c_stat_pweibull(
	PyObject* qvalObj, 
	double shape, 
	double scale);

EXTERN PyObject* c_stat_qweibull(
	PyObject* pvalObj, 
	double shape, 
	double scale);



//wilcoxon sign rank distribution
EXTERN PyObject* c_stat_dsignrank(
	PyObject* xvalObj, 
	int n);

EXTERN PyObject* c_stat_psignrank(
	PyObject* qvalObj, 
	int n);

EXTERN PyObject* c_stat_qsignrank(
	PyObject* pvalObj, 
	int n);





EXTERN PyObject* c_stat_moveavg(
	PyObject* X, 
	PyObject* Y, 
	int Period = 2);

EXTERN PyObject* c_stat_rolling(
	PyObject* X, 
	PyObject* Y, 
	int Period = 2);

EXTERN PyObject* c_stat_test_norm_ad(PyObject* Obj);



#undef EXTERN