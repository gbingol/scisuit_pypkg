import numpy as np
import scipy.optimize as opt
import scipy.stats as stats


x_data = np.array([0, 3, 7, 10, 14, 18, 20])
y_data = np.array([4500, 29000, 90000, 229000, 1200000, 3100000, 5500000])

def exp_func(x, a, b):
    return a * np.exp(b * x)


params, covariance = opt.curve_fit(exp_func, x_data, y_data)
a_hat, b_hat = params  
param_errors = np.sqrt(np.diag(covariance))  # Standard errors


n = len(y_data)
p = len(params)
dof = n - p  

# Compute residuals
residuals = y_data - exp_func(x_data, *params)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)


r_squared = 1 - (ss_res / ss_tot)


t_values = params / param_errors
p_values = 2 * (1 - stats.t.cdf(np.abs(t_values), df=dof))  


alpha = 0.05
t_crit = stats.t.ppf(1 - alpha / 2, dof)  
conf_intervals = [(param - t_crit * err, param + t_crit * err) for param, err in zip(params, param_errors)]


print(f"Estimated Parameters:")
print(f"  a = {a_hat:.4f} ± {param_errors[0]:.4f} (95% CI: {conf_intervals[0][0]:.4f} to {conf_intervals[0][1]:.4f})")
print(f"  b = {b_hat:.4f} ± {param_errors[1]:.4f} (95% CI: {conf_intervals[1][0]:.4f} to {conf_intervals[1][1]:.4f})")
print(f"\nStatistical Tests:")
print(f"  t-values: {t_values}")
print(f"  p-values: {p_values}")
print(f"\nGoodness of Fit:")
print(f"  R-squared: {r_squared:.4f}")
print(f"  Degrees of Freedom: {dof}")
