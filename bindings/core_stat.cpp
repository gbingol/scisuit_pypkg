#include "core_stat.h"

#include <cmath>

#include <core/core_funcs.h>
#include <core/stats/distributions.h>
#include <core/stats/basictests/normality.h>
#include <core/math/fitting.h>

#include "wrapperfuncs.h"


using namespace core::stats;




PyObject* c_stat_dbeta(PyObject* X, double shape1, double shape2)
{
	TRYBLOCK();

	if (IsRealNum(X))
	{
		double dval = dist::dbeta(*GetAsRealNumber(X), shape1, shape2);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(X);
	return List_FromVector(dist::dbeta(Vec, shape1, shape2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pbeta(PyObject* qvalObj, double shape1, double shape2)
{
	TRYBLOCK();

	if (IsRealNum(qvalObj))
	{
		double dval = dist::pbeta(*GetAsRealNumber(qvalObj), shape1, shape2);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pbeta(Vec, shape1, shape2));

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qbeta(PyObject* pvalObj, double shape1, double shape2)
{
	TRYBLOCK();

	if (IsRealNum(pvalObj))
	{
		double dval = dist::qbeta(*GetAsRealNumber(pvalObj), shape1, shape2);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qbeta(Vec, shape1, shape2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------        binomial distribution -------------------*/
PyObject* c_stat_dbinom(PyObject* X, int size_, double prob)
{
	TRYBLOCK();

	if (IsRealNum(X))
	{
		double dval = dist::dbinom(*GetAsRealNumber(X), size_, prob);
		return Py_BuildValue("d", dval);
	}
		
	auto Vec = Iterable_As1DVector(X);
	return List_FromVector(dist::dbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pbinom(PyObject* qvalObj, int size_, double prob)
{
	TRYBLOCK();

	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pbinom(qval, size_, prob));
	}
		
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qbinom(PyObject* pvalObj, int size_, double prob)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qbinom(pval, size_, prob));
	}
		
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------     negative binomial distribution -------------------*/
PyObject* c_stat_dnbinom(PyObject* X, int size_, double prob)
{
	TRYBLOCK();

	if (IsRealNum(X))
	{
		double dval = dist::dnbinom(*GetAsRealNumber(X), size_, prob);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(X);
	return List_FromVector(dist::dnbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pnbinom(PyObject* qvalObj, int size_, double prob)
{
	TRYBLOCK();

	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pnbinom(qval, size_, prob));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pnbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qnbinom(PyObject* pvalObj, int size_, double prob)
{
	TRYBLOCK();

	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qnbinom(pval, size_, prob));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qnbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}






/* --------------- multinomial distribution ---------------- */

PyObject* c_stat_dmultinom(PyObject* X, int size_, PyObject* probs)
{
	TRYBLOCK();

	auto x = Iterable_As1DVector<int>(X);
	auto prob = Iterable_As1DVector(probs);
	return Py_BuildValue("d", dist::dmultinom(x, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}





/*  -----------        chisq distribution -------------------*/
PyObject* c_stat_dchisq(PyObject* xvalObj, int df)
{
	TRYBLOCK();

	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dchisq(xval, df));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dchisq(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pchisq(PyObject* qvalObj, int df)
{
	TRYBLOCK();
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pchisq(qval, df));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pchisq(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qchisq(PyObject* pvalObj, int df)
{
	TRYBLOCK();
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qchisq(pval, df));
	}
		
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qchisq(Vec, df));
		
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


/*  -----------        Exponential distribution -------------------*/

PyObject* c_stat_dexp(PyObject* xvalObj, double rate)
{
	TRYBLOCK();

	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dexp(xval, rate));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dexp(Vec, rate));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pexp(PyObject* qvalObj, double rate)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pexp(qval, rate));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pexp(Vec, rate));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qexp(PyObject* pvalObj, double rate)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qexp(pval, rate));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qexp(Vec, rate));

	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        F distribution -------------------*/
PyObject* c_stat_df(PyObject* xvalObj, int df1, int df2)
{
	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::df(xval, df1, df2));
	}
	
	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::df(Vec, df1, df2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pf(PyObject* qvalObj, int df1, int df2)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pf(qval, df1, df2));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pf(Vec, df1, df2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qf(PyObject* pvalObj, int df1, int df2)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qf(pval, df1, df2));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qf(Vec, df1, df2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------        Gamma distribution -------------------*/

PyObject* c_stat_dgamma(PyObject* xvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		double dval = dist::dgamma(GetAsRealNumber(xvalObj).value(), shape, scale);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dgamma(Vec, shape, scale));
	

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pgamma(PyObject* qvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pgamma(qval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pgamma(Vec, shape, scale));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qgamma(PyObject* pvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qgamma(pval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qgamma(Vec, shape, scale));
	

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------        geometric distribution -------------------*/
PyObject* c_stat_dgeom(PyObject* X, double prob)
{
	TRYBLOCK();
	
	if (IsRealNum(X))
	{
		double dval = dist::dgeom(*GetAsRealNumber(X), prob);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(X);
	return List_FromVector(dist::dgeom(Vec, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pgeom(PyObject* qvalObj, double prob)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pgeom(qval, prob));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pgeom(Vec, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qgeom(PyObject* pvalObj, double prob)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qgeom(pval, prob));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qgeom(Vec, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/***************       hypergeometric dist        ******************/

PyObject* c_stat_dhyper(PyObject* X, int m, int n, int k)
{
	TRYBLOCK();
	
	if (IsRealNum(X))
	{
		double xval = *GetAsRealNumber(X);
		return Py_BuildValue("d", dist::dhyper(xval, m, n, k));
	}

	auto Vec = Iterable_As1DVector(X);
	return List_FromVector(dist::dhyper(Vec, m, n, k));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_phyper(PyObject* qvalObj, int m, int n, int k)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::phyper(qval, m, n, k));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::phyper(Vec, m, n, k));
	

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qhyper(PyObject* pvalObj, int m, int n, int k)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qhyper(pval, m, n, k));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qhyper(Vec, m, n, k));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------        Normal distribution -------------------*/

PyObject* c_stat_dnorm(PyObject* xvalObj, double mean, double sd)
{
	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dnorm(xval, mean, sd));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dnorm(Vec, mean, sd));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pnorm(PyObject* qvalObj, double mean, double sd)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pnorm(qval, mean, sd));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pnorm(Vec, mean, sd));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qnorm(PyObject* pvalObj, double mean, double sd)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qnorm(pval, mean, sd));
	}
	
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qnorm(Vec, mean, sd));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        Lognormal distribution -------------------*/

PyObject* c_stat_dlnorm(PyObject* xvalObj, double meanlog, double sdlog)
{
	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dlnorm(xval, meanlog, sdlog));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dlnorm(Vec, meanlog, sdlog));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_plnorm(PyObject* qvalObj, double meanlog, double sdlog)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::plnorm(qval, meanlog, sdlog));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::plnorm(Vec, meanlog, sdlog));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qlnorm(PyObject* pvalObj, double meanlog, double sdlog)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qlnorm(pval, meanlog, sdlog));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qlnorm(Vec, meanlog, sdlog));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        Pareto distribution -------------------*/

