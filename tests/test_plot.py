import sys, os
import numpy as np

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.stats as stat
import scisuit.plot as plt


def bar():
	categ=["Q1", "Q2", "Q3", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	plt.bar(labels=categ, height=A)
	plt.bar(height=B, labels=categ)


def barh():
	categ=["Q1", "Q2", "Q3", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	plt.barh(labels=categ, width=A)
	plt.barh(width=B, labels=categ)


def histogram():
	import scisuit.stats as stat

	x=stat.rnorm(500)
	plt.hist(x,  
			fill=plt.Brush(color=plt.COLOR_RED), 
			line=plt.Pen(color="0 255 0", width=2))



def linechart():
	categories=["Q1", "Q2", "Q3", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	#Clustered line chart with two series
	plt.line(labels=categories, y=A)
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
	x=stat.rnorm(100)

	#Normal Q-Q chart
	plt.qqnorm(x)

	#Marker specified
	marker = {'fill': plt.Color.WHITE, 'linecolor': plt.Color.BLUE, 'type': plt.MARKER_SQUARE, 'linewidth': 2, 'size': 5}
	plt.qqnorm(x, marker=marker)



def qqplot():
	treatment = [24, 33,43,43,43,44,46,49,49,52,53,54,56,57,57,58,59,61,62,67,71]
	control = [10,17,19,20,26,28,33,37,37,41,42,42,42,43,46,48,53,54,55,55,60,62,85]

	plt.qqplot(x=control, y=treatment, marker = plt.Marker(style = plt.MARKER_CIRCLE))



def quiver():
	x=np.arange(-3.0, 3.0, 0.5)
	y=np.arange(-1.0, 5.0, 0.5)
	X, Y = np.meshgrid(x,y)

	#V= (u, v) = (0.5+0.8x)i + (1.5-0.8y)j
	U= 0.5 + 0.8*X
	V=1.5 - 0.8*Y

	#without scaling
	plt.quiver(X,Y, U, V)

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
	x = [1, 2, 3, 4]
	y = [1, 3, 7, 14]

	plt.scatter(
	x=x, 
	y=y,
	trendline=plt.Trendline
		(
		style =plt.Trendline.STYLE.POLY,
		degree=3,
		intercept=-10,
		line=plt.Pen(color="255 0 0", width=2),
		show_equation=True,
		show_stats=True
		)
	)


def scisuit_hist_scatter():

	import math
	from scisuit.stats import rbinom

	n=60
	p=0.4

	#Generate random numbers from a binomial distribution
	x = np.array(rbinom(n=1000, size=n, prob=p), dtype=np.float32)

	#z-ratio
	z = (x - n*p)/math.sqrt(n*p*(1-p))

	#DeMoivre's equation
	f = 1.0/math.sqrt(2*math.pi)*np.exp(-z**2/2.0)

	#Density scaled histogram
	plt.hist(z, density=True)

	#Overlay scatter plot
	plt.scatter(x=z, y=f)


def scatter_quiver():
	t=np.arange(0.0, 2.0, 0.2)
	y=np.arange(-5.0, 0.0, 0.2)

	t, y = np.meshgrid(t,y) 

	f1= 4-t+2*y

	x1 = [1, 2, 3]
	y1 = [-1, -4, -6]

	plt.dirfield(t,y,f1) 
	plt.scatter(x=x1, y=y1)



def scatter_errorbar():

	import math
	import numpy as np
	import scisuit.plot as plt


	measurement = [0, 20, 100] #temperatures

	#Energy absorbed at different temperatures
	data = np.array([
		[52, 58, 82, 35, 84], #0C
		[48, 66, 74, 86, 78], #20
		[73.5, 82, 72, 80, 79] #100C
	])

	mean  = np.mean(data, axis=1)
	std = np.std(data, axis=1, ddof=1)
	se = std/ math.sqrt(data.shape[1])

	plt.scatter(x = measurement, y = mean)
	for i in range(len(measurement)):
		x1 = measurement[i]
		x2 = x1
		y1, y2 = mean[i] + se[i], mean[i] - se[i]
		plt.plot(
			x=[x1, x2], 
			y=[y1, y2], 
			color = plt.Color.BLACK, 
			style = plt.PEN_LONGDASH,
			width=2)



from math import sqrt, pi
from scisuit.stats import rbinom
import scisuit.plot as plt
import scisuit.plot.gdi as gdi


def layout_test():
	n=60 ; p=0.4

	#Generate random numbers from a binomial dist
	x = np.array(rbinom(n=100, size=n, prob=p))
	z = (x - n*p)/sqrt(n*p*(1-p))
	f = 1.0/sqrt(2*pi)*np.exp(-z**2/2.0)

	plt.layout(2,2)

	plt.subplot(0, 0, nrows=1, ncols=2)

	plt.hist(z, density=True)
	plt.scatter(x=z, y=f)

	gdi.line(p1=(-2, 0.1), p2=(0, 0.5), pen=gdi.Pen(plt.COLOR_GREEN, 2, plt.PEN_DOTDASH))
	gdi.rect(p =(-2, 0.5), width=2, height=0.4, pen=gdi.Pen(plt.COLOR_GREEN))

	gdi.ellipse(p = (-1, 0.3), width=2, height=0.2, pen=gdi.Pen(plt.COLOR_BROWN))

	gdi.text(p = (-1, 0.3), text="hello world", angle=180)


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


plt.canvas(x=(-10,10), y=(-1, 1))

#will not be shown (out of bounds)
gdi.arc(center = (4,3), 
		p1=(6, 3), 
		p2=(2,3),  
		pen=gdi.Pen(plt.COLOR_GREEN, width=3), 
		brush=gdi.Brush(plt.COLOR_BROWN, plt.BRUSH_FDIAGHATCH))

x= np.linspace(-10, 10, 100)
y = np.sin(x)
y2 = np.sin(x + np.pi/4)

gdi.curve(x, y)
gdi.curve(x, y2, pen=gdi.Pen(plt.COLOR_GREEN, width=2))

plt.show()



