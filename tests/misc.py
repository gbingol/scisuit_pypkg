
import sys
import pathlib

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))


import scisuit.plot as plt
import scisuit.plot.gdi as gdi





def canvasopts():
	plt.layout(2,2)

	#All shown
	plt.subplot(0,0)
	plt.canvas(x=[0,5], y=[0,5])

	#Horizontal axis not shown
	plt.subplot(0,1)
	plt.canvas(x=[0,5], y=[0,5], haxis=False)

	#Vertical axis not displayed
	plt.subplot(1,0)
	plt.canvas(x=[0,5], y=[0,5], vaxis=False)

	#Gridlines are not displayed
	plt.subplot(1,1)
	plt.canvas(x=[0,5], y=[0,5], vgrid=False, hgrid=False)



x = np.arange(0, 6, 0.5)

plt.scatter(x=x, y=x**2, lw=3, ls=":", marker="s")
plt.scatter(x=x, y=x, lw=3, ls=":", marker="s")
plt.scatter(x=x, y=2*x, lw=3, ls=":", marker="x", label = "2x")
id1 = gdi.line(p1=(1,1), p2=(3,5), label="line")
id2 = gdi.rect(xy=(1,1), height=5, width=4, label="rect", fc="#FF0000", hatch="/")

gdi.makegroup(id1, [id2])

plt.legend(3,2)
plt.show()


from math import sqrt, pi
from scisuit.stats import rbinom
n=60 ; p=0.4

#Generate random numbers from a binomial dist
x = np.array(rbinom(n=100, size=n, prob=p))
z = (x - n*p)/sqrt(n*p*(1-p))
f = 1.0/sqrt(2*pi)*np.exp(-z**2/2.0)

plt.hist(z, density=True)
plt.scatter(x=z, y=f)