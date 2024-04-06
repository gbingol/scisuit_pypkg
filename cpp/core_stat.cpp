#include "core_stat.h"

#include <algorithm>
#include <cmath>

#include <core/core_funcs.h>
#include <core/math/stat_dist.h>
#include <core/math/stat_tests.h>
#include <core/math/fitting.h>

#include "wrapperfuncs.h"


using namespace core::math;




PyObject* c_stat_dbeta(PyObject* X, double shape1, double shape2)
{
	TRYBLOCK();

	if (IsExactTypeRealNumber(X))
	{
		double dval = dist::dbeta(ExtractRealNumber(X).value(), shape1, shape2);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(X);
	return List_FromCVector(dist::dbeta(Vec, shape1, shape2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pbeta(PyObject* qvalObj, double shape1, double shape2)
{
	TRYBLOCK();

	if (IsExactTypeRealNumber(qvalObj))
	{
		double dval = dist::pbeta(ExtractRealNumber(qvalObj).value(), shape1, shape2);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pbeta(Vec, shape1, shape2));

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qbeta(PyObject* pvalObj, double shape1, double shape2)
{
	TRYBLOCK();

	if (IsExactTypeRealNumber(pvalObj))
	{
		double dval = dist::qbeta(ExtractRealNumber(pvalObj).value(), shape1, shape2);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qbeta(Vec, shape1, shape2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------        binomial distribution -------------------*/
PyObject* c_stat_dbinom(PyObject* X, int size_, double prob)
{
	TRYBLOCK();

	if (IsExactTypeRealNumber(X))
	{
		double dval = dist::dbinom(ExtractRealNumber(X).value(), size_, prob);
		return Py_BuildValue("d", dval);
	}
		
	auto Vec = Iterable_As1DVector(X);
	return List_FromCVector(dist::dbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pbinom(PyObject* qvalObj, int size_, double prob)
{
	TRYBLOCK();

	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pbinom(qval, size_, prob));
	}
		
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qbinom(PyObject* pvalObj, int size_, double prob)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qbinom(pval, size_, prob));
	}
		
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------     negative binomial distribution -------------------*/
PyObject* c_stat_dnbinom(PyObject* X, int size_, double prob)
{
	TRYBLOCK();

	if (IsExactTypeRealNumber(X))
	{
		double dval = dist::dnbinom(ExtractRealNumber(X).value(), size_, prob);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(X);
	return List_FromCVector(dist::dnbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pnbinom(PyObject* qvalObj, int size_, double prob)
{
	TRYBLOCK();

	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pnbinom(qval, size_, prob));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pnbinom(Vec, size_, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qnbinom(PyObject* pvalObj, int size_, double prob)
{
	TRYBLOCK();

	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qnbinom(pval, size_, prob));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qnbinom(Vec, size_, prob));
	
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

	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dchisq(xval, df));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dchisq(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pchisq(PyObject* qvalObj, int df)
{
	TRYBLOCK();
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pchisq(qval, df));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pchisq(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qchisq(PyObject* pvalObj, int df)
{
	TRYBLOCK();
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qchisq(pval, df));
	}
		
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qchisq(Vec, df));
		
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


/*  -----------        Exponential distribution -------------------*/

PyObject* c_stat_dexp(PyObject* xvalObj, double rate)
{
	TRYBLOCK();

	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dexp(xval, rate));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dexp(Vec, rate));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pexp(PyObject* qvalObj, double rate)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pexp(qval, rate));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pexp(Vec, rate));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qexp(PyObject* pvalObj, double rate)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qexp(pval, rate));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qexp(Vec, rate));

	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        F distribution -------------------*/
PyObject* c_stat_df(PyObject* xvalObj, int df1, int df2)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::df(xval, df1, df2));
	}
	
	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::df(Vec, df1, df2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pf(PyObject* qvalObj, int df1, int df2)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pf(qval, df1, df2));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pf(Vec, df1, df2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qf(PyObject* pvalObj, int df1, int df2)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qf(pval, df1, df2));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qf(Vec, df1, df2));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------        Gamma distribution -------------------*/

PyObject* c_stat_dgamma(PyObject* xvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		double dval = dist::dgamma(ExtractRealNumber(xvalObj).value(), shape, scale);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dgamma(Vec, shape, scale));
	

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pgamma(PyObject* qvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pgamma(qval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pgamma(Vec, shape, scale));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qgamma(PyObject* pvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qgamma(pval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qgamma(Vec, shape, scale));
	

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------        geometric distribution -------------------*/
PyObject* c_stat_dgeom(PyObject* X, double prob)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(X))
	{
		double dval = dist::dgeom(ExtractRealNumber(X).value(), prob);
		return Py_BuildValue("d", dval);
	}

	auto Vec = Iterable_As1DVector(X);
	return List_FromCVector(dist::dgeom(Vec, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pgeom(PyObject* qvalObj, double prob)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pgeom(qval, prob));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pgeom(Vec, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qgeom(PyObject* pvalObj, double prob)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qgeom(pval, prob));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qgeom(Vec, prob));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/***************       hypergeometric dist        ******************/

PyObject* c_stat_dhyper(PyObject* X, int m, int n, int k)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(X))
	{
		double xval = ExtractRealNumber(X).value();
		return Py_BuildValue("d", dist::dhyper(xval, m, n, k));
	}

	auto Vec = Iterable_As1DVector(X);
	return List_FromCVector(dist::dhyper(Vec, m, n, k));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_phyper(PyObject* qvalObj, int m, int n, int k)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::phyper(qval, m, n, k));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::phyper(Vec, m, n, k));
	

	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qhyper(PyObject* pvalObj, int m, int n, int k)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qhyper(pval, m, n, k));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qhyper(Vec, m, n, k));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