PyObject* c_stat_dpareto(PyObject* xvalObj, double location, double shape)
{
	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dpareto(xval, location, shape));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dpareto(Vec, location, shape));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_ppareto(PyObject* qvalObj, double location, double shape)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::ppareto(qval, location, shape));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::ppareto(Vec, location, shape));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qpareto(PyObject* pvalObj, double location, double shape)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qpareto(pval, location, shape));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qpareto(Vec, location, shape));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        Poisson distribution -------------------*/
PyObject* c_stat_dpois(PyObject* xvalObj, double mu)
{
	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dpois(xval, mu));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dpois(Vec, mu));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_ppois(PyObject* qvalObj, double mu)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::ppois(qval, mu));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::ppois(Vec, mu));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qpois(PyObject* pvalObj, double mu)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qpois(pval, mu));
	}
	
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qpois(Vec, mu));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        t distribution -------------------*/

PyObject* c_stat_dt(PyObject* xvalObj, int df)
{
	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dt(xval, df));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dt(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pt(PyObject* qvalObj, int df)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pt(qval, df));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pt(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qt(PyObject* pvalObj, int df)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qt(pval, df));
	}
	
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qt(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



//Kolmogorov-Smirnov Dist
PyObject * c_stat_psmirnov(PyObject * qvalObj, int n)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double pval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::psmirnov(pval, n));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::psmirnov(Vec, n));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


/*  -----------        uniform distribution -------------------*/

PyObject* c_stat_dunif(PyObject* xvalObj, double min, double max)
{
	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dunif(xval, min, max));
	}
	
	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dunif(Vec, min, max));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_punif(PyObject* qvalObj, double min, double max)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::punif(qval, min, max));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::punif(Vec, min, max));	
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qunif(PyObject* pvalObj, double min, double max)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qunif(pval, min, max));
	}
	
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qunif(Vec, min, max));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



