from .roots import bisect, brentq, muller, newton, ridder, fsolve
from .fitting import linearinterp, lagrange, spline, expfit, logfit, logistfit, polyfit, powfit
from .integ import trapz, cumtrapz

rt_bisect = bisect
rt_brentq = brentq
rt_muller = muller
rt_newton = newton
rt_ridder = ridder
rt_fsolve = fsolve


#clean up namespace
del bisect, brentq, muller, newton, ridder, fsolve