/*  -----------        Normal distribution -------------------*/

PyObject* c_stat_dnorm(PyObject* xvalObj, double mean, double sd)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dnorm(xval, mean, sd));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dnorm(Vec, mean, sd));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pnorm(PyObject* qvalObj, double mean, double sd)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pnorm(qval, mean, sd));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pnorm(Vec, mean, sd));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qnorm(PyObject* pvalObj, double mean, double sd)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qnorm(pval, mean, sd));
	}
	
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qnorm(Vec, mean, sd));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        Lognormal distribution -------------------*/

PyObject* c_stat_dlnorm(PyObject* xvalObj, double meanlog, double sdlog)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dlnorm(xval, meanlog, sdlog));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dlnorm(Vec, meanlog, sdlog));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_plnorm(PyObject* qvalObj, double meanlog, double sdlog)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::plnorm(qval, meanlog, sdlog));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::plnorm(Vec, meanlog, sdlog));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qlnorm(PyObject* pvalObj, double meanlog, double sdlog)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qlnorm(pval, meanlog, sdlog));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qlnorm(Vec, meanlog, sdlog));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        Pareto distribution -------------------*/

PyObject* c_stat_dpareto(PyObject* xvalObj, double location, double shape)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dpareto(xval, location, shape));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dpareto(Vec, location, shape));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_ppareto(PyObject* qvalObj, double location, double shape)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::ppareto(qval, location, shape));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::ppareto(Vec, location, shape));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qpareto(PyObject* pvalObj, double location, double shape)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qpareto(pval, location, shape));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qpareto(Vec, location, shape));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        Poisson distribution -------------------*/
PyObject* c_stat_dpois(PyObject* xvalObj, double mu)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dpois(xval, mu));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dpois(Vec, mu));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_ppois(PyObject* qvalObj, double mu)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::ppois(qval, mu));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::ppois(Vec, mu));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qpois(PyObject* pvalObj, double mu)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qpois(pval, mu));
	}
	
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qpois(Vec, mu));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        t distribution -------------------*/

PyObject* c_stat_dt(PyObject* xvalObj, int df)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dt(xval, df));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dt(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_pt(PyObject* qvalObj, int df)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pt(qval, df));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pt(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qt(PyObject* pvalObj, int df)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qt(pval, df));
	}
	
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qt(Vec, df));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



//Kolmogorov-Smirnov Dist
PyObject * c_stat_psmirnov(PyObject * qvalObj, int n)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double pval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::psmirnov(pval, n));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::psmirnov(Vec, n));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


/*  -----------        uniform distribution -------------------*/

PyObject* c_stat_dunif(PyObject* xvalObj, double min, double max)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dunif(xval, min, max));
	}
	
	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dunif(Vec, min, max));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_punif(PyObject* qvalObj, double min, double max)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::punif(qval, min, max));
	}
	
	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::punif(Vec, min, max));	
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qunif(PyObject* pvalObj, double min, double max)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qunif(pval, min, max));
	}
	
	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qunif(Vec, min, max));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



//weibull distribution