//weibull distribution

PyObject* c_stat_dweibull(PyObject* xvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		double xval = GetAsRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dweibull(xval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromVector(dist::dweibull(Vec, shape, scale));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_stat_pweibull(PyObject* qvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::pweibull(qval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromVector(dist::pweibull(Vec, shape, scale));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_stat_qweibull(PyObject* pvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		return Py_BuildValue("d", dist::qweibull(pval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromVector(dist::qweibull(Vec, shape, scale));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        wilcoxon sign rank distribution -------------------*/

PyObject* c_stat_dsignrank(PyObject* xvalObj, int n)
{
	IF_PYERR(n<=0, PyExc_ValueError, "n must be >0");

	TRYBLOCK();
	
	if (IsRealNum(xvalObj))
	{
		int xval = static_cast<int>(std::round(GetAsRealNumber(xvalObj).value()));
		return Py_BuildValue("d", dist::dsignrank(xval, n));
	}

	auto Vec = Iterable_As1DVector(xvalObj);

	core::CVector retVec;
	for (const auto& xv : Vec)
		retVec.push_back(dist::dsignrank(static_cast<int>(xv), n));

	return List_FromVector(retVec.data());
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_psignrank(PyObject* qvalObj, int n)
{
	IF_PYERR(n<=0, PyExc_ValueError, "n must be >0");

	TRYBLOCK();
	
	if (IsRealNum(qvalObj))
	{
		double qval = *GetAsRealNumber(qvalObj);
		return Py_BuildValue("d", dist::psignrank(qval, n));
	}

	auto Vec = Iterable_As1DVector(qvalObj);

	core::CVector retVec;
	for (const auto& qv : Vec)
		retVec.push_back(dist::psignrank(qv, n));

	return List_FromVector(retVec.data());
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qsignrank(PyObject* pvalObj, int n)
{
	IF_PYERR(n<=0, PyExc_ValueError, "n must be >0");

	TRYBLOCK();
	
	if (IsRealNum(pvalObj))
	{
		double pval = *GetAsRealNumber(pvalObj);
		CHECKRANGE_RET(pval, 0.0, 1.0, "p value must be in the range of (0,1).");

		return Py_BuildValue("d", dist::qsignrank(pval, n));
	}

	auto Vec = Iterable_As1DVector(pvalObj);

	core::CVector retVec;
	for (const auto& pv : Vec)
	{
		CHECKRANGE_RET(pv, 0.0, 1.0, "p value must be in the range of (0,1).");
		retVec.push_back(dist::qsignrank(pv, n));
	}

	return List_FromVector(retVec.data());
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}






// -------------    End of distributions    --------------



PyObject* c_stat_rolling(PyObject* X, PyObject* Y, int Period)
{
	IF_PYERR(Period <= 0, PyExc_ValueError, "period must be >0");
	IF_PYERR(Period < 2, PyExc_ValueError, "period must be >=2");

	auto xvec = Iterable_As1DVector(X);
	auto yvec = Iterable_As1DVector(Y);

	TRYBLOCK();
	
	auto Rolling = core::math::fitting::rolling(xvec, yvec, Period);

	auto DataList = PyList_New(Rolling.m_Data.size());
	for (size_t i = 0; const auto & V : Rolling.m_Data)
	{
		auto Item = List_FromVector(V.data());
		PyList_SetItem(DataList, i++, Item);
	}

	PyObject* Tuple = PyTuple_New(2);
	PyTuple_SetItem(Tuple, 0, List_FromVector(Rolling.m_X));
	PyTuple_SetItem(Tuple, 1, DataList);

	return Tuple;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_stat_test_norm_ad(PyObject* Obj)
{
	auto Data = Iterable_As1DVector(Obj);
	TRYBLOCK();
	
	auto Result = tests::normality::AndersonDarling(Data);

	auto TupleObj = PyTuple_New(2);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", Result.first));
	PyTuple_SetItem(TupleObj, 1, Py_BuildValue("d", Result.second));

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	return nullptr;
}


PyObject* c_stat_test_shapirowilkinson(PyObject* Obj)
{
	auto Data = Iterable_As1DVector(Obj);
	TRYBLOCK();
	
	auto Result = tests::normality::ShapiroWilkinson(Data);

	auto TupleObj = PyTuple_New(3);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", Result.w));
	PyTuple_SetItem(TupleObj, 1, Py_BuildValue("d", Result.pw));
	PyTuple_SetItem(TupleObj, 2, Py_BuildValue("s", Result.msg.c_str()));

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	return nullptr;
}