import sys, os
import numpy as np
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 



import scisuit.plot as plt


def bar():
	categ=["Q1", "Q2", "Q3", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	plt.bar(labels=categ, height=A, fc=(0,255,0), hatch="\\")
	plt.bar(height=B, labels=categ, lw=2)


def barh():
	categ=["Q1", "Q2", "Q3", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	plt.barh(labels=categ, width=A)
	plt.barh(width=B, labels=categ)


def histogram():
	import scisuit.stats as stat

	x=stat.rnorm(500)
	plt.hist(x, fc="255 0 0", lw=2, ec=[0,255,0])



def linechart():
	categories=["Q1", "Q2", "Q3", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	#Clustered line chart with two series
	plt.line(labels=categories, y=A, marker=plt.Marker(fc=(0,255,0)))
	plt.line(labels=categories, y=B)



def pie():
	data=[10, 6, 8]

	#labels have been automatically assigned as 1, 2 and 3.
	plt.pie(data)

"""
	#Labels explicitly defined
	plt.pie(data, labels=["A", "B", "C"])

	#Number of labels less than slices
	plt.pie(data, labels=["A"])

	#Explosion of whole pie
	plt.pie(data, explode = 1)

	#Explosion of only first slice
	plt.pie(data, explode = [1] )

	#arbitrary colors for each slice.
	plt.pie(data, colors = [plt.COLOR_GREEN, plt.COLOR_RED, plt.COLOR_CHOCOLATE] )

	#set the angle of first slice to 45°.
	plt.pie(data, startangle=45)
"""


def qqnorm():
	import scisuit.stats as stat
	x=stat.rnorm(100)

	#full control on marker
	plt.layout(1,2)

	plt.subplot(0,0)
	plt.qqnorm(x, lw=5, ec=(0, 255,0), 
			marker=plt.Marker(style="s", fc=(255,0,0), lw=2))


	#marker with default Pen and Brush properties
	plt.subplot(0, 1)
	plt.qqnorm(x, lw=3, marker="s")



def qqplot():
	t = [24, 33,43,43,43,44,46,49,49,52,53,54,56,57,57,58,59,61,62,67,71]
	c = [10,17,19,20,26,28,33,37,37,41,42,42,42,43,46,48,53,54,55,55,60,62,85]

	plt.qqplot(x=c, y=t, marker="c", markersize=10, fc="#FF0000")



def quiver():
	x=np.arange(-3.0, 3.0, 0.5)
	y=np.arange(-1.0, 5.0, 0.5)
	X, Y = np.meshgrid(x,y)

	#V= (u, v) = (0.5+0.8x)i + (1.5-0.8y)j
	U= 0.5 + 0.8*X
	V=1.5 - 0.8*Y

	#without scaling
	plt.quiver(X,Y, U, V)

	plt.figure()

	#with scaling
	plt.quiver(X,Y, U, V, scale = True)



def dirfield():
	t=np.arange(0.0, 2.0, 0.2)
	y=np.arange(-5.0, 0.0, 0.2)

	t, y = np.meshgrid(t,y) 
	
	f1= 4-t+2*y

	plt.dirfield(t,y,f1) 



def boxplot():
	x = [2, 1, 3, 6, 4]
	y = [7, 7, 8, 4, 2]

	plt.boxplot(data=x)
	plt.boxplot(data=y)


def scatter():
	x = np.arange(0, 6, 0.5)
	y = x**2

	plt.layout(2,1)

	#show line and marker with default pen and brush
	plt.subplot(0,0)
	plt.scatter(x=x, y=y, lw=3, ls=":", marker="s", markersize=10)

	#customize marker properties
	plt.subplot(1,0)
	plt.scatter(x=x, y=y, marker=plt.Marker(fc="#00FF00"))





def layout_test():
	from math import sqrt, pi
	from scisuit.stats import rbinom
	n=60 ; p=0.4

	#Generate random numbers from a binomial dist
	x = np.array(rbinom(n=100, size=n, prob=p))
	z = (x - n*p)/sqrt(n*p*(1-p))
	f = 1.0/sqrt(2*pi)*np.exp(-z**2/2.0)

	plt.layout(2,2)

	plt.subplot(0, 0, nrows=1, ncols=2)

	plt.hist(z, density=True)
	plt.scatter(x=z, y=f)

	gdi.line((-2, 0.1), (0, 0.5), edgecolor="0 255 0", lw=2, ls= "-.")
	gdi.rect([-2, 0.5], width=2, height=0.4, edgecolor=[0, 255, 0])

	gdi.ellipse(xy=(-1, 0.3), width=2, height=0.2, edgecolor="#A02A2A") 

	gdi.text([-1, 0.3], label="hello world", rotation=180)


	#new chart
	t = np.arange(0.0, 2.0, 0.2)
	y = np.arange(-5.0, 0.0, 0.2)
	t, y = np.meshgrid(t,y) 
	f1= 4-t+2*y #dy/dt

	plt.subplot(1,0)
	plt.dirfield(t,y,f1) 


	#new chart
	categ=["😁", "Q2", "😍", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	plt.subplot(1,1)
	plt.bar(labels=categ, height=A)
	plt.bar(height=B, labels=categ)




import scisuit.plot as plt
import scisuit.plot.gdi as gdi
import numpy as np


x=np.arange(-3.0, 3.0, 0.5)
y=np.arange(-1.0, 5.0, 0.5)
X, Y = np.meshgrid(x,y)

#V= (u, v) = (0.5+0.8x)i + (1.5-0.8y)j
U= 0.5 + 0.8*X
V=1.5 - 0.8*Y


plt.quiver(X,Y,U, V, scale=0.3, lw=3, ec=(0,255, 0), length=0.2, alpha = 0.25)

 

plt.show()