PyObject* c_stat_dweibull(PyObject* xvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		double xval = ExtractRealNumber(xvalObj).value();
		return Py_BuildValue("d", dist::dweibull(xval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(xvalObj);
	return List_FromCVector(dist::dweibull(Vec, shape, scale));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_stat_pweibull(PyObject* qvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::pweibull(qval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(qvalObj);
	return List_FromCVector(dist::pweibull(Vec, shape, scale));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_stat_qweibull(PyObject* pvalObj, double shape, double scale)
{
	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
		return Py_BuildValue("d", dist::qweibull(pval, shape, scale));
	}

	auto Vec = Iterable_As1DVector(pvalObj);
	return List_FromCVector(dist::qweibull(Vec, shape, scale));
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}




/*  -----------        wilcoxon sign rank distribution -------------------*/

PyObject* c_stat_dsignrank(PyObject* xvalObj, int n)
{
	CHECKPOSITIVE_RET(n, "n must be >0");

	TRYBLOCK();
	
	if (IsExactTypeRealNumber(xvalObj))
	{
		int xval = static_cast<int>(std::round(ExtractRealNumber(xvalObj).value()));
		return Py_BuildValue("d", dist::dsignrank(xval, n));
	}

	auto Vec = Iterable_As1DVector(xvalObj);

	core::CVector retVec;
	for (const auto& xv : Vec)
		retVec.push_back(dist::dsignrank(static_cast<int>(xv), n));

	return List_FromCVector(retVec);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_psignrank(PyObject* qvalObj, int n)
{
	CHECKPOSITIVE_RET(n, "n must be >0");

	TRYBLOCK();
	
	if (IsExactTypeRealNumber(qvalObj))
	{
		double qval = ExtractRealNumber(qvalObj).value();
		return Py_BuildValue("d", dist::psignrank(qval, n));
	}

	auto Vec = Iterable_As1DVector(qvalObj);

	core::CVector retVec;
	for (const auto& qv : Vec)
		retVec.push_back(dist::psignrank(qv, n));

	return List_FromCVector(retVec);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}


PyObject* c_stat_qsignrank(PyObject* pvalObj, int n)
{
	CHECKPOSITIVE_RET(n, "n must be >0");

	TRYBLOCK();
	
	if (IsExactTypeRealNumber(pvalObj))
	{
		double pval = ExtractRealNumber(pvalObj).value();
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

	return List_FromCVector(retVec);
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}






// -------------    End of distributions    --------------



PyObject* c_stat_moveavg(PyObject* X, PyObject* Y, int Period)
{
	CHECKPOSITIVE_RET(Period, "period must be >0");
	IF_PYERRVALUE_RET(Period < 2, "period must be >=2");

	auto xvec = Iterable_As1DVector(X); 
	auto yvec = Iterable_As1DVector(Y);

	TRYBLOCK();
	
	auto MoveAver = fitting::moveavg(xvec, yvec, Period);

	auto ListX = List_FromCVector(MoveAver.m_X);
	auto ListY = List_FromCVector(MoveAver.m_Y);

	auto Tuple = PyTuple_New(2);
	PyTuple_SetItem(Tuple, 0, ListX);
	PyTuple_SetItem(Tuple, 1, ListY);

	return Tuple;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_stat_rolling(PyObject* X, PyObject* Y, int Period)
{
	CHECKPOSITIVE_RET(Period, "period must be >0");
	IF_PYERRVALUE_RET(Period < 2, "period must be >=2");

	auto xvec = Iterable_As1DVector(X);
	auto yvec = Iterable_As1DVector(Y);

	TRYBLOCK();
	
	auto Rolling = fitting::rolling(xvec, yvec, Period);

	auto DataList = PyList_New(Rolling.m_Data.size());
	for (size_t i = 0; const auto & V : Rolling.m_Data)
	{
		auto Item = List_FromCVector(V);
		PyList_SetItem(DataList, i++, Item);
	}

	PyObject* Tuple = PyTuple_New(2);
	PyTuple_SetItem(Tuple, 0, List_FromCVector(Rolling.m_X));
	PyTuple_SetItem(Tuple, 1, DataList);

	return Tuple;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	Py_RETURN_NONE;
}



PyObject* c_stat_test_norm_ad(PyObject* Obj)
{
	auto Data = Iterable_As1DVector(Obj);
	TRYBLOCK();
	
	auto Result = tests::AndersonDarling(Data);

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
	
	auto Result = tests::ShapiroWilkinson(Data);

	auto TupleObj = PyTuple_New(3);
	PyTuple_SetItem(TupleObj, 0, Py_BuildValue("d", Result.w));
	PyTuple_SetItem(TupleObj, 1, Py_BuildValue("d", Result.pw));
	PyTuple_SetItem(TupleObj, 2, Py_BuildValue("s", Result.msg.c_str()));

	return TupleObj;
	
	CATCHRUNTIMEEXCEPTION(nullptr);

	return nullptr;
}