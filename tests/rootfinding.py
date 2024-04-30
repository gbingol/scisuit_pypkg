import sys, os
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scipy.optimize as opt
from scisuit.roots import brentq, toms748
from timeit import timeit

def performance():
	kwargs, N = {"f": lambda x: x**2-5, "a":0, "b":5}, 1000

	print("Scipy functions")
	print("brentq:", timeit(lambda: opt.brentq(**kwargs), number=N))
	print("toms748:", timeit(lambda: opt.toms748(**kwargs), number=N))

	print("scisuit functions")
	print("brentq:", timeit(lambda: brentq(**kwargs, tol=1E-16), number=N))
	print("toms748:", timeit(lambda: toms748(**kwargs, tol=1E-16), number=N))



"""

f1 = { "f":lambda x: x**2 - (1-x)**9,
	"df": lambda x: 2*x + 9*(1-x)**8,
	"d2f": lambda x: 2 - 72*(1-x)**7 }

f2 = { "f":lambda x: 1/8 * (9 - 1/x),
	"df": lambda x: 1 /(8*x**2),
	"d2f": lambda x: -1/(4*x**3) }

from scisuit.roots import newton

args = {"f":f1["f"], "x0":-1.4}
print(
	newton(**args, x1=1),
	newton(**args, fprime=f1["df"]),
	newton(**args, fprime=f1["df"], fprime2=f1["d2f"]), 
	sep="\n")

print("-----------------------")

args = {"f":f2["f"], "x0":0.001}
print(
	newton(**args, x1=0.25),
	newton(**args, fprime=f2["df"]),
	newton(**args, fprime=f2["df"], fprime2=f2["d2f"]),
	sep="\n")


"""

from scisuit.roots import brentq, bisect, itp


kwargs = {"f": lambda x: x**2-5, "a":0.01, "b":5}

print(
	"bisect: ", bisect(**kwargs), "\n",
	"brentq: ", brentq(**kwargs), "\n",
	"itp: ", itp(**kwargs))